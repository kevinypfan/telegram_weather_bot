# telegram bot Xanonymous
import requests as req
import json 

def getDATA(locationName,usr_require):
    #get user require's api_id from db
    #select the part of need
    global maindata
    dataid='F-C0032-001'#臺灣各縣市天氣預報資料及國際都市天氣預報(36hr)
    url=('https://opendata.cwb.gov.tw/api/v1/rest/datastore/{}?Authorization={}&locationName={}'.format(dataid,'CWB-E0647ADC-96D1-4831-84BF-FAD066C7AEFA',locationName))
    maindata=json.loads(req.get(url).text)['records']['location'][0]['weatherElement']
    # data split
    Wx=(maindata[0]['time'][0:usr_require[0]])
    PoP=(maindata[1]['time'][0:usr_require[1]])
    MinT=(maindata[2]['time'][0:usr_require[2]])
    Cl=(maindata[3]['time'][0:usr_require[3]])
    MaxT=(maindata[4]['time'][0:usr_require[4]])
    return [Wx,PoP,MinT,Cl,MaxT]
#getDATA(locationName,AuthorizationKey,[2,2,2,2,2])#    <<<==  get data here

