# coding: utf-8

import whois

domain = whois.query('jessemillar.com')

print(domain.__dict__)