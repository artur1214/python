from termcolor import colored
import socket
GREEN = colored("[+] ", 'green')
RED = colored("[!] ", "red")
YELLOW = colored("[!] ", 'yellow')
def read1():
    print('~'*50)
    host = input(GREEN + "Host --> ")
    port = int(input(GREEN + "Port --> "))
    print("~"*50)
    scan = socket.socket()
    try:
        scan.connect((host, port))
    except socket.error:
        print(RED + "Port -- ", port, ' -- [CLOSED]')
    else:
        print(YELLOW + 'Port -- ', port, ' -- [OPEN]')

def read2():
    host = input(GREEN + "Host --> ")
    port  = range(6000,7001)
    for i in port:
        try:
            scan = socket.socket()
            scan.settimeout(0.5)
            scan.connect((host, i))
        except socket.error:
            pass
            #print(RED + "Port -- ", i, " -- [CLOSED]\n")
        else:
            print(YELLOW + "Port -- ", i, " -- [OPEN]\n")



print("~"*50)

print("\t[1] --- сканировать отделный порт")
print("\t[2] --- сканировать список")

print("~"*50, "\n")
text_a = input("[scan]--> ")

if text_a == "1":
    read1()
elif text_a == "2":
    read2()
else:
    
    print(colored("Параметр введен не правильно!", 'red'))




