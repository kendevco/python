import requests

API_URL = "https://zlx31990.live.dynatrace.com/api/v1/synthetic/monitors"
API_KEY = "dt0c01.DF2ZFTMNGC4RLKAUBZPSBQCF.IG3WW2V7FQMLWFKYFX7CMC6EEHKFE6NVKUH5ZZ42MSAUMTIHYYIOAJBGXC77VBPA"
websites = [
    "http://EpicValidation.carenet.org",
    "http://RehabAudiology.carenet.org",
    "http://highlands.carenet.org",
    "http://cohprimarymed.carenet.org",
    "http://cohgi.carenet.org",
    "http://cohminorprocedure.carenet.org",
    "http://cohobgyn.carenet.org",
    "http://cohpsychiatry.carenet.org",
    "http://cohspecialtycare.carenet.org",
    "http://cohwoundcenter.carenet.org",
    "http://cohpainmanagement.carenet.org",
    "http://hits.carenet.org",
    "http://echomasterprovidermaintenance.carenet.org/",
    "http://doclookup.carenet.org/",
    "https://mdmdatamaintenance.carenet.org/",
    "https://preventableharmmaintenance.carenet.org/",
    "https://paymentrequests.carenet.org/",
    "https://psdata.carenet.org/",
    "https://CAMSouthCountySignin.carenet.org",
    "https://Telemetry.carenet.org",
    "https://badgephoto.carenet.org/",
    "http://InjuryReport.carenet.org",
    "http://LeaderConnect.carenet.org",
    "http://Ptools.carenet.org",
    "http://SLCHPedNutriManual.carenet.org ",
    "http://SLCHRefPhy.carenet.org",
    "http://MDX.carenet.org",
    "http://Mosby.carenet.org",
    "http://www.BJHHandHygiene.org",
    "https://BJHRestraints.carenet.org",
    "https://bjhicusurvey.carenet.org",
    "http://pmweb/failedmedicaldevice/Startup.aspx",
    "http://IPObservations.carenet.org",
    "http://PSQ.carenet.org",
    "http://Clin-Eng-Web.carenet.org",
    "http://CorporatehealthServices.carenet.org ",
    "http://SLCHOPPE.carenet.org",
    "http://WebCheck.carenet.org",
    "http://OHServices.carenet.org",
    "http://CernerQC.carenet.org",
    "http://InterpreterSchedule.bjc.org",
    "http://BJHVisioncenter.carenet.org",
    "https://QualityChecksv2.carenet.org",
    "http://PreventableHarm.carenet.org",
    "http://CSCCOPLabSignin.carenet.org",
    "http://SLCHSOCIALWORK.carenet.org",
    "http://Media.bjc.org",
    "http://psycho-oncologydb.carenet.org",
    "http://druginfofiles.carenet.org",
    "http://MSOInitialApplication.carenet.org",
    "http://echomasterproviderservice.carenet.org",
    "http://MDMData.carenet.org",
    "http://BJHCSR.carenet.org",
    "http://Ebook.carenet.org",
    "http://webcheckservice.carenet.org",
    "http://DLA20.carenet.org",
    "http://RehabEfficiencyDB.carenet.org",
    "http://webchecknew.carenet.org",
    "http://CPCISTL.carenet.org",
    "http://BJCPassport.carenet.org",
    "http://CommunityEdEvents.carenet.org",
    "http://HRA.carenet.org",
    "http://PHRED.carenet.org",
    "http://SLCHRehabEfficiency.carenet.org",
    "http://HealthyKidsHealthyMinds.carenet.org",
    "http://BJCHost.carenet.org",
    "http://schooloutreach.carenet.org",
    "http://slchfrcstats.carenet.org",
    "http://trservice.carenet.org",
    "http://WUPassport.carenet.org",
    "http://BJCCal.carenet.org",
    "http://cochlear.carenet.org",
    "http://bjcapprovalsystem.carenet.org",
    "http://SLCHOpLabSignIn.carenet.org",
    "http://soariandowntime.carenet.org",
    "http://BJCNotification.carenet.org",
    "http://CHNEhits.carenet.org",
    "http://DoNotSolicit.carenet.org",
    "http://SLCHLabTestGuide.bjc.org",
    "http://wuepicvalidation.carenet.org",
    "https://abacus.carenet.org/",
    "http://hitsimportlog.carenet.org/"
            ]

headers = {
    "Authorization": f"Api-Token {API_KEY}",
    "Content-Type": "application/json"
}

for website in websites:
    trimmed_website = website.replace("http://", "").replace("https://", "")
    monitor_name = f"Internal - {trimmed_website}"
    monitor_data = {
        "type": "HTTP",
        "name": monitor_name,
        "frequencyMin": 5,
        "locations": ["SYNTHETIC_LOCATION-1CFF19B8B4F46823"], # Update with the location entity ID
        "script": {
            "version": "1.0",
            "requests": [
                {
                    "method": "GET",
                    "url": website,
                    "description": f"GET {trimmed_website}",
                }
            ],
        },
        "enabled": True,
    }

    response = requests.post(API_URL, json=monitor_data, headers=headers)
    if response.status_code == 200:
        print(f"Monitor created for {website}: {response.text}")
    else:
        print(f"Error creating monitor for {website}: {response.text}")