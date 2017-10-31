import sys
import platform

platform = platform.system()
hostname = "nullable"
domain = "nightmare.haus"
static_ip = "0.0.0.0"
motd = """
        <your motd here>
        """
port_config = {}
port_config['ssh'] = 22


def main():
    get_args()
    print(platform)
    print(hostname+ "." + domain)
    print(static_ip)
    print(motd)

def get_args():
    if (len(sys.argv) <= 1):
        print("You haven't supplied a hostname.")
        print("Please supply at minimum a hosntame.")
        print("Ags: Hostname, Static IP")
        sys.exit(0)
    else:
        hostname = sys.argv[1]





main()

