#%%

from imap_tools import MailBox, AND
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os
import matplotlib.pyplot as plt

#%%

# account credentials
username = input('username')
password = input('password')
imap_server = "imaps.bluewin.ch"
imap_port = 993


#%%
# Fetches the emails, and only takes those e-mails that we received after the 24.8.2023, and that are contact requests
# Also prints the folders inside the e-mail account
messages = []
with MailBox(imap_server, port=imap_port).login(username, password) as mailbox:
    for f in mailbox.folder.list():
        print(f)  # FolderInfo(name='INBOX|cats', delim='|', flags=('\\Unmarked', '\\HasChildren'))

    
    for msg in mailbox.fetch(AND(date_gte=datetime.date(2023, 8, 24), subject= 'Contact request')):
        messages.append(msg)
        
        #print(msg.text)
        #print(msg.date, msg.subject, len(msg.text or msg.html))
# %%
# Just some functions to extract different features

def get_text(msg):
    html = msg.html
    
    start_flag = "Message<br/>\r\n"
    end_flag = "To contact the person you can reply to this"
    start_index = html.find(start_flag) + len(start_flag)
    end_index = html.find(end_flag)
    html = html[start_index:end_index]
    soup = BeautifulSoup(html)
    text = soup.get_text()
    return text

def get_email_adress(msg):

    html = msg.html

    prestart_flag = "The contact details of the sender<br/>\r\n    <strong>\r\n"
    start_flag = "<br/>\r\n"
    end_flag = "<br/>\r\n"
    prestart_index = html.find(prestart_flag) + len(prestart_flag)
    start_index = html.find(start_flag, prestart_index) + len(start_flag)
    end_index = html.find(end_flag, start_index)

    email_adress = html[start_index:end_index].strip()
    return email_adress



def get_name(msg):
    subject = msg.subject
    start_index = subject.find('|') + 2
    name = subject[start_index:]
    return name

def classify_occupation(text):
    text = text.lower()
    student_flag = any([el in text for el in ['student', 'studies', 'studium', 'bachelor', 'master', 'uzh', 'eth', 'zhaw', 'zhdk', 'phzh', 'hwz']])
    phd_flag = any([el in text for el in ['phd', 'doktor']])
    intern_flag = any([el in text for el in ['intern', 'internship', 'praktikum', 'praktikant']])

    
    if phd_flag: # if phd term occurs, applicant is most likely a phd student
        return 'phd'

    if student_flag and not phd_flag and not intern_flag:
        return 'student'
    
    if intern_flag and not phd_flag and not student_flag:
        return 'intern'
    return 'student'
    #return ('student ' if student_flag else '') + ('phd ' if phd_flag else '') + ('intern ' if intern_flag else '')


def get_messages_from_mailbox(mailbox_name):

    mailbox_messages = []
    with MailBox(imap_server, port=imap_port).login(username, password, initial_folder=mailbox_name) as mailbox:
        for msg in mailbox.fetch():
            mailbox_messages.append(msg)
    mailbox_df = messages_to_df(mailbox_messages)
    return mailbox_df


# %%
# Generating some features
# Here, we generate a Dataframe that contains different information extracted from the email, such as
# name, length of text, usage of personal adress, occupation
# The uid is the e-mail id, which can be used to move mails to different folders

def messages_to_df(messages):
    df = pd.DataFrame(data={'message': messages})
    df['text'] = df['message'].apply(get_text)
    df['uid'] = df['message'].apply(lambda x: x.uid)
    df['name'] = df['message'].apply(get_name)
    df['personal_adress'] = df['text'].apply(lambda x: 'mirthe' in x.lower())
    df['length'] = df['text'].apply(lambda x: len(x))
    df['occ'] = df['text'].apply(classify_occupation)
    df['email'] = df['message'].apply(get_email_adress)
    df.set_index('uid', inplace=True)
    return df

df = messages_to_df(messages)

# %%
# Picking canditated based on previous generates features
# Feel free to change these criteria
# Of course, they are not exact and only based on what we can read from the messages
manual_excluded = pd.Series([])
manual_included = pd.Series([])

round_1_ind = df.drop_duplicates(subset='name').loc[
    # Person should have mentioned Mirthe's name in the message
    #(df['personal_adress'] == True) 
    # The message should contain at least 1000 characters
    (df['length'] > 1000)  
    # The person should not be an intern or a phd student
    & (df['occ'] == 'student')

    & (~df['name'].isin(manual_excluded))

    | (df['name'].isin(manual_included))
    ].index.to_list()


#%%
# Prints the selected applicants into a text file each, contained in the folder round_1_path
round_1_path = 'round_1'
def print_into(sub, path):
    #print(sub.index)
    with open(os.path.join(path, sub['name']), "w") as text_file:
        text_file.write(sub.text)

for i in round_1_ind:
    print_into(df.loc[i], round_1_path)

#%% 
# Copies the selected applicants into the Round_1 folder inside the email

with MailBox(imap_server, port=imap_port).login(username, password) as mailbox:
    mailbox.copy(round_1_ind, 'Second_chance')

# %%
no_names = []
with MailBox(imap_server, port=imap_port).login(username, password, initial_folder='No') as mailbox:
    for msg in mailbox.fetch():
        name = get_name(msg)
        no_names.append(name)

# %%
# deletes all emails from round 1
def delete_from_folder(folder):
    with MailBox(imap_server, port=imap_port).login(username, password, initial_folder=folder) as mailbox:
        mailbox.delete(mailbox.uids())
delete_from_folder('Round_1')




# %%
