import dns.resolver
import dns.exception

domain = input('Enter domain name: ').strip()

record_types = ('A', 'AAAA', 'CNAME', 'NS', 'MX')

for rtype in record_types:
    print('---', rtype, 'records ---')
    try:
        answers = dns.resolver.resolve(domain, rtype)
        for rdata in answers:
            print(rdata.to_text())
    except dns.resolver.NoAnswer:
        print('No', rtype, 'record found.')
    except dns.exception.DNSException as e:
        print('Error:', e)
        break
