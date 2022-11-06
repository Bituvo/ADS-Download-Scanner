import os
import subprocess
from shutil import copy2, move, rmtree
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

user = os.path.expanduser('~')
DOWNLOADS = os.path.join(user, 'Downloads')
TEMPFOLDER = os.path.join(user, 'AppData\\Local\\Temp')

rawOutput = subprocess.check_output(['dir', '/r'], cwd=DOWNLOADS, shell=True)
output = [i[20:].strip() for i in rawOutput.decode().split('\n')[7:]]

def getWarnings(trim=True):
    warnings = []
    for line in output:
        if ':' in line:
            file = ' '.join(line.split(' ')[1:])
            warnings.append(file.split(':'))

            if trim:
                if len(warnings[-1][0]) > 15:
                    warnings[-1][0] = warnings[-1][0][:15] + '...'

    return warnings

warnings = getWarnings()
        
root = tk.Tk()

if warnings == []:
    root.withdraw()
    showinfo('No ADS found', 'No alternate data streams were found in your Downloads folder.')
    root.destroy()

else:
    root.title('Warning: ADS found')
    root.geometry(f'800x560')
    root['bg'] = '#ddd'

    topFrame = tk.Frame(root, bg='#dcc')
    string = f'{len(warnings)} Alternate Data Stream' + ('s' if len(warnings) > 1 else '') + ' found'
    tk.Label(topFrame, text=string, font=('Segoe UI', 25, 'bold'), bg='#dcc').pack(padx=10, pady=10)
    topFrame.pack(fill='x')

    tk.Label(root, text='\nFilename\t\tADS name\t\tADS extension\t\tADS type', font=('Segoe UI', 14), bg='#ddd').pack(padx=10, pady=5, anchor='nw')
    
    contentsFrame = tk.Frame(root, height=300)
    contentsFrame.pack_propagate(False)
    scrollBar = tk.Scrollbar(contentsFrame)
    scrollBar.pack(side='right', fill='y')
    contentsFrame.pack(padx=10, pady=5, anchor='nw', fill='x')
    text = tk.Text(contentsFrame, font=('Segoe UI', 14), yscrollcommand=scrollBar.set)
    text.pack(anchor='nw')
    tk.Label(root, bg='#ddd').pack()
    scrollBar['command'] = text.yview

    toWrite = ''
    for warning in warnings:
        data = [warning[0]]
        data.append(''.join(warning[1].split('.')[:-1]))
        data.append(warning[1].split('.')[-1].upper())
        data.append(warning[2])

        string = '\t\t'.join(data[:2]) + '\t\t\t' + '\t\t\t'.join(data[2:])
        toWrite += f'{string.strip()}\n'

    text.insert('end', toWrite.strip())
    text['state'] = 'disabled'

    def removeAll():
        warnings = getWarnings(False)

        files = []
        for warning in warnings:
            files.append(os.path.join(DOWNLOADS, warning[0]))

        ADSDIR = os.path.join(TEMPFOLDER, 'ADS Removal')
        os.mkdir(ADSDIR)
        for file in files:
            copy2(file, os.path.join(ADSDIR, os.path.split(file)[1]))
            move(os.path.join(ADSDIR, os.path.split(file)[1]), file)
        rmtree(ADSDIR)

        showinfo('ADS removed', 'All alternate data streams were removed from your Downloads.')

    ttk.Style().configure("TButton", background='#ddd')
    buttonFrame = tk.Frame(root, bg='#ddd')
    ttk.Button(buttonFrame, text='Remove all', command=removeAll).pack(side='left', ipadx=30, ipady=10, padx=50)
    buttonFrame.pack(padx=10, pady=10)

    root.mainloop()
