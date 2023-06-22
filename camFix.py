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
    
    # comment here
    if response.lower() == 'y':
        # comment here
        subprocess.call(["sudo","systemctl","disable","ft-test3.service"])
        print("New File Status:  ", end='')
        subprocess.call(["systemctl","is-enabled","ft-test3.service"])
        print() # this is to leave a space between lines
        print("The file status is now correctly set. A test picture will be taken.")
        print("The testcam.jpg can be opened in the window that just popped up.")
        print("You can delete testcam.jpg once it's been validated.")
        folder_path = "/home/pi"
        os.chdir(folder_path)
        subprocess.call(["sudo","raspistill","-o","testcam.jpg"]) 
        subprocess.run(["xdg-open",folder_path])
        break # this quits the program
# comment here
    elif response.lower() == 'n':
        # comment here
        print("If the file status is disabled your camera should be working. If it's not, please reach out for additional technical support.")
        break # this quits the program
# comment here
    else:
        print("Invalid Input: Please enter a 'y' to continue or 'n' to quit.")
        print() # this is to leave a space between lines
