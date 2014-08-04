#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         FlowIt Lab v2.1
# Created:      September 9  2013
# Version:      Version: 2.1
# Copyright:    (c) German Campuzano Zuluaga gcampuzanozuluaga@med.miami.edu 2013
# Version 2.1 changes:
#     1. Adds path for backup: C:\Program Files\BD FACSCanto Software\SetupReports
#     2. Fixes regex for copath and sunquest files
#     3. Modifies global varibles
#-------------------------------------------------------------------------------

import os
import time
import shutil
import re
import easygui

# compile executable: python -O C:\Users\germancz\Dropbox\Programming\Python\APPS\pyinstaller\pyinstaller.py --onefile C:\Users\germancz\Dropbox\Programming\Python\APPS\flow_manager_program\FlowIt v2.1.py

# testdr,colon = "Z:/GERMAN/FlowIt test directory/JTEST_RW/", "" # activate this part to test in Z drive - or other drive

testdr, colon = "", ":"  # activate this part before compiling to run on final machine

# public vars
now = time.time()  # curr time
nowtime = time.ctime()  # curr time as string
nowyr = time.ctime()[-4:]  # curr year
nowday = time.ctime()[8:10]  # curr day
nowmonth = time.ctime()[4:7]  # curr day 
nowhr = time.ctime()[11:19]  # curr hr
month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

version = 2.1
year = 2013
print "FlowCuro Lab  v" + str(version) + " " + str(year) + "\nCopyright: gcampuzanozuluaga@med.miami.edu 2013\n"

# VARS___________________________________
# Log files and directories - machine id
flow_machineid = testdr + "D" + colon + "/BDExport/TECHNICAL_FILE_MANAGER"  # machine id txt file directory
machid_txt = flow_machineid + "/MACHINE ID.txt"  # create text file with machine ID    
if not os.path.exists(flow_machineid):  # check if path for log file exists, else create it
    os.makedirs(flow_machineid)
os.open(machid_txt, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
with open(machid_txt, "r+") as machineid:  # title to text log - runonly once
    titler = machineid.read()
    isnewmachine = titler.rfind("MACHINE ID")
    if isnewmachine == -1:
        machine = raw_input("This is the first time this program runs on this machine. Please assign a name to this machine: ")
        machineid.write("MACHINE ID: " + machine + "\nCREATION DATE: " + nowtime + "\n______________________________________________________\n")    
    else:
        var = "MACHINE ID: "
        stump = titler.find(var) + (len(var))
        ini = titler[stump:]
        search_enter = ini.find('\n')
        machine = (ini[:search_enter])
        print "MACHINE ID: " + machine
# technical and case log
jpth_tech = testdr + "J" + colon + "/TECHNICAL/FILE_ADMIN_LOG/" + machine  # log file directory
txt = jpth_tech + "/FLOW_CASES_LOG_" + machine + "_" + nowyr + ".txt"  # create text case_log file with year of creation
case_log_dir = testdr + "J" + colon + "/TECHNICAL/CASE_LOG"
case_log_tech = case_log_dir + "/TECH_CASE_LOG_" + nowyr + ".txt"  # create text case_log file with year of creation

# Variables for paths on flow cytometer PC
flow_new_expn = testdr + "D" + colon + "/BDExport/Experiments/NEW"
flow_new_exps = testdr + "D" + colon + "/BDExport/Experiments/SENT"
flow_new_fcsn = testdr + "D" + colon + "/BDExport/FCS/NEW"
flow_new_fcss = testdr + "D" + colon + "/BDExport/FCS/SENT"
flow_new_setreportn = testdr + "C" + colon + "/Program Files/BD FACSCanto Software/SetupReports/NEW"
flow_new_setreports = testdr + "C" + colon + "/Program Files/BD FACSCanto Software/SetupReports/SENT"
flow_new_pdfn = testdr + "D" + colon + "/BDExport/REPORTS_PDF/NEW"
flow_new_pdfs = testdr + "D" + colon + "/BDExport/REPORTS_PDF/SENT"

# Variables for paths on J: drive backup
jpth_bckp_exp = testdr + "J" + colon + "/BACKUP/" + machine + "/RAWDATA/EXPERIMENTS"
jpth_bckp_fcs = testdr + "J" + colon + "/BACKUP/" + machine + "/RAWDATA/FCS"
jpth_bckp_setreport = testdr + "J" + colon + "/BACKUP/" + machine + "/RAWDATA/SETUP_REPORTS"
jpth_bckp_pdf_cpath = testdr + "J" + colon + "/BACKUP/" + machine + "/REPORTS_PDF/COPATH"
jpth_bckp_pdf_sq = testdr + "J" + colon + "/BACKUP/" + machine + "/REPORTS_PDF/SUNQUEST"
jpth_bckp_pdf_qc = testdr + "J" + colon + "/BACKUP/" + machine + "/REPORTS_PDF/QC"
jpth_bckp_pdf_rsch = testdr + "J" + colon + "/BACKUP/" + machine + "/REPORTS_PDF/RESEARCH"

# Variables for paths on J: drive clinical
jpth_cln_cpath = testdr + "J" + colon + "/CLINICAL_FLOW/COPATH"
jpth_cln_sq = testdr + "J" + colon + "/CLINICAL_FLOW/SUNQUEST"
jpth_cln_rsch = testdr + "J" + colon + "/CLINICAL_FLOW/RESEARCH"
jpth_cln_qc = testdr + "J" + colon + "/CLINICAL_FLOW/QC"
jpth_cln_cpathold = testdr + "J" + colon + "/CLINICAL_FLOW/COPATH/DONE"
jpth_cln_sqold = testdr + "J" + colon + "/CLINICAL_FLOW/SUNQUEST/DONE"

# REGEX___________________________________
rsrchpatt = re.compile("(.*RXH.*).pdf")  # REGEX RESEARCH cases
qcpatt = re.compile("(.*QCF.*).pdf")  # REGEX QC cases
copthpatt = re.compile("(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s+(\w+\d*)\s+\d+(?=.pdf)")  # REGEX COPATH cases
sunqpatt = re.compile("([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s(\w+\d*)\s+?\d+(?=.pdf)")  # REGEX SUNQUEST cases


def check_case_log ():
    if not os.path.exists(case_log_dir):  # check if path for log file exists, else create it
        os.makedirs(case_log_dir)
    os.open(case_log_tech, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
    with open(case_log_tech, "r+") as log:  # title to text log - run only once
        titler = log.read()
        isnewlog = titler.rfind("FILE_NAME,CASE_ID,CASE_NAME,SAMPLE_MATRIX,PANEL,DATE,HOUR")
        
    if isnewlog == -1:
        with open(case_log_tech, "a") as log:
            log.write("FILE_NAME,CASE_ID,CASE_NAME,SAMPLE_MATRIX,PANEL,DATE,HOUR\n")
            log.close   


def createarch ():
    arr = [flow_new_expn,
           flow_new_exps,
           flow_new_fcsn,
           flow_new_fcss,
           flow_new_setreportn,
           flow_new_setreports,
           flow_new_pdfn,
           flow_new_pdfs,
           
           jpth_bckp_exp,
           jpth_bckp_fcs,
           jpth_bckp_setreport,
           jpth_bckp_pdf_cpath,
           jpth_bckp_pdf_sq,
           jpth_bckp_pdf_qc,
           jpth_bckp_pdf_rsch,
           
           jpth_cln_cpath,
           jpth_cln_sq,
           jpth_cln_rsch,
           jpth_cln_qc,
           jpth_cln_cpathold,
           jpth_cln_sqold,
           jpth_tech]
    
    for e in arr:
        if not os.path.exists(e):  # check if path for log file exists, else create it
            os.makedirs(e)
            print "Path created: " + e
    print "\n"
    
def initial():
    os.open(txt, os.O_RDWR | os.O_CREAT)  # check if file exists, else create it
    with open(txt, "r+") as newlog:  # title to text log - runonly once
        titler = newlog.read()
        isnewlog = titler.rfind("BEGINNING OF FILE HANDLING LOG FOR MACHINE")
        if isnewlog == -1:
            newlog.write("BEGINNING OF FILE HANDLING LOG FOR MACHINE: " + machine + "\nCREATION DATE: " + nowtime + "\n______________________________________________________\n\n")    
    print "Valid file names (for regular expression patterns check FlowIt user manual):\n"\
    + "CoPath: [Accession number w\wo part] [name] [TS, FL, BM or PB] [type of test] [serial number][.pdf]\n"\
    + "Sunquest: [Accession number w\wo part] [name] [TS, FL, BM or PB] [type of test] [serial number][.pdf]\n"\
    + "QC: include [QCF] somewhere in the file name\n"\
    + "RESEARCH: include [RXH] somewhere in the file name"

def cyclecopyraw():  # procedure to copy fcs and experiment files from D to J drive
    arr = [[flow_new_expn, jpth_bckp_exp, flow_new_exps, "EXPERIMENTAL", "----1. EXPERIMENTAL CASES BACKUP----\n"],
        [flow_new_fcsn, jpth_bckp_fcs, flow_new_fcss, "FCS", "----2. FCS CASES BACKUP----\n"],
        [flow_new_setreportn, jpth_bckp_setreport, flow_new_setreports, "SETUP_REPORTS", "----3. SETUP REPORTS BACKUP----\n"]]
    i = 0
    with open(txt, "r+") as oldlog:  # run backup only once a day based on var nowday
        tt = oldlog.read()
        logtoday = "CASE LOG: " + nowtime
        newday = tt.rfind(logtoday)
    print "\n_________________________\n#### CASE LOG: " + nowtime + " ####" + "\n"
    log("\n_________________________\n#### CASE LOG: " + nowtime + " ####")    
    if newday == -1:
        for e in arr:
            mirrorfiles(e[0], e[1], e[2], e[3], e[4])
            i += 1
    else:
        for e in arr:
            print e[4] + "-0 " + e[3] + " cases were BACKED-UP to the J: NETWORK DRIVE.\n"
            log(e[4] + "-0 " + e[3] + " cases were BACKED-UP to the J: NETWORK DRIVE.\n")
            i += 1

def mirrorfiles(src, sharedestination, sentfolder, typecase, n):  # subprocedure called by cyclecopyraw to copy files and test if timedir (tdir) exists 
    cnt = 0
    totcases = len(os.listdir(src))  # src is the NEW cases folder on local D: drive
    for f in os.listdir(src):
        ofi = src + "/" + f
        tcr = time.ctime(os.path.getmtime(ofi))[-4:]  # Date of file to sort in directory by year
        filt = os.stat(ofi).st_mtime  # time for file creation
        agedays = (((now - filt) / 60) / 60) / 24
        tdir = sharedestination + "/" + tcr
        # print agedays
        if agedays > 1:
            if os.path.exists(tdir):
                copydirsfiles(ofi, tdir, sentfolder, f)
                cnt += 1
            else:
                os.mkdir(tdir)
                copydirsfiles(ofi, tdir, sentfolder, f)
                cnt += 1
    case = str(cnt)
    casetot = str(totcases)
    print n + "-A total of " + case + " out of " + casetot + " " + typecase + " cases were BACKED-UP to the J: NETWORK DRIVE.\n"
    log(n + "-A total of " + case + " out of " + casetot + " " + typecase + " cases were BACKED-UP to the J: NETWORK DRIVE.\n")

def copydirsfiles (ofi, tdir, sentfolder, f):  # subprocedure called by mirrorfiles to copy stuff depending if it is a file or a directory 
    dfi = tdir + "/" + f
    now = time.ctime()[-13:-5]
    tcr = now.replace(":", "")
    if os.path.isdir(ofi):  # procedure for a directory
# proc for bckp - DIRECTORIES
        if os.path.exists(dfi):
            dfi = dfi + "_COPY_" + tcr
            shutil.copytree(ofi, dfi, symlinks=False, ignore=None)
        else:
            shutil.copytree(ofi, dfi, symlinks=False, ignore=None)
# proc for LOCAL SENT - DIRECTORIES
        dfi = sentfolder + "/" + f
        if os.path.exists(dfi):
            dfi = dfi + "_COPY_" + tcr
            shutil.copytree(ofi, dfi, symlinks=False, ignore=None)
            shutil.rmtree(ofi)
        else:
            shutil.copytree(ofi, dfi, symlinks=False, ignore=None)
            shutil.rmtree(ofi)
    else:  # procedure for a file
# proc for bckp - FILES
        if os.path.exists(dfi):
            dfi = tdir + "/" + f[:-4] + "_COPY_" + tcr + ".pdf"
            shutil.copy2(ofi, dfi)
        else:
            shutil.copy2(ofi, dfi)
# proc for LOCAL SENT - FILES
        dfi = sentfolder + "/" + f
        if os.path.exists(dfi):
            dfi = sentfolder + "/" + f[:-4] + "_COPY_ " + tcr + ".pdf"
            shutil.move(ofi, dfi)
        else:
            shutil.move(ofi, dfi)

def timefile():  #moves old files to WEEKOLD and deletes year-old files INACTIVE!!!!!!!!!!!!!!!!!!
    dirs = [jpth_cln_cpathold, jpth_cln_sqold, jpth_cln_qc, jpth_cln_rsch]
    tyr = 0
    removedyr = []    
    for di in dirs:
        for f in os.listdir(di):
            fullpath = os.path.join(di, f)
            filt = os.stat(fullpath).st_mtime  # time of file creation
            agedays = (((now - filt) / 60) / 60) / 24
            if agedays > 370:  # eliminate if case is older than a year in WEEK_OLD cases%%%%%%%%%%%%%%%%%%%%%%%%%%370%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if os.path.isdir(f):
                    pass
                else:
                    removedyr.append(f)
                    os.remove(fullpath)
                    tyr = 0    
    print "----4. YEAR-OLD CASES----\n-" + str(tyr) + " cases are >370 days old and have been eliminated from the CLINICAL_FLOW subfolders. CASES: " + str(removedyr) + "\n"
    log("----4. YEAR-OLD CASES----\n-" + str(tyr) + " cases are >370 days old and have been eliminated from the CLINICAL_FLOW subfolders. CASES: " + str(removedyr) + "\n")

def elimsent():
    listcas = []
    i = 0
    arr = [[flow_new_exps, jpth_bckp_exp], [flow_new_fcss, jpth_bckp_fcs], [flow_new_setreports, jpth_bckp_setreport]]
    for e in arr:
        for f in os.listdir(e[0]):
            ofi = e[0] + "/" + f
            filt = os.stat(ofi).st_mtime  # time for file creation%%%%%%%%%%%%%%%%%%%%%%%%%%%90%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            agedays = (((now - filt) / 60) / 60) / 24
            if agedays > 90:
                listcas.append(f)
                tcr = time.ctime(os.path.getmtime(ofi))[-4:]  # Date of file to sort in directory by year
                tdir = e[1] + "/" + tcr
                
                if os.path.exists(tdir + "/" + f):  # file or sub-directory is already in destination backup folder -> it is deleted from source folder
                    if os.path.isdir(ofi):
                        shutil.rmtree(ofi)
                    else:
                        os.remove(ofi)
                    i += 1
                elif os.path.exists(tdir):  # directory exists but file or sub-directory is not there -> copy file/directory 
                    # from source and then deleted from source folder
                    dst = tdir + "/" + f
                    if os.path.isdir(ofi):
                        shutil.copytree(ofi, dst, symlinks=False, ignore=None)
                        shutil.rmtree(ofi)
                    else:
                        shutil.copy2(ofi, dst)
                        os.remove(ofi)
                    i += 1
                else:  # directory for backup by year does not exists -> create backup dir,  copy file/directory 
                    # from source and then deleted from source folder
                    os.makedirs(tdir)
                    dst = tdir + "/" + f
                    if os.path.isdir(ofi):
                        shutil.copytree(ofi, dst, symlinks=False, ignore=None)
                        shutil.rmtree(ofi)
                    else:
                        shutil.copy2(ofi, dst)
                        os.remove(ofi)
                    i += 1
         # BACKUP CASES__________________________
    arr = [[rsrchpatt, jpth_bckp_pdf_rsch], [qcpatt, jpth_bckp_pdf_qc],
    [copthpatt, jpth_bckp_pdf_cpath], [sunqpatt, jpth_bckp_pdf_sq]]

    for e in arr:
        files = []
        for f in  os.listdir(flow_new_pdfs):
            if re.match(e[0], f):
                files.append(f)
        for f in files:
            ofi = flow_new_pdfs + "/" + f
            filt = os.stat(ofi).st_mtime  # time for file creation%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%90%%%%%%%%%%%%%%%%%%%%%%%%%%
            agedays = (((now - filt) / 60) / 60) / 24
            if agedays > 90:
                listcas.append(f)
                tcr = time.ctime(os.path.getmtime(ofi))[-4:]  # Date of file to sort in directory by year
                tdir = e[1] + "/" + tcr
                
                if os.path.exists(tdir + "/" + f):  # file or sub-directory is already in destination backup folder -> it is deleted from source folder
                    if os.path.isdir(ofi):
                        pass
                    else:
                        os.remove(ofi)
                    i += 1
                elif os.path.exists(tdir):  # directory exists but file or sub-directory is not there -> copy file/directory 
                    # from source and then deleted from source folder
                    dst = tdir + "/" + f
                    if os.path.isdir(ofi):
                        pass
                    else:
                        shutil.copy2(ofi, dst)
                        os.remove(ofi)
                    i += 1
                else:  # directory for backup by year does not exists -> create backup dir,  copy file/directory 
                    # from source and then deleted from source folder
                    os.makedirs(tdir)
                    dst = tdir + "/" + f
                    if os.path.isdir(ofi):
                        pass
                    else:
                        shutil.copy2(ofi, dst)
                        os.remove(ofi)
                    i += 1
        
        
        
        pi = str(i)
     
    log ("----5. OLD FILES ON LOCAL D: OR C: DRIVE----\n""-" + pi + " cases were >90 day old and were eliminated from the LOCAL DRIVE - CASES: " + str(listcas) + " \n")
    print "----5. OLD FILES ON LOCAL D: OR C: DRIVE----\n""-" + pi + " cases were >90 day old and were eliminated from the LOCAL DRIVE - CASES: " + str(listcas) + " \n"

def match(end=None, to_open=None, nomatch=None, add=None, tot=None, caselog=None):
    countin = 0
    if end == 1:
        msg = ("There are clinical cases in the LOCAL drive that do not meet the required naming convention and were not transfered to the NETWORK drive."
        "Please fix the names for the program to continue.\n CASES: " + str(nomatch))
        title = "Flow cytometry case manager"
        choice = easygui.ccbox(msg, title)
        if choice == 1:
            pass
        else:
            easygui.msgbox("This application will end but you must fix the files and re-run the program. These are clinical samples.")
            
            for e in to_open:
                time.sleep(0.3)
                os.startfile(e)
                
            log("----6. CLINICAL CASES BACKUP AND CLINICAL_FLOW TRANSFER----\n-Cases transfered: " + str(add) + " out of " + str(tot)\
            + ". CASES: " + str(caselog) + "\n-Not transfered: " + str(len(nomatch)) + " cases had INVALID file names. CASES: " + str(nomatch) + " THE PROGRAM WAS CANCELED AND CLINICAL CASES WERE LEFT IN THE LOCAL DRIVE\n_________________________\n")

            print "----6. CLINICAL CASES BACKUP AND CLINICAL_FLOW TRANSFER----\n-Cases transfered: " + str(add) + " out of " + str(tot)\
            + ". CASES: " + str(caselog) + "\n-Not transfered: " + str(len(nomatch)) + " cases had INVALID file names. CASES: " + str(nomatch) + " THE PROGRAM WAS CANCELED AND CLINICAL CASES WERE LEFT IN THE LOCAL DRIVE\n_________________________\n" 
            return
    else:
        to_open = []
    
    if caselog:
        pass
    else:
        caselog = []  # list to store cases that dont match the REGEX and are not transfered to C_FLOW subdirectories
    tot = len(os.listdir(flow_new_pdfn))  # Number of cases in the source directory with the PDFs to be transfered
    add = 0
    
    for e in os.listdir(flow_new_pdfn):
        src = flow_new_pdfn + "/" + e  # source file to transfer
        arr = [[rsrchpatt, jpth_cln_rsch, jpth_bckp_pdf_rsch, "RXH"], [qcpatt, jpth_cln_qc, jpth_bckp_pdf_qc, "QCF"],
              [copthpatt, jpth_cln_cpath, jpth_bckp_pdf_cpath, "COPATH"], [sunqpatt, jpth_cln_sq, jpth_bckp_pdf_sq, "SUNQUEST"]]
        for f in arr:
            test = 0
            # copy to clinical_flow subfolders
            
            if f[0].match(e):  # regex to match cases and copy them to clinical folder
                # print "YES " + str(e)
                dst = f[1] + "/" + e
                regex_id = f[0]
                file_name = f[0].match(e)
                if re.compile(f[0]).groups > 1:
                    print re.compile(f[0]).groups
                    print file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4)
                    acces_num, name, matrix, test_type = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4)
                    # print acces_num, name, matrix, test_type
                shutil.copy2(src, dst)
                to_open.append(dst)
                tcr = time.ctime(os.path.getmtime(src))[-4:]  # Date of file to sort in directory by year
                tdir = f[2] + "/" + tcr
                if os.path.exists(tdir):  # create directory by year if it does not exist
                    dst = tdir + "/" + e
                else:
                    os.makedirs(tdir)
                    dst = tdir + "/" + e
                
                shutil.copy2(src, dst)
                
            else:
                # print "NO " + str(e) + str(f[0])
                test = -1
                
            if test != -1:
                add += 1
                dst = flow_new_pdfs + "/" + e
                caselog.append(f[3] + ": " + e)
                
                if f[3] == "COPATH" or f[3] == "SUNQUEST":
                    case_log(e, acces_num, name, matrix, test_type)
                
                shutil.move(src, dst)
                break

    nomatch = os.listdir(flow_new_pdfn)
    if len(nomatch) > 0:
        os.startfile(flow_new_pdfn)
        match(1, to_open, nomatch, add, tot, caselog)
    else:
        for e in to_open:
            time.sleep(0.3)
            os.startfile(e)
            
        log("----6. CLINICAL CASES BACKUP AND CLINICAL_FLOW TRANSFER----\n-Cases transfered: " + str(add) + " out of " + str(tot)\
        + ". CASES: " + str(caselog) + "\n-Not transfered: " + str(len(nomatch)) + " cases had INVALID file names. CASES: " + str(nomatch) + "\n_________________________\n")

        print "----6. CLINICAL CASES BACKUP AND CLINICAL_FLOW TRANSFER----\n-Cases transfered: " + str(add) + " out of " + str(tot)\
        + ". CASES: " + str(caselog) + "\n-Not transfered: " + str(len(nomatch)) + " cases had INVALID file names. CASES: " + str(nomatch) + "\n_________________________\n" 
    
def log(e):
    with open(txt, "a") as log:
        log.write(e + "\n")
        log.close
        
def case_log(e, casenum, casename, matrix, typeflow):
    
    date = str(month[nowmonth]) + "/" + str(nowday) + "/" + str(nowyr)

    os.open(case_log_tech, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
    with open(case_log_tech, "r+") as log:  # title to text log - runonly once
        titler = log.read()
        isnewlog = titler.rfind(e)
        
    if isnewlog == -1:
        with open(case_log_tech, "a") as log:
            log.write(str(e) + "," + str(casenum) + "," + str(casename) + "," + str(matrix) + "," + str(typeflow) + "," + str(date) + "," + str(nowhr) + "\n")
            log.close     
               
check_case_log ()
createarch()    
initial()
cyclecopyraw()
timefile()
elimsent()
match()
os.system("pause")
