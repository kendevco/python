import whois
import csv
import pandas as pd

sites = [
    'www.bjc.org',
    'jobs.bjc.org',
    'bjcshines.com',
    'trimybest.com',
    'media.bjc.org',
    'makingsaves.com',
    'makingsaves.net',
    'doctors.bjc.org',
    'altonsurgery.com',
    'mybjcpension.com',
    'altonsurgery.net',
    'mybjcpension.net',
    'www.bjcshines.com',
    'myboonehealth.com',
    'www.trimybest.com',
    'www.trimybest.com',
    'yourbestmedicine.net',
    'onlinepayment.bjc.org',
    'balanceworksbetter.com',
    'makemedicinebetter.com',
    'balanceworksbetter.net',
    'makemedicinebetter.net',
    'classes-events.bjc.org',
    'barnesjewishcollege.com',
    'clinicaldesktop.bjc.org',
    'northwest-healthcare.com',
    'www.balanceworksbetter.com',
    'barnesjewishwestcounty.com',
    'www.givingbarnesjewish.com',
    'www.makemedicinebetter.com',
    'www.balanceworksbetter.net',
    'barnesjewishwestcounty.net',
    'interpreterschedule.bjc.org',
    'midriversfamilyphysicians.com',
    'midriversfamilyphysicians.net',
    'midwestsurgicalspecialists.com',
    'bjccommunityhealthliteracy.net',
    'midwestsurgicalspecialists.net',
    'professionals.barnesjewish.org',
    'bjchealthsolutionsconsultant.com',
    'www.bjchealthsolutionsconsultant.com',
    'www.bjsph.org',
    'bjchcm.carenet.org',
    'fmd.gslbdmz1.bjc.org',
    'ctxremote.carenet.org',
    'slchlabtestguide.bjc.org',
    'bjcstcharlescountyknee.net',
    'bjcagilityemployerportal.com',
    'fmdwustl.gslbdmz.carenet.org',
    'www.bjcstcharlescountyknee.net',
    'www.bjcagilityemployerportal.com'
]
# Prepare CSV file
with open("domain_ownership.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    csv_writer.writerow(["Domain", "Registrar", "Updated Date", "Creation Date", "Expiration Date"])

    for domain in sites:
        try:
            info = whois.whois(domain)
            registrar = info.registrar if info.registrar else "N/A"
            updated_date = info.updated_date.strftime("%Y-%m-%d") if info.updated_date else "N/A"
            creation_date = info.creation_date.strftime("%Y-%m-%d") if info.creation_date else "N/A"
            expiration_date = info.expiration_date.strftime("%Y-%m-%d") if info.expiration_date else "N/A"
            csv_writer.writerow([domain, registrar, updated_date, creation_date, expiration_date])
        except (whois.parser.PywhoisError, AttributeError) as e:
            print(f"Error: Failed to retrieve domain information for {domain}. Error details: {str(e)}")

print("Domain ownership information saved to 'domain_ownership.csv' file.")