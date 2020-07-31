#Scraping File
import requests
import csv                                                             #Csv Genration
import re                                                              #Regular Expresion
from bs4 import BeautifulSoup                                          #For HTML Parsing

def findNumber(str):                                                   #For Validate numbers with "-"
    array=re.findall(r'[0-9\-]',str)
    if array[-1]=="-":
        array.pop()
    return ''.join(array)

def clgInfoPage(url):                                                  #For Parsing each College Information Page


    global cnt       
    clgurl=requests.get(url)
    htmlClgContent=clgurl.content
    clgSoup=BeautifulSoup(htmlClgContent,'html.parser')

    idd                  =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblInstituteCode").getText()
    clgName              =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblInstituteNameEnglish").getText()
    regionClg            =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblRegion").getText()
    Address              =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblAddressEnglish").getText()
    District             =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblDistrict").getText()
    AutoStatus           =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblStatus2").getText()
    totalBoys            =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblBoysTotal").getText()
    totalGirls           =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblGirlsTotal").getText()
    website              =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblWebAddress").getText()
    clgConNo             =findNumber(clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblOfficePhoneNo").getText())
    email                =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblEMailAddress").getText()
    Contact_person_name  =clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish").getText()
    person_No            =findNumber(clgSoup.find('span',id="ctl00_ContentPlaceHolder1_lblPersonalPhoneNo").getText())
    #Check Null Value and Validate Data
    if idd!="" and clgName!=None and regionClg!="" and District!="" and Address!="" and AutoStatus!="" and totalBoys!="" and totalGirls!="" and website!="" and clgConNo!="" and email!="" and Contact_person_name!="" and Contact_person_name!="0" and Contact_person_name!="--" and Contact_person_name!="---"  and Contact_person_name!="" and person_No!="":
        global csv_writer
        csv_writer.writerow([idd,clgName,regionClg,Address,District,AutoStatus ,totalBoys,totalGirls,website,clgConNo,email,Contact_person_name,person_No])
        cnt=cnt+1 
        print(cnt)
        

if __name__ == "__main__":
    
    print("Genrating CSV Please Wait Until End Of Executuion ")
    f= open('DTE Colleges.csv', 'w+')                                           #Create CSV
    csv_writer = csv.writer(f)
    csv_writer.writerow(["ID","College Name","Region","Location","District","Autonomus_Status","Boys_Total","Girls_Total","Website Link","Contact Number","Email Address","Tpo Name","Tpo Contact Number"])  #Genrate Header
    cnt=0
    
    region = ['Amravati', 'Aurangabad', 'Mumbai', 'Nagpur', 'Nashik', 'Pune']
    regionID = 1
    for name in region:
        try:
            URL = ("http://www.dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=" + str(regionID) + "&RegionName=" + name)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            tables = soup.find("table", {"class": "DataGrid"})
            college_tags = tables.findChildren("td")
            i = 3

            #Validate Engineering College
            word1 = "Engineering"
            word2 = "Technology"
            word3 = "Technical"
            word4 = "Technological"
            institute_code = []
            go_to_college_link = []
            while True:
                if (i <= len(college_tags)):
                    name = college_tags[i].text
                    if word1 in name or word2 in name or word3 in name or word4 in name:
                        institute_code.append(college_tags[i - 1])
                else:
                    break
                i = i + 3

            #Append Engineering College link in go_to_college_link URL List
            for institute in institute_code:
                clg_link = institute.find('a', {'href': re.compile("^frm")})
                go_to_college_link.append("http://dtemaharashtra.gov.in/" + clg_link.get('href'))
            
            
            #Traverse go_to_college_link list to scrape each college information page
            for link in go_to_college_link:
                try:
                    clgInfoPage(link)
                except:
                    print("Don't press any key to terminate program")
                    pass
            regionID = regionID + 1   #Change The Region
        except:
            print("Don't press any key to terminate program")
            pass
        
    print("END")
    f.close()
