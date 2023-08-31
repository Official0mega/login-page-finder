#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Use it at your own risk. Author will not be responsible for any damage!

import argparse
import sys
from sys import stdout
from signal import signal, getsignal, SIGINT
from urllib.request import Request, urlopen, URLError, HTTPError

DESCRIPTION = 'Login page finder script'
AUTHOR = 'Author: Omer Ramić <@sp_omer>'
VERSION = '0.2f'
UA = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64) Gecko/20071127 Firefox/2.0.0.11'}
TIMEOUT = 30

class FindLoginPage():
    def __init__(self, domain, sub_links, number_of_sub_links):
        self.domain = domain
        self.sub_links = sub_links
        self.number_of_sub_links = number_of_sub_links
        self.sub_link_counter = 0
        self.valid_links = []

    def check(self):
        for sub_link in self.sub_links:
            if not sub_link:
                break
            try:
                full_link = self.domain + '/' + sub_link.strip()
                request_link = Request(full_link, headers=UA)
                self.sub_link_counter += 1
                stdout.write("\r" + "Nr. of checked links: %s/%s" % (self.sub_link_counter, self.number_of_sub_links))
                stdout.flush()
                response = urlopen(request_link, timeout=TIMEOUT)
            except HTTPError:
                pass
            except URLError:
                pass
            else:
                self.valid_links.append(full_link)

        stdout.write("\n\n" + "Number of valid links found: %s\n" % len(self.valid_links))

def load_data(full_domain):
    print("\n" + DESCRIPTION + " #v" + VERSION + "\n  " + AUTHOR + "\n")
    try:
        with open('linkovi.txt', 'r') as file:
            sub_links = file.readlines()
            sub_link_count = len(sub_links)

        domain_request = Request(full_domain, headers=UA)
        open_link = urlopen(domain_request, timeout=TIMEOUT)
        findloginpage = FindLoginPage(full_domain, sub_links, sub_link_count)
        findloginpage.check()
        return findloginpage.valid_links
    except URLError:
        print("\nCheck entered domain name:", full_domain, "doesn't exist.\n")
        return []
    except HTTPError as greska:
        print("\nPage not found. Error nr.:", greska.code)
        return []
    except IOError:
        print("Error: file can't be opened, check if file 'linkovi.txt' exist.")
        return []
    except KeyboardInterrupt:
        print("You hit control-c")

def exit_gracefully(signum, frame):
    signal(SIGINT, original_sigint)
    try:
        if input("\n\nReally exit? (y/n)> ").lower().startswith('y'):
            exit(1)
    except KeyboardInterrupt:
        print("\n\nOk ok, exiting")
        exit(1)

    signal(SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = getsignal(SIGINT)
    signal(SIGINT, exit_gracefully)
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=AUTHOR)
    parser.add_argument("-u", "--url", dest="URL", help="Target URL (e.g. \"http://www.target.com\")", required=True)
    args = parser.parse_args()
    if args.URL:
        valid_links = load_data(args.URL if args.URL.startswith("http") else "http://%s" % args.URL)
        with open('login_details.txt', 'w') as output_file:
            for link in valid_links:
                output_file.write(link + '\n')
        print("Results written to login_details.txt")
    else:
        parser.print_help()
