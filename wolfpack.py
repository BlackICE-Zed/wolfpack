#!/usr/bin/python3
import subprocess
import argparse
import socket
import os

def main():
    # Verify root privileges
    if os.geteuid() != 0:
        print("Please run as root.")
        exit(1)

    # Read arguments
    flagRead = argparse.ArgumentParser()
    flagRead.add_argument('-t','--target',type=str,help="Specify target IP",metavar='target IP',required=True)
    flagRead.add_argument('-lf','--listfile',type=str,help="Specify wordlists from a file",metavar='filename',required=True)
    flagRead.add_argument('-o','--outputdirectory',type=str,help="Where to store the output files (will NOT verify write rights)",metavar='path to dir',required=True)
    flagRead.add_argument('-v','--version',action='version',version='Wolfpack v0.1.0 (Early)',help="Print out Wolfpack version")

    flagSet = flagRead.parse_args()

    # Setup flags
    if flagSet.target:
        targetIP = flagSet.target
    if flagSet.listfile:
        try:
            with open(flagSet.listfile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if "wfuzz_list" in line:
                        parts = line.split('=')
                        wfuzzList = parts[1].strip()
                    elif "ffuf_list" in line:
                        parts = line.split('=')
                        ffufList = parts[1].strip()
        except FileNotFoundError:
            print("Wordlist file not found")
            exit(1)
        except IOError as e:
            print(f"Error reading wordlist file: {e}")
            exit(1)
    if flagSet.outputdirectory:
        outDir = flagSet.outputdirectory
    nmapComm = "sudo nmap -p- -sC -oA portscan"
    
    # Verify flags before the attack
    print(f'----------------------WOLFPACK----------------------\n')
    print(f'Verify the flags below:\n')
    print(f'Target IP: {targetIP}')
    print(f'Nmap command: {nmapComm} {targetIP}\n')
    print(f'wfuzz wordlist: {wfuzzList}')
    print(f'ffuf wordlist: {ffufList}\n')
    print(f'Path to store results: {outDir}\n')
    ans = input(f'Commence the attack? [Y/n]: ')
    if ans == 'Y' or ans == 'y' or ans == '\n' or ans == '':
        conf = True
    else:
        conf = False
    if conf == False:
        print("Aborted")
        exit(0)
    print("Attack")
    
    # Nmap scan
    print("Starting nmap container...\n")
    subprocess.run(["sudo", "docker", "build", "-t", "wolfa", "./port-scan"])
    subprocess.run(["sudo", "docker", "run", "--name", "nmap-cont", "-it", "wolfa", "/app/port-entrypoint.sh", targetIP, "portscan"])
    subprocess.run(["sudo", "docker", "cp", "nmap-cont:/app/portscan.nmap", outDir])
    subprocess.run(["sudo", "docker", "cp", "nmap-cont:/app/portscan.gnmap", outDir])
    subprocess.run(["sudo", "docker", "cp", "nmap-cont:/app/portscan.xml", outDir])
    subprocess.run(["sudo", "docker", "rm", "nmap-cont"])
    print("Nmap scan complete\n")

    # Resolve hostname from next scans
    try:
        targetHost = socket.gethostbyaddr(targetIP)[0]
        
        # Wfuzz scan
        print("Starting wfuzz container...\n")
        subprocess.run(["sudo", "docker", "build", "-t", "wolfb", "./dir-scan"])
        subprocess.run(["sudo", "docker", "run", "--name", "wfuzz-cont", "-it", "wolfb", "/app/dir-entrypoint.sh", targetHost+"/FUZZ", wfuzzList])
        subprocess.run(["sudo", "docker", "cp", "wfuzz-cont:/app/dirscan.txt", outDir])
        subprocess.run(["sudo", "docker", "rm", "wfuzz-cont"])
        print("Wfuzz scan complete\n")
        
        # Ffuf scan
        print("Starting ffuf container...\n")
        subprocess.run(["sudo", "docker", "build", "-t", "wolfc", "./dns-scan"])
        subprocess.run(["sudo", "docker", "run", "--name", "ffuf-cont", "-it", "wolfc", "/app/dns-entrypoint.sh", "FUZZ."+targetHost, ffufList])
        subprocess.run(["sudo", "docker", "cp", "ffuf-cont:/app/dnsscan.txt", outDir])
        subprocess.run(["sudo", "docker", "rm", "ffuf-cont"])
        print("Ffuf scan complete\n")
    except socket.herror:
        print("Hostname failed to resolve\nWill proceed with wfuzz scan, but not with ffuf scan\n")
        
        # Wfuzz scan
        print("Starting wfuzz container (with IP as parameter)...\n")
        subprocess.run(["sudo", "docker", "build", "-t", "wolfb", "./dir-scan"])
        subprocess.run(["sudo", "docker", "run", "--name", "wfuzz-cont", "-it", "wolfb", "/app/dir-entrypoint.sh", targetIP+"/FUZZ", wfuzzList])
        subprocess.run(["sudo", "docker", "cp", "wfuzz-cont:/app/dirscan.txt", outDir])
        subprocess.run(["sudo", "docker", "rm", "wfuzz-cont"])
        print("Wfuzz scan complete\n")
        


if __name__ == "__main__":
    main()