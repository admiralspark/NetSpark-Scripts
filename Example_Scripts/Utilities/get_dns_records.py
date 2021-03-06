#!/usr/bin/env python
# -*- coding utf-8 -*-
#
# Copyright 2016 Akshay Raj Gollahalli
# STILL BROKEN

import dns.resolver


def get_records(domain):
    """
    Get all the records associated to domain parameter.
    :param domain:
    :return:
    """
    ids = [
        'NONE',
        'A',
        'NS',
        'MD',
        'MF',
        'CNAME',
        'SOA',
        'MB',
        'MG',
        'MR',
        'NULL',
        'WKS',
        'PTR',
        'HINFO',
        'MINFO',
        'MX',
        'TXT',
        'RP',
        'AFSDB',
        'X25',
        'ISDN',
        'RT',
        'NSAP',
        'NSAP-PTR',
        'SIG',
        'KEY',
        'PX',
        'GPOS',
        'AAAA',
        'LOC',
        'NXT',
        'SRV',
        'NAPTR',
        'KX',
        'CERT',
        'A6',
        'DNAME',
        'OPT',
        'APL',
        'DS',
        'SSHFP',
        'IPSECKEY',
        'RRSIG',
        'NSEC',
        'DNSKEY',
        'DHCID',
        'NSEC3',
        'NSEC3PARAM',
        'TLSA',
        'HIP',
        'CDS',
        'CDNSKEY',
        'CSYNC',
        'SPF',
        'UNSPEC',
        'EUI48',
        'EUI64',
        'TKEY',
        'TSIG',
        'IXFR',
        'AXFR',
        'MAILB',
        'MAILA',
        'ANY',
        'URI',
        'CAA',
        'TA',
        'DLV',
    ]

    google_resolver = dns.resolver.Resolver()
    google_resolver.nameservers = ['8.8.8.8']

    for a in ids:
        try:
            answers = google_resolver.query(domain, a)
            for rdata in answers:
                print(a, ':', rdata.to_text())

        except Exception as e:
            print(e)  # or pass

if __name__ == '__main__':
    DOMAIN = input("Url: ")
    get_records(DOMAIN)
