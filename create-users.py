#!/usr/bin/pyton3

# INET4031 
#Anas Liban
# Date Created: December 5th, 2025
# Last Modified: December 5th, 2025

# os lets us run system commands like adduser/passwd
# re lets us check if a line starts with "#" (so we can skip commented lines)
# sys allows the script to read from create-users.input using stdin
import os
import re
import sys

def main():

    # Read each line of the input file one at a time
    for line in sys.stdin:

        # If the line starts with "#", it's a comment, so skip it
        match = re.match("^#", line)

        # Split the line by ":" so we can separate username, password, etc.
        fields = line.strip().split(':')

        # If it’s commented OR doesn’t have all 5 fields, ignore it
        if match or len(fields) != 5:
            continue

        # Pull the parts of the user info out of the fields
        username = fields[0]                     # username we will create
        password = fields[1]                     # password for user
        gecos = "%s %s,,," % (fields[3], fields[2]) # full name format used in Linux

        # A user can be in multiple groups, separated by commas
        groups = fields[4].split(',')


        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        print(cmd)     # Dry Run: only print
        os.system(cmd)  # Real run happens in Step 5

        print(f"==> Setting password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        print(cmd)     # Dry Run: only print
        os.system(cmd)

        # Add user to assigned groups unless group is "-"
        for group in groups:
            if group != "-":
                print(f"==> Adding {username} to {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                print(cmd)     # Dry Run: only print
                os.system(cmd)

if __name__ == "__main__":
    main()

