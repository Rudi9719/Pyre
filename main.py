import sys, os, platform
from uuid import uuid4


'''
    Config Section!
'''
## SHARED
# Should updates be run?
run_update = True

# Setup the first user
user1_uname = "gregory"
user1_pw = str(uuid4())
user1_fname = "Gregory"
user1_lname = "Rudolph"

# Hostname (PC Name on Windows)
hostname = "nullable"
# Domain
domain = "nightmare.haus"
# Workgroup
workgroup = "NIGHTMARES"

# Assign a Static IP
static_ip = "0.0.0.0"



# The following options are specifically for *nix
# Set the root PW
root_pw = str(uuid4())
# SSH Banner, displayed before login
banner = """
###############################################################
#                   Welcome to {}\t\t      # 
#      All connections are monitored and recorded             #
#                                                             #
#  Disconnect IMMEDIATELY if you are not an authorized user!  #
###############################################################
        """

#MoTD displayed after login
motd = """
    Welcome to {}.{}
    System is: {}
    IP is: {}
    
"""


# Port configuration
port_config = {}
port_config['ssh'] = 22

# Programs to be installed during update phase ONLY IF UPDATES=TRUE
installables = ["mysql", "python3", "telnet"]


platform = platform.system()

'''
PLEASE DO NOT EDIT BELOW THIS LINE
-----This----is----a-----line---------
'''


def main():
    global motd, banner
    get_args()
    print(platform + " Detected.")
    print(static_ip + " Requested.")
    print("Banner:")
    banner = banner.format(domain)
    print(banner)
    print("Motd:")
    motd = motd.format(hostname, domain, platform, static_ip)
    print(motd)
    set_greetings()
    update_install()

def add_user1():
    if "Windows" in platform:
        pass
    elif "Linux" in platform:
        pass
    elif "Darwin" in platform:
        pass

def update_install():
    if (run_update):
        if "Darwin" in platform:
            print("Darwin detected, installing homebrew!")
            os.system("/usr/bin/ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"")
            for item in installables:
                os.system("sudo -u {} brew install {}".format(user1_uname, item))
        elif "Linux" in platform:
            print("Linux detected, using APT!")
            os.system("apt update")
            for item in installables:
                os.system("apt install " + item)
            os.system("apt upgrade")
        elif "Windows" in platform:
            print("Not sure how to do this..")
    else:
        print("Run updates was false, skipping.")

def set_greetings():
    global motd, banner
    if "Windows" in platform:
        pass
    else:
        motd_f = open("/etc/motd", "w")
        motd_f.write(motd)
        banner_f = open("/etc/banner", "w")
        banner_f.write(banner)
        motd_f = open("/etc/motd")
        banner_f = open("/etc/banner")
        os.system("echo Banner /etc/banner >> /etc/ssh/sshd_config")
        if motd in motd_f.read():
            print("MoTD Set Sucessfully")
        else:
            print("Error setting MoTD")
        if banner in banner_f.read():
            print("Banner set Successfully")
        else:
            print("Error setting Banner")

        sshd_conf = open("/etc/ssh/sshd_config")
        if "Banner /etc/banner" in sshd_conf.read():
            print("Banner config detected!")


def get_args():
    global hostname
    global static_ip
    if (len(sys.argv) == 1):
        print("You haven't supplied a hostname.")
        print("Please supply at minimum a hosntame.")
        print("You must specify domain, motd and banner in the config section.")
        print("Ags: Hostname, Static IP")
        sys.exit(0)
    elif (len(sys.argv) == 2):
        hostname = sys.argv[1]
    elif (len(sys.argv) == 3):
        hostname = sys.argv[1]
        static_ip = sys.argv[2]








main()

