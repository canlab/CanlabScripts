#!/usr/bin/env python

import requests
import zipfile
import json
import io, os
import sys
import re 

# from https://api.qualtrics.com/docs/getting-survey-responses-via-the-new-export-apis

def exportSurvey(apiToken, surveyId, dataCenter, fileFormat, savePath):

    surveyId = surveyId
    fileFormat = fileFormat
    dataCenter = dataCenter
    savePath = savePath

    # setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }

    # step 1: creating data export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["progressId"]
    print(downloadRequestResponse.text)

    # step 2: checking on data export progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed":
        print ("progressStatus=", progressStatus)
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")
        progressStatus = requestCheckResponse.json()["result"]["status"]

    # step 2.1: check for error
    if progressStatus is "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]

    # step 3: downloading file
    requestDownloadUrl = baseUrl + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # step 4: unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(savePath+"MyQualtricsDownload")
    print('Complete')

def main():

    try:
        apiToken = os.environ['Q_API_TOKEN']
        dataCenter = os.environ['Q_DATA_CENTER']
    except KeyError:
        print("set environment variables Q_API_TOKEN and Q_DATA_CENTER")
        sys.exit(2)

    try:
        surveyId = sys.argv[1]
        fileFormat = sys.argv[2]
        savePath = sys.argv[3]
    except IndexError:
        print ("usage: ./script surveyId fileFormat savePath")
        sys.exit(2)

    if fileFormat not in ["csv", "tsv", "spss"]:
        print ('fileFormat must be either csv, tsv, or spss')
        sys.exit(2)

    r = re.compile('^SV_.*')
    m = r.match(surveyId)
    if not m:
        print ("Survey Id must match ^SV_.*")
        sys.exit(2)

    exportSurvey(apiToken, surveyId, dataCenter, fileFormat, savePath)

if __name__== "__main__":
    main()
