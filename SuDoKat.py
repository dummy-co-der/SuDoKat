import argparse
import urllib
import os
import dns.resolver
from termcolor import colored


print(colored("""
						                 //\ 
               						        //  \ 
					                       //     \ 
					                      //        \ 
					                     //          \     ______
					                    //            \   (      )
 ____        ____        _  __     _	                   ||  	           \  | @    |
/ ___| _   _|  _ \  ___ | |/ /__ _| |_	       	   /_______||_______________\_\______|________
\___ \| | | | | | |/ _ \| ' // _` | __|            \      /|__________________/       \      /
___) || |_| | |_| | (_) | . \ (_| | |                    (                             |____/
|____/ \__,_|____/ \___/|_|\_\__,_|\__|                   \_________________/          |
			       		                   ||              /\   d3vil  |
						            \      	  / |          |
			~ Anuj 			             \          /   |__________|
		       Maheshwari		              \       /     |__________|  
                                                               \    /      /            \ 
                                                                \/        /              |
                                                                         |       /\      |
                                                                         |      /  \     |
                                                                         |     |   |     |
                                                                         |     |   |     |
                                                                         |     |   |     |
                                                                         |     |   |     |
                                                                         |____|     |____|
                                                                        /     |    /     |
                                                                       (______|   (______| 
""", 'yellow', attrs=['bold', 'dark']))

print('\n')


def logical_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file \u001b[31m%s\u001b[0m does not exist!" % arg)
    else:
        return open(arg, 'r')


def standard_wordlist():
    url = 'https://raw.githubusercontent.com/dummy-co-der/SuDoKat/main/wordlist.txt'
    print(
        f'[+] \u001b[33m '+ colored('Default Wordlist is: ', 'red', attrs=['bold', 'dark'])+ str(url)+'\u001b[0m \n')

    def_array = []
    response = urllib.request.urlopen(url)

    for line in response:
        decoded_line = line.decode("utf-8").replace('\n', '')
        def_array.append(decoded_line)

    return def_array


def verbose_mode_check(args, sub, domain):
    if args.verbose:
        print(f'[-] {sub}.{domain} \u001b[31m'+ colored('Invalid', 'red', attrs=['bold', 'dark'])+'\u001b[0m')


def more_mode_check(args, ip_value):
    if args.more:
        #print('\t\t |-', colored(ip_value.rrset.to_text().replace('\n', '\n\t\t |- '), 'red'))
        ex=ip_value.rrset.to_text().replace('\n', '\n\t\t |- ')
        #print(ex)
        #for i in s:
        s = ex.split(' ')
        print('\t\t\t|-\t', end = "") 
        for i in s:
        	print(i, end = "\t")
        print('\n')


parser = argparse.ArgumentParser(
    description='\u001b[36m pjrtjhri hgoirthigh  rthoirj r ihtiwg opr yu4 rth<wh  \u001b[0m')

parser.add_argument('Dom',
                    metavar='Domain',
                    type=str,
                    help='Domain Name of the Taget [ex : example.com]')
parser.add_argument('--wordlist', '-w',
                    nargs='?',
                    help='Local wordlist path',
                    metavar="FILE",
                    type=lambda x: logical_file(parser, x))
parser.add_argument('--verbose', '-v',
                    help="Increase Output Verbosity",
                    action='store_true')
parser.add_argument('--more', '-m',
                    help="Display more information about the Taget",
                    action='store_true')

args = parser.parse_args()

domain = args.Dom
wordlist_file = args.wordlist

sub_array = []

wordlist_array = wordlist_file.read().splitlines(
) if wordlist_file else standard_wordlist()

print('[+] \u001b[36m '+ colored('Enumerating subdomains :','blue',attrs=['bold', 'dark'] ) +'\u001b[0m')

for sub in wordlist_array:
    try:
        ip_value = dns.resolver.resolve(f'{sub}.{domain}', 'A')

        if ip_value:
            sub_array.append(f'{sub}.{domain}')
            if f"{sub}.{domain}" in sub_array:
                print(f'\t• {sub}.{domain} \u001b[32m' + colored("Valid", "green",attrs=['bold', 'dark']) + '\u001b[0m')
                more_mode_check(args, ip_value)
        else:
            verbose_mode_check(args, sub, domain)
    except dns.resolver.NXDOMAIN:
        verbose_mode_check(args, sub, domain)
    except dns.resolver.NoAnswer:
        verbose_mode_check(args, sub, domain)
    except KeyboardInterrupt:
        quit()


print(
    f'[+] \u001b[36m '+ colored('Total Unique Subdomains Found: ','blue',attrs=['bold','dark']) + str(len(sub_array)) +'\u001b[0m')
