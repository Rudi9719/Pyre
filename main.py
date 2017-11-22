import sys, os, platform, socket
from uuid import uuid4

'''
    Config Section!
'''
## SHARED
# Setup the first user
user1_uname = "user1"
user1_pw = str(uuid4())
user1_fname = "User"
user1_lname = "One"

# Hostname (PC Name on Windows)
hostname = "nullable"
# Domain
domain = "nightmare.haus"
# Workgroup
workgroup = "NIGHTMARES"

# Networking
interface = "en0"
dhcp = True
static_ip = "0.0.0.0"
gateway = "0.0.0.0"
netmask = "0.0.0.0"
dns1 = "8.8.8.8"
dns2 = "8.8.4.4"

# The following options are specifically for *nix
# Set the root PW
root_pw = str(uuid4())

# SSH Banner, displayed before login
banner = """
###############################################################
#                   Welcome to {}.{}\t\t      # 
#      All connections are monitored and recorded             #
#                                                             #
#  Disconnect IMMEDIATELY if you are not an authorized user!  #
###############################################################
"""

# MoTD displayed after login
motd = """
    Welcome to {}.{}
    System is: {}
    IP is: {}
    
"""

# Determine the running platform
platform = platform.system()

# Port configuration
port_config = {}
port_config['ssh'] = 22

# Programs to be installed during update phase ONLY IF run_update = True
run_update = True

if "Darwin" in platform:
    installables = ["mysql", "python3"]
    cask = ["VirtualBox"]
elif "Linux" in platform:
    installables = ["mysql", "python3", "lightdm", "openssh-server", "gnome"]

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
    banner = banner.format(hostname, domain)
    print(banner)
    print("Motd:")
    motd = motd.format(hostname, domain, platform, static_ip)
    print(motd)

    setup_networking()
    set_greetings()
    update_install()
    add_user1()


def pyre_shell():
    supported_commands = ["uadd", "help", "exit", "quit"]
    print("Type exit to quit.")
    while True:
        command = input("Pyre $ ")
        if command in supported_commands:
            parts = command.split()
            if "uadd" in parts[0]:
                if (len(parts) != 1):
                    global user1_pw, user1_name, user1_uname, user1_lname, user1_fname
                    user1_uname = parts[1]
                    user1_pw = parts[2]
                    user1_fname = parts[3]
                    user1_lname = parts[4]
                    add_user1()
                else:
                    print("uadd $username $password $firstname #lastname")
            elif "help" in parts[0]:
                print("Pyre Shell Commands:")
                print("uadd $username $password $firstname #lastname")
                print("\tAdds a new user.")
            else:
                sys.exit(0)
        elif "python" in command:
            print("You can't open python in python?!")
            sys.exit(0)
        else:
            os.system("{}".format(command))


def setup_networking():
    global dhcp

    if "Linux" in platform:
        iface = open("/etc/network/interfaces", 'a')
        if dhcp:
            iface.write("auto {}".format(interface))
            iface.write("iface {} inet dhcp".format(interface))
        else:
            global static_ip, gateway, dns1, dns2, netmask
            iface.write("auto {}".format(interface))
            iface.write("iface {} inet static".format(interface))
            iface.write("\taddress {}".format(static_ip))
            iface.write("\tnetmask {}".format(netmask))
            iface.write("\tgateway {}".format(gateway))
            iface.write("\tdns-nameservers {} {}".format(dns1, dns2))
        os.system("/etc/init.d/networking restart")
    else:
        print("Networking configuration not yet supported for this platform.")


def add_user1():
    if "Windows" in platform:
        os.system("net user {} {} /add".format(user1_uname, user1_pw))
    elif "Linux" in platform:
        os.system("useradd -m -p {} -s /bin/bash {}".format(str(uuid4()), user1_uname))
        os.system("echo {}:{} | chpasswd".format(user1_uname, user1_pw))
        os.system("echo root:{} | chpasswd".format(root_pw))
        print("Generated Root Password: " + root_pw)
    elif "Darwin" in platform:
        user1_name = "{} {}".format(user1_fname, user1_lname)
        os.system("sudo dscl . -create /Users/{}".format(user1_uname))
        os.system("sudo dscl . -create /Users/{} UserShell /bin/bash".format(user1_uname))
        os.system("sudo dscl . -create /Users/{} RealName \"{}\"".format(user1_uname, user1_name))
        os.system("sudo dscl . -create /Users/{} UniqueID \"1010\"".format(user1_uname))
        os.system("sudo dscl . -create /Users/{} PrimaryGroupID 80".format(user1_uname))
        os.system("sudo dscl . -create /Users/{} NFSHomeDirectory /Users/{}".format(user1_uname, user1_uname))
        os.system("sudo dscl . -passwd /Users/{} {}".format(user1_uname, user1_pw))


def update_install():
    if (run_update):
        if "Darwin" in platform:
            print("Darwin detected, installing homebrew!")
            os.system(
                "sudo -u {} /usr/bin/ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"".format(
                    user1_uname))
            for item in installables:
                os.system("sudo -u {} brew install {}".format(user1_uname, item))
            for item in cask:
                os.system("sudo -u {} brew cask install {}".format(user1_uname, item))
        elif "Linux" in platform:
            print("Linux detected, using APT!")
            os.system("apt update")
            for item in installables:
                os.system("apt -y install " + item)
            os.system("apt -y upgrade")
        elif "Windows" in platform:
            print("Does Windows have a non-interactive package manager?")
    else:
        print("Run updates was false, skipping.")


def set_greetings():
    global motd, banner
    if "Windows" in platform:
        print("Windows does not natively support SSH.. SKIPPING")
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
        print("You must specify domain, motd and banner in the config section.")
        print("Args: Hostname, Static IP")

        print("You haven't supplied a hostname, dropping into Pyre shell.")
        pyre_shell()
    elif (len(sys.argv) == 2):
        hostname = sys.argv[1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        static_ip = s.getsockname()[0]
    elif (len(sys.argv) == 3):
        hostname = sys.argv[1]
        static_ip = sys.argv[2]


main()
