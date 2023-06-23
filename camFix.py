# Program to automatically fix camera issues with the camera in the Raspberry Pi

import subprocess, os
# comment here
print("File Status:  ", end='')
subprocess.call(["systemctl","is-enabled","ft-test3.service"])
print() # this is to leave a space between lines
# comment here
while True:
    
    # comment here
    response = input("Does the File Status in the line above say 'enabled' ? (y/n):  ")
    print() # this is to leave a space between lines
    
    # code to execute if status enabled
    if response.lower() == 'y':
        # disable camera and verify status
        subprocess.call(["sudo","systemctl","disable","ft-test3.service"])
        print("New File Status:  ", end='')
        subprocess.call(["systemctl","is-enabled","ft-test3.service"])
        print() # this is to leave a space between lines
        print("The file status is now correctly set. System reboot required to complete the update.")
        response = input("Allow system reboot ? (y/n):  ")
            
        # perform system reboot
        if response.lower() == 'y': subprocess.call(["sudo","reboot"])
        if response.lower() == 'n': print("System reboot failed")

        break # this quits the program
# print statement if status disabled
    elif response.lower() == 'n':
        # comment here
        print("If the file status is disabled your camera should be working. If it's not, please reach out for additional technical support.")
        break # this quits the program
# comment here
    else:
        print("Invalid Input: Please enter a 'y' to continue or 'n' to quit.")
        print() # this is to leave a space between lines
