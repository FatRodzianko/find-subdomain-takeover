# find-subdomain-takeover
Python script to discover possible subdomain takeover through CNAME records

Written in deprecated Python2. If you want this in Python3 do it yourself because I am far too lazy to re-write this and I don't care. There is a much better tool for this called [subjack](https://github.com/haccer/subjack). It's written in go and I have no idea how to use go, so I wrote this shoddy python script for myself.

This script has a lot of debug output that I do not plan on removing. It also runs pretty slowly if you have a large list of subdomains, since it makes 1 dns request at a time. If this doesn't work for you, consider modifying the script

Checks for the following subdomain takeover scenarios:
* cname doesn't exist
* s3 bucket doesn't exist
* azure website doesn't exist
* github.io
* herokudns
* readme.io

All of this is based on this blog post here: [https://0xpatrik.com/subdomain-takeover-candidates/](https://0xpatrik.com/subdomain-takeover-candidates/)

This script will not perform a takeover for you. You will need to figure that out. This will only point out subdomains that you may be able to takeover. There will likely be false positives.

## Usage
```
usage: find-subdomain-takeover.py [-h] --file FILE [--nameserver NAMESERVER]

Find subdomains with CNAME records that can be purchased for subdomain
takeover

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  provide file containing list of subdomains
  --nameserver NAMESERVER, -s NAMESERVER
                        provide IP address of nameserver in x.x.x.x format
```

The file of subdomains should be one subdomain per line. Here is an example of what a list would look like:
```
cat domain-take-over-test.txt 
aws.fatrodzianko.com
azure1.fatrodzianko.com
azure2.fatrodzianko.com
azure3.fatrodzianko.com
doesnotexist.fatrodzianko.com
github.fatrodzianko.com
herokudns.fatrodzianko.com
readme.fatrodzianko.com
subtest.fatrodzianko.com
fake.fatrodzianko.com
fatrodzianko.com
```

If you don't provide a nameserver, it will use 8.8.8.8 by default. I'd suggest you provide the nameserver for the domain you are investigating. If you don't know how to find that, here is an example of finding the name server for fatrodzianko.com:

```
nslookup -type=NS fatrodzianko.com 8.8.8.8
Server:  dns.google
Address:  8.8.8.8

Non-authoritative answer:
fatrodzianko.com        nameserver = ns2.dreamhost.com
fatrodzianko.com        nameserver = ns1.dreamhost.com
fatrodzianko.com        nameserver = ns3.dreamhost.com
```

## Example output
Here is an example of the script being used:
```
python find-subdomain-takeover.py -f domain-take-over-test.txt -s 162.159.26.14
Using nameserver: 162.159.26.14                                                                                                                           
query: aws.fatrodzianko.com.                                                                                                                              
AWS S3 bucket found.fatrodzianko.s3.amazonaws.com                                                                                                         
S3 bucket not found. Possible for takeover                                                                                                                
query: azure1.fatrodzianko.com.                                                                                                                           
Azure site has been found. fatrodzianko.azurewebsites.net                                                                                                 
No DNS record for fatrodzianko.azurewebsites.net possible for subdomain takeover?                                                                         
query: azure2.fatrodzianko.com.                                                                                                                           
Azure site has been found. fatrodzianko.cloudapp.net                                                                                                      
No cname record for azure2.fatrodzianko.com
query: azure3.fatrodzianko.com.
Azure site has been found. fatrodzianko.scm.azurewebsites.net
No DNS record for fatrodzianko.scm.azurewebsites.net possible for subdomain takeover?
query: doesnotexist.fatrodzianko.com.
cname is: fat-doesnotexist-rodzianko.com
No DNS record for fat-doesnotexist-rodzianko.com possible for subdomain takeover?
query: github.fatrodzianko.com.
Github page found. fatrodzianko.github.io
Github page not found. Possible for subdomain takeover
query: herokudns.fatrodzianko.com.
Heroku DNS site found. fatrodzianko.herokudns.com
No DNS record for fatrodzianko.herokudns.com possible for subdomain takeover?
query: readme.fatrodzianko.com.
readme.io site has been found. fatrodzianko.readme.io
The readme.io site does not exist. Possible for subdomain takeover.
query: subtest.fatrodzianko.com.
cname is: fatrodzianko.com
DNS lookup of cname: fatrodzianko.com
CNAME fatrodzianko.com is registered.
No DNS record for fake.fatrodzianko.com
No cname record for fatrodzianko.com
Subdomains for possible takeover:
['fatrodzianko.s3.amazonaws.com', 'fatrodzianko.azurewebsites.net', 'fatrodzianko.scm.azurewebsites.net', 'fat-doesnotexist-rodzianko.com', 'fatrodzianko.github.io', 'fatrodzianko.herokudns.com', 'fatrodzianko.readme.io']
```
