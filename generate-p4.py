#!/usr/bin/env python

import sys, os
import argparse
from subprocess import call

def read_template(filename):
    with open (filename, "r") as code_template:
        data = code_template.readlines()
    return data

def p4_define():
    p4_define = read_template('template/define.p4')
    return p4_define

def ethernet():
    ethernet_hdr = read_template('template/headers/ethernet.p4')
    parse_eth = read_template('template/parsers/parse_ethernet.p4')
    return (ethernet_hdr + parse_eth)

def ipv4():
    ipv4_hdr = read_template('template/headers/ipv4.p4')
    parse_ipv4 = read_template('template/parsers/parse_ipv4.p4')
    return (ipv4_hdr + parse_ipv4)

def tcp():
    tcp_hdr = read_template('template/headers/tcp.p4')
    parse_tcp = read_template('template/parsers/parse_tcp.p4')
    return (tcp_hdr + parse_tcp)

def udp():
    udp_hdr = read_template('template/headers/udp.p4')
    parse_udp = read_template('template/parsers/parse_udp.p4')
    return (udp_hdr + parse_udp)

def forward_table():
    fwd_tbl = read_template('template/tables/forward_table.p4')
    return fwd_tbl

def control():
    ingress = read_template('template/controls/ingress.p4')
    return ingress

def generate_programs(args):
    program_name = 'parser'
    if not os.path.exists(program_name):
       os.makedirs(program_name)

    program = p4_define() + ethernet() + ipv4() + tcp() + udp() + forward_table() + control()

    program_text =  ('').join(program);
    with open ('%s/main.p4' % program_name, 'w') as out:
        out.write(program_text)

    call(['cp', 'template/run_switch.sh', program_name])
    call(['cp', 'template/commands.txt', program_name])


def main():
    parser = argparse.ArgumentParser(description='A programs that generate a set'
                            ' of P4 programs')
    parser.add_argument("-p", "--parser", default=False, action="store_true",
                            help="parser benchmark")
    parser.add_argument("-v", "--vlan", default=False, action='store_true',
                        help="send a VLAN tag packet")

    args = parser.parse_args()

    if args.parser:
        generate_programs(args)
    else:
        parser.print_help()

if __name__=='__main__':
    main()