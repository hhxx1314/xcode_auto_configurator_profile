#The MIT License (MIT)
#
#Copyright (c) 2016 Jinyu Yu
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#!/usr/bin/python


from mod_pbxproj import XcodeProject
import sys
import json

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print json

class Configuration:
    def __init__(self,jsonFileName):
        self.jsonFileName = jsonFileName
        #find config name
        self.name = jsonFileName.split(".")[0].lower()
        
        #load json data
        with open(jsonFileName) as data_file:
            self.jsonContent = json.load(data_file)


#if len(sys.argv) < 2:
#raise Exception("need project.pbxproj file path")


#read the file path
filePath = sys.argv[1]

if len(sys.argv) > 2:
    jsonFiles = list(sys.argv)
    del jsonFiles[0:2]
else:
    jsonFiles = ["profile.json"]

#print "jsonFiles"

#create configuration objects
dictOfConfig = dict();
for file in jsonFiles:
    config = Configuration(file)
    dictOfConfig[config.name] = config

#load project file and create a backup
project = XcodeProject.Load(filePath)
project.backup()

rootObject = project["rootObject"]

projectObject = project["objects"][rootObject]["targets"]


buildConfigurationLists = []
for id in projectObject:
    buildConfigurationList = project["objects"][id]["buildConfigurationList"]
    buildConfigurationLists.append(buildConfigurationList)

buildListsArr = []
for key in buildConfigurationLists:
    #print  project["objects"][key]["buildConfigurations"]
    buildListsArr = buildListsArr + project["objects"][key]["buildConfigurations"]

#print buildListsArr

for key in buildListsArr:
    version =  project["objects"][key]["name"].lower()
    if version == "release" and  project["objects"][key]["buildSettings"]:
        buildSettingsArr = project["objects"][key]["buildSettings"]
        bundle_id = buildSettingsArr["PRODUCT_BUNDLE_IDENTIFIER"]
        print bundle_id
        if bundle_id is not None:
            if dictOfConfig["profile"].jsonContent.has_key(bundle_id):
                print dictOfConfig["profile"].jsonContent[bundle_id]
                b = dictOfConfig["profile"].jsonContent[bundle_id]
                param = json.loads(b)
                buildSettingsArr["PROVISIONING_PROFILE"] = param["PROVISIONING_PROFILE"]
                buildSettingsArr["CODE_SIGN_IDENTITY"] = dictOfConfig["profile"].jsonContent["CODE_SIGN_IDENTITY"]
                buildSettingsArr["CODE_SIGN_IDENTITY[sdk=iphoneos*]"] = dictOfConfig["profile"].jsonContent["CODE_SIGN_IDENTITY[sdk=iphoneos*]"]
                if buildSettingsArr.has_key("PROVISIONING_PROFILE_SPECIFIER"):
                    buildSettingsArr["PROVISIONING_PROFILE_SPECIFIER"] = param["PROVISIONING_PROFILE_SPECIFIER"]
                    buildSettingsArr["DEVELOPMENT_TEAM"] = dictOfConfig["profile"].jsonContent["DEVELOPMENT_TEAM"]


    print "-------"

project.save()

print "Auto Configuration Complete"
