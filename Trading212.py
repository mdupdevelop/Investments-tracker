import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import pandas as pd
from bs4 import BeautifulSoup


# account credentials
username = ""
password = ""
#preparation for future csv file
data=[]
# Connect to mail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
(retcode, capabilities) = mail.login(username,password )
mail.list()
mail.select('inbox')



n=0
(retcode, messages) = mail.search(None, '(FROM "noreply@trading212.com" UNSEEN)')
if retcode == 'OK':
   for num in messages[0].split() :
        print ('Processing email')
        n=n+1
        typ, data = mail.fetch(num,'(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])
                From, encoding = decode_header(original["From"])[0]
                if isinstance(From , bytes):
                    # if it's a bytes, decode to str
                    From = From.decode(encoding)
                    print("From retrieved")
                else:
                    From = original['From']
                    print("From retrieved")
                subject, encoding = decode_header(original["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                    print("Subject retrieved")
                else:
                    subject = (original['SUBJECT'])
                    print("Subject retrieved")

                if ((From == 'Trading 212 <noreply@trading212.com>') and (subject == 'Contract Note Statement from Trading 212')): #Emails from Trading212 official adress and subject
                    # multipart body, not a text/plain text
                    if original.is_multipart():
                        # iterate over email parts
                        print("Message is multipart")
                        for part in original.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                                print("Body of email retrieved")
                            except:
                                pass
                            if content_type == "text/html" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                soup = BeautifulSoup(body,'html.parser') 
                                #Names of columns in statement
                                header_list = []
                                header = soup.find_all("thead")[0].find_all("th")
                                for element in header:
                                    try:
                                        header_list.append(element.get_text())
                                    except:
                                        continue
                                #first and last item of header list is ''
                                header_list.pop(0)
                                header_list.pop()
                                print("Email header processed")
                                #Data assigned to columns
                                HTML_data = soup.find_all("tbody")[2].find_all("tr")[1:] 
                                totalcontent= []
                                for element in HTML_data:
                                    content_list = []
                                    #Each tr contains td with cells
                                    for subelement in element:
                                        try:
                                            inside = subelement.get_text().strip()
                                            if inside == '':
                                                continue
                                            else:
                                                content_list.append(inside)
                                        except:
                                            continue
                                    if content_list:
                                        totalcontent.append(content_list)
                                        print("Email body processed")

                                # Storing the data into Pandas 
                                # DataFrame  
                                originalDF = pd.read_csv('Trading212Trades.csv')
                                T212InfoDF = pd.DataFrame(totalcontent, columns = header_list) 
                                originalDF = originalDF.append(T212InfoDF)
                                originalDF.to_csv('Test.csv', index=False)      
                                print("New CSV exported")         
                else: mail.store(num, '-FLAGS', '\Seen')   # Set other emails back to Unread









