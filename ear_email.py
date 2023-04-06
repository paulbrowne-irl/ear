import logging
import os.path
import shutil
from pandas.core.frame import DataFrame

import win32com.client
import pandas as pd

from openpyxl import Workbook
from openpyxl import load_workbook

import settings

## Module level variables


'''
Walk folder recursively
'''
def walk_folder(data_frame,parent_folder,this_folder):
    

    # Walk and print folders
    for folder in this_folder.Folders:
        print (folder.Name)
        
        #Do recursive call to walk sub folder
        data_frame = walk_folder(data_frame,parent_folder+"::"+folder.Name,folder)

    #Print folder items
    folderItems = this_folder.Items
 
    for mail in folderItems:

        #for debugging
        print("DF size:"+str(data_frame.size))
        if(data_frame.size>settings.BREAK_AFTER_X_FIELDS):
            print("Breaking ...")
            return data_frame

        #Filter on mail items only
        if(mail.Class!=43):
            print("Skipping item type:"+str(mail.Class))

        else:
           
            new_row = {'Parent':parent_folder,
                       'Subject':mail.Subject,
                       'To':mail.To,
                       'CC':mail.CC,
                       'Recipients':""+str(mail.Recipients),
                       'RecievedByName':mail.ReceivedByName,
                       'ConversationTopic':mail.ConversationTopic,
                       'ConversationID':mail.ConversationID,
                       'Sender':mail.Sender,
                       'SenderName':mail.SenderName,
                       'SenderEmailAddress':mail.SenderEmailAddress,
                       'attachments.Count':mail.attachments.Count,
                       'Size':mail.Size,
                       'MessageClass':""+str(mail.MessageClass),
                       'ConversationIndex':mail.ConversationIndex,
                       'EntryID':mail.EntryID,
                       'Parent':""+str(mail.Parent),
                       'CreationTime':""+str(mail.CreationTime),
                       'ReceivedTime':""+str(mail.ReceivedTime),
                       'LastModificationTime':""+str(mail.LastModificationTime),
                       'Body':mail.Body,
                       'Categories':mail.Categories
                       
                     }
            
            data_frame= data_frame.append(new_row,ignore_index=True)
            
           # data_frame.append(new_row, )


            #
            #HTMLBody
            #RTFBody


    return data_frame
           
        

'''
Output from Outlook Into Excel
'''
def export_email_to_excel(OUTLOOK):
    
    
    #debugging
    #root_folder = .Folders.Item(1)
    print("Getting handle to outlook");
    root_folder = OUTLOOK.Folders.Item(settings.INBOX_NAME)

    #Create data frame
    df = pd.DataFrame()

    #Walk folders
    print("About to walk folder");
    new_data = walk_folder(df,"",root_folder)

    #Print a sample of the data
    print(new_data)

    
    #Save the new data
    new_data.to_excel(settings.EMAIL_REPORT_FILE)




