'''
Author : Arfat Bin Amer
'''
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import re, json
# create BeautifulSoup object
parsed_html = BeautifulSoup(open("path to your sample test.html"), "html.parser")
''' All the Regex pattern for extracting data in it'''
name_pattern = 'Name[ ]{0,}'
email_pattern = '[\w\.-]+@[\w\.-]+'
phone_pattern = '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'
beds_pattern = 'Beds[ ]{0,}'
baths_pattern = 'Baths[ ]{0,}'
address_patterns = r'\s*([0-9]*)((NW|SW|SE|NE|S|N|E|W))?(.*)((NW|SW|SE|NE|S|N|E|W))?((#|APT|BSMT|BLDG|DEPT|FL|FRNT|HNGR|KEY|LBBY|LOT|LOWR|OFC|PH|PIER|REAR|RM|SIDE|SLIP|SPC|STOP|STE|TRLR|UNIT|UPPR|\,)[^,]*)(\,)([\s\w]*)'

# lead_name will have lead name which will get through the tag which contains Name in it.
lead_name = ''.join([t.parent.find('strong').text for t in parsed_html.findAll(text=re.compile(name_pattern))])

# email_list will have all the emails prsent in the page
email_list = parsed_html.findAll(text=re.compile(email_pattern))
for i in email_list:
    if '@email.realtor.com' not in i: # Exclude the unwanted or known email that not required. 
        email = i
phone_list = parsed_html.findAll(text=re.compile(phone_pattern)) # get all phone numbers list
phone_list = list(dict.fromkeys(phone_list)) # remove the duplicate numbers if exsits
phone = ''.join(list(filter(lambda a: a not in ('(623) 252-1424','(800) 878-4166'), phone_list))) # remove known or unwanted numbers
beds = ''.join([t.parent.find('strong').text for t in parsed_html.findAll(text=re.compile(beds_pattern))]) # beds will get number of beds through the tag which contains Beds in it. 
baths = ''.join([t.parent.find('strong').text for t in parsed_html.findAll(text=re.compile(baths_pattern))]) # beds will get number of baths through the tag which contains Baths in it. 
address_list = parsed_html.findAll(text=re.compile(address_patterns)) # get all the address_patterns present in the page.
for i in address_list:
    if re.match(address_patterns+'\n',i+'\n'):
        address = i								# get actual address from that
# create final output_json
output_json = {
   "name":lead_name,
   "email":email,
   "phone": phone,
   "beds":beds,
   "baths":baths,
   "address":address
   }
#print(output_json)

# write the output_json into output.json file in same folder.
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)