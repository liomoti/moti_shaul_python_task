# BMC task
# Author: Moti Shaul

from datetime import datetime
import threading
import socket
import subprocess

class bcolors:
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# get user input and return the string separated by comma
def getInput():
    print(bcolors.HEADER + "Hi, Please enter list of pairs of hostname and root directory" + bcolors.ENDC)
    user_input = input(bcolors.HEADER + "e.g. Hostname1:port | /tempFolder , Hostname2:port | /tempFolder \n" + bcolors.ENDC)
    split_input = user_input.split(",")
    return split_input

# execute function scanRemote as thread
def startThreads(address, port, folder):
    try:
        x = threading.Thread(target=scanRemote, args=(address, port, folder,))
        x.start()
    except NameError:
        print("\033[91m Error: unable to start thread")

# connect to hostname with socket and print list of files from folder
def scanRemote(address, port, folder):
    try:
        # connect to host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, int(port)))
        # commands for getting list of files
        commands = ["dir", folder, "/b"]
        order = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
        # prepare text for print
        text_to_print = "ThreadID: " + str(threading.current_thread().ident) + "  Time: "+str(datetime.now().time()) + "\n"
        text_to_print += "Host address: " + address+":"+port + "  folder: " + folder + "\n"
        # get list of files
        response = order.stdout.readlines()
        sock.close()
        for item in response:
            text_to_print += item.rstrip().decode('utf-8') + "\n"

        text_to_print += "~~~~~~~~~~~~~" + "\n"
        print(text_to_print)
    except (ConnectionRefusedError, NameError, socket.error):
        print(bcolors.FAIL +"Error: unable to connect to "+address+":"+port+" "+folder + bcolors.ENDC)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    host_list = getInput()
    for item in host_list:
        host_and_folder = item.split("|")
        address_and_port = host_and_folder[0].split(":")
        if len(host_and_folder) != 2:
            print(bcolors.WARNING + host_and_folder[0]+" is not legal, must type host address and folder location" + bcolors.ENDC)
        elif len(address_and_port) != 2:
            print(bcolors.WARNING + host_and_folder[0] + " is not legal address, may you missing port?" + bcolors.ENDC)
        else:
            startThreads(address_and_port[0].rstrip().lstrip(), address_and_port[1].rstrip().lstrip(), host_and_folder[1].rstrip().lstrip())
