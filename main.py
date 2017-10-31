import sys, os, platform

from uuid import uuid4


## SHARED
# Should updates be run?
run_update = True

# Setup the first user
user1_uname = "newuser"
user1_pw = str(uuid4())
user1_fname = "John"
user1_lname = "Doe"

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
installables = ["openssh-server", "apache2", "nmap", "gnome3", "" ]


platform = platform.system()


## PLEASE DO NOT EDIT BELOW THIS LINE
#-----This----is----a-----line---------

def main():
    get_args()
    print(platform)
    print(static_ip)
    print(banner.format(domain))
    print(motd.format(hostname, domain, platform, static_ip))



def get_args():
    global hostname
    global static_ip
    if (len(sys.argv) == 1):
        print("You haven't supplied a hostname.")
        print("Please supply at minimum a hosntame.")
        print("You must specify domain and motd in the config section.")
        print("Ags: Hostname, Static IP")
        sys.exit(0)
    elif (len(sys.argv) == 2):
        hostname = sys.argv[1]
    elif (len(sys.argv) == 3):
        hostname = sys.argv[1]
        static_ip = sys.argv[2]








main()

