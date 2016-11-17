# Linkit Smart Duo projects

#### Out of the box set up steps

    This procedure assumes using a Mac to set up.

1. Plug the unit into a 5V power supply.

    The chip has two USB ports. Plus a micro USB connector into the rightmost one. It supplies power to the chip and is also used to programs the Arduino side of the chip.
    
    The leftmost connector is a USB out connection. An OTG (on the go) USB adaptor is required to use it.

2. Wait for it to boot up

    On powering up, the chip's orange LED will blink once, then stay lit for about 30 seconds while it boots. After that it will blink on and off for a few seconds. When that stops, it's ready.

3. Check your computer wifi settings and look for an access point called "Linkit_Smart_xxxx_xxxxxx" (the x's will be hexadecimal digits).

4. Change your wifi settings to use the Linkit access point.

    When connected, the orange LED will blink three times, pause and repeat.

5. In your browser, go to http://mylinkit.local

6. You'll get a "please set a password" prompt. Set a password for the board.

7. Next you'll be asked to log in 

8. Update the board's firmware (switch back to your main wifi access point as needed)

    Follow these instructions to update the board's firmware: https://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_smart_7688/get_started/7688_duo/update/
    
    _Note: after updating, you'll need to start over again at step #1_ 

    * Firmware downloads page: https://labs.mediatek.com/site/global/developer_tools/mediatek_linkit_smart_7688/sdt_intro/index.gsp

    _Note: the firmware image file ends with a .img extension that Mac OS thinks is a disk image. This is just the firmware images and the .img cannot be opened as if it is a disk image on Mac._
    
    In general, you will
    * switch back to the Linkit access point
    * click the "upgrade firmware" button on the Linkit webUI
    * point to the lks7688.img firmware file
    * click Upgrade & Restart
    * wait 3 minutes while the chip upgrades the firmware (showing a continuously blinking wifi LED)
    * wait 30 seconds for the OS to boot (showing a solid wifi LED for 30 seconds)

9. Set the chip to "station" mode instead of "access point" mode

    In the chip's web UI click on "Network" (the right right of "System Information". Then select Station mode, choose your main wifi access point and enter the passcode.
  
10. Confirm you can SSH into the device

    In terminal, ssh to root@mylinkit.local with the password you set above
  
    _Note: if you have ssh'd into a different linkit board, you may need to delete its entry from ~/.ssh/known_hosts_  
  
11. Add a micro SD card for storage.

    _Note: the chip comes with a small amount of NAND Flash storage. But unlike a typical Flash drive, there is no usage leveling and atomic writes. Because NAND Flash storage has a limited number of erase/write cycles, it's best to use the NAND Flash drive only for critical use.
    
    * Power off the device
    * Insert a pre-formatted (FAT32) Micro SD card into the slot. I've had success with 1GB and 4GB cards.
    * Boot up the device
    * SSH in and confirm you can navigate to /Media/SD-P1 and see a usable drive

12. Create a dev folder

    * cd /Media/SD-P1
    * mkdir dev
    
13. Link to the dev folder in the root directory

    * cd ~
    * ln -s /Media/SD-P1/dev dev
    
    Now you can ssh in and type "cd dev" to get to that folder
    
14. Create an SSH key (to use services such as github.com)

    Generate your identity key

    * mkdir ~/.ssh
    * dropbearkey -t rsa -f ~/.ssh/id_rsa

    Convert public key from dropbear binary to openssh text
    
    * dropbearkey -y -f ~/.ssh/id_rsa | head -n 2 | tail -1
    
    Copy the public key that's output and add it to your account at Github.com
    
15. Change the git ssh command to use Dropbear
    
    * echo "#!/bin/sh" > ~/.gitssh.sh
    * echo "dbclient -y -i ~/.ssh/id_rsa \$\*" >> ~/.gitssh.sh
    * chmod +x ~/.gitssh.sh
    * echo "export GIT_SSH=\$HOME/.gitssh.sh" >> /etc/profile
    
    Log out and back in
    
    * ^D
    * ssh root@mylinkit.local
    
16. Clone a Github.com repository

    * cd ~/dev
    * git clone git@github.com:jhogsett/linkit.git
    
17. Install the Python Requests library for reaching the web

    * pip install requests
    
18. Run a Python program to verify things are set up

    * cd ~/dev/linkit/python
    * python circleci5.py {YOURKEY}
    
    Tail the log file to see if it's reaching CirclCI
    
    * tail -f ~/dev/linkit/python/circleci.log
  
19. Establish your Git identify

    Before you can commit changes, you need to let Git know who you are.

    * git config --global user.email "{YOUR EMAIL}"
    * git config --global user.name "{YOUR FULL NAME}"
  
20. Set up Git for pulling and pushing commits

    A _git pull_ is a _git fetch_ followed by a _git merge_. To do the merge, Git needs to know how. (One might think this would have been set up correctly to begin with, since Git comes pre-installed.)

    * ln -s $(which git) /usr/lib/git-core/git
    
    See: https://community.onion.io/topic/785/git-error-merge-not-found
        
21. Customize the 'ls' command

    Edit your profile and add an alias to customize the _ls_ command.

    * vim /etc/profile (for all users)
    
    or
    
    * vim /root/.profile (for root user)
    
    Then add
    
    * alias ls='ls -al' (or your desired customization)
    
    Then log out and back in.
    
    Add any other profile scripts to either file (there is no _.bashrc_).
    
22. Add your SSH key so you don't have to enter a password 

    Get your SSH public key. On a Mac it should be /Users/USERNAME/.ssh/id_rsa.pub
    
    * vim /etc/dropbear/authorized_keys
    
    Add your key and save the file. Then, log out and back in, and if it worked, you won't be asked for a password.

23. Add a CircleCI API token to the environment

    * Edit your profile as in step #21 
    * add export KEY={THE KEY}

24. Create a service start-up script for a Python script

    To have a script automatically start up on system boot, create a script such as the following 

    _Tip: place your Python script in `/root` so it can be started up even if the SD card has not finished initializing_

    * vim /etc/init.d/circleci
    
    Example script:
    
    ```bash
    #!/bin/sh /etc/rc.common
 
SCRIPT_NAME="Build Status"
SCRIPT_PATH="/root/circleci6.py $KEY"
LOG_FILE="/tmp/circleci.log"
START=99
STOP=10
 
start() {       
        echo "Starting $SCRIPT_NAME"
        $SCRIPT_PATH >> $LOG_FILE 2>&1 &
}                
 
stop() {         
        echo "Stopping $SCRIPT_NAME"
        killall -9 `basename $SCRIPT_PATH`
}
```
    * chmod +x /etc/init.d/circleci

    Enable or disable the automatic start up with:
    
    * /etc/init.d/circcleci enable
    * /etc/init.d/circcleci disable
    
    When enabled, new start up and shutdown scripts can be seen in /etc/rc.d such as:
    
    ```K10circleci -> ../init.d/circleci```
    ```S99circleci -> ../init.d/circleci```

    Now you can start and stop the service by using:
    
    * /etc/init.d/circleci start
    * /etc/init.d/circleci stop
    * /etc/init.d/circleci restart

    _Notes:_
    
    * The START and STOP variables specify where in the start up and shutdown process this script is handled. The higher the number, the later in the process the script is handled.

#### Links
