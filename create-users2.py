#!/usr/bin/python3

# INET4031 - Automated User Creation Script (with Dry-Run option)
# Author: Anas Liban

import os
import re

def main():
    # Ask if we should only show commands or really run them
    answer = input("Run in dry-run mode? (Y/N): ").strip().upper()
    dry_run = (answer == "Y")

    # Open the input file with the list of users
    try:
        f = open("create-users.input")
    except FileNotFoundError:
        print("Error: create-users.input not found in this folder.")
        return

    # Go through each line of the file
    for line in f:
        # Check if the line is a comment
        is_comment = re.match("^#", line)

        # Break the line into pieces
        fields = line.strip().split(':')

        if dry_run:
            # In dry run, show why we skip lines
            if is_comment:
                print("DRY RUN: skipping commented line:", line.strip())
                continue
            if len(fields) != 5:
                print("DRY RUN: skipping bad line (needs 5 fields):", line.strip())
                continue
        else:
            # In real run, just skip bad or commented lines quietly
            if is_comment or len(fields) != 5:
                continue

        # Get user info from the fields
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        # Create the user account
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"

        if dry_run:
            print("DRY RUN would run:", cmd)
        else:
            print(cmd)
            os.system(cmd)

        # Set the user password
        print(f"==> Setting password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | sudo passwd {username}"

        if dry_run:
            print("DRY RUN would run:", cmd)
        else:
            print(cmd)
            os.system(cmd)

        # Add the user to groups
        for group in groups:
            if group != "-":
                print(f"==> Adding {username} to {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"

                if dry_run:
                    print("DRY RUN would run:", cmd)
                else:
                    print(cmd)
                    os.system(cmd)

    f.close()

if __name__ == "__main__":
    main()
