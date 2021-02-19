import dns.resolver
import argparse
import requests

### Reference for how to perform some of these subdomain takeovers, especially for cloud providers:
### https://0xpatrik.com/takeover-proofs/

parser = argparse.ArgumentParser(description="Find subdomains with CNAME records that can be purchased for subdomain takeover")

parser.add_argument("--file", "-f", type=str, required=True, help="provide file containing list of subdomains")
parser.add_argument("--nameserver", "-s", type=str, required=False, default="8.8.8.8",help="provide IP address of nameserver in x.x.x.x format")
args = parser.parse_args()

f = open(args.file,'r')
s = args.nameserver
nameserver = [s]
subdomains = f.readlines()

print "Using nameserver: " + s
cnames = []
takeover = []
for subdomain in subdomains:
        #Make a DNS query for each subdomain looking for a CNAME record
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = nameserver
            dnsAnswer = resolver.query(subdomain.strip(), 'CNAME')
            print "query: " + str(dnsAnswer.qname)
            for cname in dnsAnswer:
                if "\\009" in str(cname.target)[:-1]:
                    newcname = str(cname.target)[:-1].replace("\\009","")
                else:
                    newcname = str(cname.target)[:-1]
                #Check if the CNAME record is an S3 bucket
                s3_buckets = ["s3","amazonaws.com"]
                #if "s3.amazonaws.com" in newcname:
                if any(x in newcname for x in s3_buckets):
                    print "AWS S3 bucket found." + newcname
                    try:
                        s3response = requests.get("http://"+newcname)
                        bucket_not_found = ["bucket does not exist","NoSuchBucket"]
                        #if "bucket does not exist" in s3response.text:
                        if any(x in s3response.text for x in bucket_not_found):
                            print "S3 bucket not found. Possible for takeover"
                            takeover.append(newcname)
                            continue
                        else:
                            continue
                    except:
                        continue
                #Check if the CNAME is a github.io page
                elif "github.io" in newcname:
                    print "Github page found. " + newcname
                    try:
                        githubresponse = requests.get("https://"+newcname)
                        if githubresponse.status_code == 404:
                            print "Github page not found. Possible for subdomain takeover"
                            takeover.append(newcname)
                            continue
                        else:
                            continue
                    except:
                        continue
                #Check if the CNAME is a HerokuDNS domainsite:
                elif "herokudns.com" in newcname:
                    print "Heroku DNS site found. " + newcname
                    try:
                        herukuAnswer = resolver.query(newcname)
                        print "DNS lookup of cname: " + newcname
                        for answer in herukuAnswer:
                            print "CNAME " + newcname + " is registered."
                    except dns.resolver.NXDOMAIN:
                        print "No DNS record for " + newcname + " possible for subdomain takeover?"
                        takeover.append(newcname)
                    except dns.resolver.DNSException:
                        print "Unhandled DNS exception"
                    except:
                        print "Second dns lookup for " + newcname + " failed?"
                #check if the CNAME is a readme.io site
                elif "readme.io" in newcname:
                    print "readme.io site has been found. " + newcname
                    try:
                        readmeresponse = requests.get("https://"+newcname)
                        if readmeresponse.status_code == 404:
                            print "The readme.io site does not exist. Possible for subdomain takeover."
                            takeover.append(newcname)
                            continue
                        else:
                            continue
                    except:
                        continue
                # Check if the CNAME is an AZURE site
                elif ("azurewebsites.net" in newcname) or ("cloudapp.net" in newcname) or ("scm.azurewebsites.net" in newcname):
                    print "Azure site has been found. " + newcname
                    try:
                        azureAnswer = resolver.query(newcname)
                        print "DNS lookup of Azure CNAME: " + newcname
                        for answer in azureAnswer:
                            print "CNAME " + newcname+ " is registered."
                            continue
                    except dns.resolver.NXDOMAIN:
                            print "No DNS record for " + newcname + " possible for subdomain takeover?"
                            #takeover.appened(newcname)
                            takeover.append(newcname)

                            continue
                    except dns.resolver.DNSException:
                        print "Unhandled DNS exception"
                        continue
                    except:
                        print "Second dns lookup for Azure site " + newcname + " failed?"
                        continue
                #Verify that the CNAME is a base domain. If it is not a base domain, check to see if the base domain is registered.
                elif newcname.count('.') > 1:
                    print "CNAME " + newcname + " is not a base domain. Check to see if the base domain is available."
                    base = newcname.split(".")
                    basedomain = ".".join(base[-2:])
                    try:
                        baseAnswer=dns.resolver.query(basedomain)
                        for answer in baseAnswer:
                            print "The base domain " + basedomain + " is not available."
                            continue
                    except dns.resolver.NXDOMAIN:
                        print "No DNS record for the base domain " + basedomain +". Possible for subdomain takeover."
                        takeover.append(basedomain)
                        continue
                    except:
                        print "Second DNS lookup for " + basedomain + " failed."
                        continue
                #If none of the above triggers, make DNS request for the CNAME record to see if it exists.
                #An NXDOMAIN response indicates that it MIGHT be vulnerable to subdomain takeover
                else:
                    print 'cname is: ' + newcname
                    cnames.append(newcname)
                    try:
                        cnameAnswer = dns.resolver.query(newcname)
                        print "DNS lookup of cname: " + newcname
                        for answer in cnameAnswer:
                            print "CNAME " + newcname + " is registered."
                    except dns.resolver.NXDOMAIN:
                        print "No DNS record for " + newcname + " possible for subdomain takeover?"
                        takeover.append(newcname)
                    except dns.resolver.DNSException:
                        print "Unhandled DNS exception"
                    except:
                        print "Second dns lookup for " + newcname + " failed?"
        except dns.resolver.NXDOMAIN:
            print "No DNS record for " + subdomain.strip()
        except:
            print 'No cname record for ' + subdomain.strip()

print "Subdomains for possible takeover:\n" , takeover
