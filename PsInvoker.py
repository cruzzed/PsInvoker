import os
import subprocess
import socket
import getpass
import tkinter as tk
from tkinter import filedialog

#========FUNCTIONS========

def gethostuser():
    print ('Getting username and labname...')
    usr = getpass.getuser()
    if usr.lower() != 'localadmin':
        usr = str('TECHLAB\\'+usr).upper()
    elif usr.lower()== 'localadmin':
        usr = str('.\\'+usr)
    print ('Username:',usr)
    passwd = getpass.getpass(prompt='Please enter your password to run the file as your current user:', stream=None)
    print('Finding lab name...')
    if socket.gethostname().find('.')>=0:
        pcname=socket.gethostname()
    else:
        pcname=socket.gethostbyaddr(socket.gethostname())[0]
    if pcname.find('ID')>=0 or pcname.find('AS')>=0:
        labname = pcname[:2]
    elif pcname.find('CGI')>=0 or pcname.find('VFX')>=0:
        labname = pcname[:3]
    elif pcname.find('APLC')>=0:
        labname = pcname[:4]
    elif pcname.find('PLC')>=0 or pcname.find('SOC')>=0 or pcname.find('CNA')>=0:
        labname = pcname[:8]
    elif pcname.find('COMM')>=0 or pcname.find('ROBO')>=0:
        labname = pcname[:9]
    else:
        labname = pcname[:7]
    print ('Lab name:',labname)
    labpicker(labname,usr,passwd)

def labpicker(labname, usr, passwd):
    print ('Picking all PC number from provided list. ('+labname+'.txt)')
    with open(labname+'.txt') as pclist:
        allpc = pclist.read().split()
        print (allpc)
        nousepc=[]
        print ('List of PCs:')
        for pc in allpc:
            try:
                findhostcmd = 'WMIC /NODE:"'+pc+'" COMPUTERSYSTEM GET USERNAME'
                findhost = subprocess.check_output(findhostcmd, timeout=1, shell=False).decode('utf-8').upper()
                if findhost.find(usr) != -1:
                    nousepc.append(pc)
                    print (pc, 'is targeted.')
                elif findhost.find(pc) != -1:
                    nousepc.append(pc)
                    print(pc,'is logged in as local user and is targeted.')
                elif findhost.find('TECHLAB\\') == -1:
                    nousepc.append(pc)
                    print(pc,'is not used by anyone and still targeted.')
                else:
                    print(pc,'is used by other people.')
            except subprocess.CalledProcessError as e:
                result = e.output
                print (pc,'has an error:',result)
            except subprocess.TimeoutExpired as t:
                print(pc, 'is offline')
    #print ('List of targeted PC:')
    #for nopc in nousepc:
    #    print (nopc)
    invoker(labname,nousepc,usr,passwd)
    return nousepc

def invoker(labname,nousepc,usr,passwd):
    pc = str()
    print('''
    Select commands:
    1. CCK's rounding batch file
    2. Shutdown (shutdown /s /t xx)(Please be cautious by setting the time >30 seconds.)
    3. Restart (shutdown /r /t xx)(Please be cautious by setting the time >30 seconds.)
    4. Custom batch file (select your own batch file)
    5. Custom batch file as SYSTEM (select your own batch file)
    R. Refresh PC List (please use this if there is anyone recently come inside the lab.)
    X. Abort shutdown command (will not work if time set <30 seconds.)
    ''')
    selcmd = str(input('Enter input: '))
    if selcmd.upper() == '1':
        print ('Selected command type: CCK Batch file in temp')
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -u {1} -p {2} -d -c -i \\\\temp\\pub\\cck\\Rounding.bat'.format(pc,usr,passwd)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    elif selcmd.upper() == '2':
        print ('Selected command type: Shutdown')
        time = int(input('Please specify the countdown timer: '))
        time = str(time)
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -s -d shutdown /s /t {1}'.format(pc,time)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    elif selcmd.upper() == '3':
        print ('Selected command type: Restart')
        time = int(input('Please specify the countdown timer: '))
        time = str(time)
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -s -d shutdown /r /t {1}'.format(pc,time)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    elif selcmd.upper() == '4':
        print ('Selected command type: Custom')
        custompath = filedialog.askopenfilename()
        custompath = str(custompath).replace('/','\\')
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -u {1} -p {2} -d -c -i {3}'.format(pc,usr,passwd,custompath)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    elif selcmd.upper() == '5':
        print ('Selected command type: Custom with Run as System')
        custompath = filedialog.askopenfilename()
        custompath = str(custompath).replace('/','\\')
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -u {1} -p {2} -s -d -c -i {3}'.format(pc,usr,passwd,custompath)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    elif selcmd.upper() == 'R':
        print ('Selected command type: Refresh list')
        print ('Refreshing list...')
        labpicker(labname,usr,passwd)
    elif selcmd.upper() == 'X':
        print ('Selected type: Abort shutdown commands')
        time = int(input('Please specify the countdown timer: '))
        time = str(time)        
        for pc in nousepc:
            command = 'psexec -accepteula \\\\{0} -s -d shutdown /a'.format(pc)
            print('Attack commencing...')
            subprocess.Popen(command, shell=False)
        print('Attack finished...')
        invoker(labname,nousepc,usr,passwd)
    else:
        print ('Wrong input. Input again.')
        invoker(labname,nousepc,usr,passwd)
    
def main():
    print ('''
|PsInvoker v1.0
|Automatically execute specified commands on multiple remote hosts
|in a lab by utilizing a powerful remote command executer: PsExec.
|~Please login to all PC manually before use and copy all files to desktop~.
    ''')
    root = tk.Tk()
    root.withdraw()
    gethostuser()
#======END OF FUNCTIONS=======   
if __name__ == "__main__":
        main()
