#!/usr/bin/env python3

import os
import PhotoScan
import sys
#sys.path.append('/Users/uqmgonz1/Documents/GitHub')
#sys.path.append('/media/pearl/3d_ltmp/scripts/')
#from reef3D.PyToolbox import PStools as pt
#from reef3D.PyToolbox import PSmodel as pm
import pickle
import csv
#from importlib import reload  # Python 3.4+ only.


######################
## Job scheduler #####
######################
def runNetwork(proj_path,  argstring, tname='RunScript', PSscript='scripts/reef3D/PyToolbox/PSmodel.py'):
    ''''
    Run a task over the network
    '''

    client = PhotoScan.NetworkClient()
    # VIDEO_FILENAME=argstring.split(" ")[2]
    # VIDEO_FILENAME=VIDEO_FILENAME.strip('"')
    # doc = PhotoScan.Document(os.path.join(proj_dir,VIDEO_FILENAME + '.psx'))
    # doc.open("...")
    task1 = PhotoScan.NetworkTask()
    task1.name = tname
    task1.params['path'] = PSscript #path to the script to be executed
    task1.params['args'] = argstring #string of the arguments with space as separator
    client.connect('agisoft-qmgr.aims.gov.au') #server ip
    batch_id = client.createBatch(proj_path, [task1])
    client.resumeBatch(batch_id)
    client.disconnect()
    print("Job started...")

##TODO Tidy and test this function. check filepaths (/ vs \). Reorganise data?. <mgr>
###########################################################
## Schedule processing each transect over the network #####\
###########################################################


def batchNet(summary_file, camType, proj_dir='projects', export_path='exports'):
    ''''
    Having images registered in ReefMon from the field, the intention is to batch process
    each transect in a campain and export the data products for QAQC and further analysis
    summary_file: CSV file queried from ReefMon DB inidicating the sample id and path to
    images for each transect in a given campain. proj_dir: directory where projects are
    saved
    '''
        
    with open(os.path.join('data/LTMP/summary_samples',summary_file), newline='', encoding='utf-8') as f:
        lines = csv.reader(f,delimiter=',' )
        line_count = 0
        for line in lines:
            if line_count == 0:
                line_count+=1
            else:
                line_count+=1
                #### Get sample info from database summary ####
                MASTER_SAMPLE_ID,CRUISE_CODE,SITE_NO, TRANSECT_NO,VIDEO_FILENAME = [ line[i] for i in [1,2,6,7,8]]
                SAMPLE_ID=MASTER_SAMPLE_ID+'sc'+TRANSECT_NO
                #### create empty project file #####
                if not os.path.exists(os.path.join(proj_dir,os.path.dirname(VIDEO_FILENAME))):
                    os.makedirs(os.path.join(proj_dir,os.path.dirname(VIDEO_FILENAME)))
        
                PhotoScan.app.console.clear()
                doc = PhotoScan.app.document # construct the document class        
                psxfile = os.path.join(proj_dir,VIDEO_FILENAME + '.psx') # save project
                doc.read_only = False
                doc.save('./'+psxfile)
                print ('>> Processing file: ' + psxfile)
                #
                # VIDEO_FILENAME=VIDEO_FILENAME.replace(" ", "\ ")
                # print(VIDEO_FILENAME)
                
                ### create task job and distrubute to network
                args=" ".join([SAMPLE_ID,camType,'"'+VIDEO_FILENAME+'"', export_path])
                print(args)
                runNetwork(proj_path=psxfile, 
                argstring=args, 
                tname='RunScript', 
                PSscript='scripts/reef3D/PyToolbox/PSmodel.py')
 
###########
## Main ###
###########
'''The following process will only be executed when running script '''
sf= str(sys.argv[1]) # Summary query from ReefMon containing sample id and path to images in a transect
cT= str(sys.argv[2]) # Camera setup from Camera_params.py
pdir= str(sys.argv[3]) # folder name for where projects are stored  
epath=str(sys.argv[4]) # folder name for where data products are exported to.
batchNet(summary_file=sf, camType=cT, proj_dir=pdir, export_path=epath)
