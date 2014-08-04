import re
from easygui_labcuro import buttonbox, multenterbox, multpasswordbox

def multipleinput(msg, title, fieldNames, password = False, dir_validation = False, fieldValues = "", verification = True):
    print 1
    #USE PARWORD FOR LAST INPUT OR NOT
    if password == True:
        
        fieldValues = multpasswordbox(msg, title, fieldNames, fieldValues)
        print 'capture'
        print fieldValues
    else: 
        fieldValues = multenterbox(msg, title, fieldNames, fieldValues)

    while 1:
        if fieldValues == None: 
            break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": 
            break # no problems found
        
        if password == 'yes':
            #print 'capture_second'
            #print fieldValues
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
        else:
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
        print 'while' 
        print fieldValues

    #CHECK VALIDITY OF INPUT - dir_validation
    if dir_validation == True:
        while 1:
            errors = [False, False]
            arr = [fieldValues[1], fieldValues[2]]
            cnt = 0
            for e in arr:
                try: 
                    float(e)
                except ValueError:
                    errors[cnt] = True
                cnt += 1
            error_msg = ['Only integers are allowed for "Days to delete local files", try again',
                         'Only integers are allowed for "Days to delete network drive files", try again',
                         'Only integers are allowed for "Hours between backup", try again']
            cnt = 0
            errors_msg_out = []
            for error in errors:
                if  error == True:
                    errors_msg_out.append(error_msg[cnt])
                cnt += 1
            if len(errors_msg_out) > 0:
                errmsg = '\n'.join(errors_msg_out)
                fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
                print 'errors'        
                print fieldValues
                
            else:
                break # no problems found, break while loop
                    
    fieldict = dict(zip(fieldNames, fieldValues))
    if password == True:
        fieldict.pop('Password', None)   
    verif_fields = ""
    for e in fieldict: 
        field = e + ': %s\n' % fieldict[e] 
        verif_fields = ''.join([verif_fields, field])
    if verification:
        #VERIFY INFORMATION
        msg = ('These are the attributes you selected\n\n'+ verif_fields)
        title = "LabCuro v3.0"
        btnchoices = ["Yes", "No"]
        verification = buttonbox(msg=msg, title=title, choices=btnchoices, image=None)
        if verification == "Yes":
            #trim and remove spaces from instrument ID and service
            for i in range(0,1):
                var = str(fieldValues[i])
                var = var.strip()
                var = re.sub(r'[^\w\d,\t\n\r\f\v\s]',"_",var, re.S)  
        else:
            
            
            
            multipleinput(msg, title, fieldNames, password, dir_validation, fieldValues)
    
    print 'final'        
    print fieldValues
    return fieldValues