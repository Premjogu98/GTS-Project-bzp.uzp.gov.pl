# This Python file uses the following encoding: utf-8
import time
from datetime import datetime
import Global_var
import sys, os
import urllib.request
import urllib.parse
import re
import string
import time
import requests
import html
from Insert_On_Datbase import create_filename,insert_in_Local
import wx
app = wx.App()

# def Translate_close(text_without_translate):
#     a1 = 0
#     while a1 == 0:
#         try:
#             String2 = str(text_without_translate)
#             url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#             a = 0
#             while a == 0:
#                 try:
#                     r = requests.get(url)
#                     a = 1
#                     text = r.text
#                     text = html.unescape(str(text)).strip()
#                     trans_data = text.partition('<div dir="ltr" class="t0">')[2].partition("</div>")[0].strip()
#                     trans_data = html.unescape(str(trans_data)).strip()
#                     remove_tag = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
#                     trans_data = re.sub(remove_tag, '', trans_data).strip()
#                     return trans_data
#                 except:
#                     print('Trying TO Connection')
#                     String2 = str(text_without_translate)
#                     String2 = urllib.parse.quote(String2)
#                     # print(String2)
#                     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
#                     url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#                     headers = {'User-Agent': user_agent, }
#                     request = urllib.request.Request(url, None, headers)  # The assembled request
#                     time.sleep(2)
#                     response = urllib.request.urlopen(request)
#                     htmldata: str = response.read().decode('utf-8')  # The data u need
#                     trans_data = re.search(r'(?<=dir="ltr" class="t0">).*?(?=</div>)', htmldata).group(0)
#                     trans_data = re.sub(' +', ' ', str(trans_data))
#                     a = 0
#                     return trans_data
#         except Exception as e:
#             a1 = 0
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
#                   "\n", exc_tb.tb_lineno)
#             time.sleep(5)


def Scraping_data(get_htmlSource, browser,purchaser,reference_number,Title,Tender_id):
    a = False
    while a == False:
        try:
            SegField = []
            for data in range(45):
                SegField.append('')
            # Email
            Email = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_email">')[2].partition("</span>")[0].strip()
            Email_regex = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]+)", Email)
            if len(Email_regex) != 0:
                SegField[1] = str(Email_regex[0])

            # Address
            zamawiajacy_nazwa = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_nazwa">')[2].partition('<span id="ctl00_ContentPlaceHolder1_regon">')[0].strip().replace('</span>','')
            regon = get_htmlSource.partition('ctl00_ContentPlaceHolder1_regon">')[2].partition('</span>')[0].strip()
            zamawiajacy_adres_ulica = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_adres_ulica">')[2].partition('</span>')[0].strip()
            amawiajacy_adres_numer_domu = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_adres_numer_domu">')[2].partition('</span>')[0].strip()
            adres_numer_mieszkania = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_adres_numer_mieszkania">')[2].partition('</span>')[0].strip()
            kod_pocztowy = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_kod_pocztowy">')[2].partition('</span>')[0].strip()
            miejscowosc = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_wojewodztwo">')[2].partition('<span id="ctl00_ContentPlaceHolder1_zamawiajacy_panstwo">')[0].strip().replace('</span>','')
            panstwo = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_panstwo">')[2].partition('</span>')[0].strip()
            Tel = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_telefon">')[2].partition('</span>')[0].strip()
            Fax = get_htmlSource.partition('ctl00_ContentPlaceHolder1_zamawiajacy_fax">')[2].partition('</span>')[0].strip()
            Complete_address = zamawiajacy_nazwa+','+regon+','+zamawiajacy_adres_ulica+','+amawiajacy_adres_numer_domu+','+adres_numer_mieszkania+','+kod_pocztowy+','+miejscowosc+','+panstwo+"<br>\nTel: "+Tel+"<br>\nFaks: "+Fax
            if Complete_address != "":
                # Complete_address = Translate(Complete_address)
                Complete_address = string.capwords(str(Complete_address))
                Complete_address = html.unescape(str(Complete_address))
                SegField[2] = Complete_address

            # Tender Details
            Type_Of_Contracting = get_htmlSource.partition('ctl00_ContentPlaceHolder1_rodzaj_zamawiajacego">')[2].partition('</span>')[0].strip()
            # Type_Of_Contracting = Translate(Type_Of_Contracting)
            Type_Of_Contracting = html.unescape(str(Type_Of_Contracting))
            Type_of_the_order = get_htmlSource.partition('ctl00_ContentPlaceHolder1_rodzaj_zamowienia">')[2].partition('</span>')[0].strip()
            # Type_of_the_order = Translate(Type_of_the_order)
            Type_of_the_order = html.unescape(str(Type_of_the_order))
            Main_cpv = get_htmlSource.partition('ctl00_ContentPlaceHolder1_cpv_glowny_przedmiot">')[2].partition('</span>')[0].strip()
            # Main_cpv = Translate(Main_cpv)
            Title1 = Title
            if Title1 != '':
                # Title1 = Translate(Title1)
                Title1 = html.unescape(str(Title1))
            Tender_details = str(Title1)+"<br>\n""Rodzaj umowy: "+str(Type_Of_Contracting).replace('(please Specify):', '').strip()+"<br>\n""Numer referencyjny: "+str(reference_number) + "<br>\n""Rodzaj zamówienia: "+str(Type_of_the_order) \
                           + "<br>\n""Główny CPV: " + str(Main_cpv)
            Tender_details = string.capwords(str(Tender_details))  # string in capitalize
            Tender_details = re.sub(' +', ' ', Tender_details)  # Remove Multiple Spaces
            SegField[18] = Tender_details

            Close_Date = get_htmlSource.partition('ctl00_ContentPlaceHolder1_IV_4_4_data">')[2].partition('</span>')[0].strip()
            if Close_Date != '':
                datetime_object = datetime.strptime(Close_Date, "%Y-%m-%d")
                mydate = datetime_object.strftime("%Y-%m-%d")
                SegField[24] = mydate
            else:
                SegField[24] = ''

            SegField[7] = 'PL'
            # Website
            Website_address = get_htmlSource.partition('ctl00_ContentPlaceHolder1_adres_strony_url">')[2].partition('</span>')[0].strip()
            SegField[8] = Website_address

            purchaser1 = purchaser
            if purchaser1 != "":
                # purchaser1 = Translate(str(purchaser1))
                purchaser1 = string.capwords(str(purchaser1))
                purchaser1 = html.unescape(str(purchaser1))
                SegField[12] = purchaser1.upper()
            SegField[13] = str(Tender_id)
            SegField[14] = '2'
            SegField[22] = "0"
            SegField[26] = "0.0"
            SegField[27] = "0"  # Financier
            url = browser.current_url
            SegField[28] = str(url)
            SegField[20] = ""
            SegField[21] = ""
            SegField[42] = SegField[7]
            SegField[43] = ""
            Main_title = Title
            if Main_title != "":
                # Main_title = Translate(str(Main_title))
                Main_title = string.capwords(str(Main_title))
                Main_title = html.unescape(str(Main_title))
                SegField[19] = Main_title
            SegField[31] = 'bzp.uzp.gov.pl'

            ReplyStrings = get_htmlSource.partition('ctl00_ContentPlaceHolder1_cpv_glowny_przedmiot">')[2].partition('</span>')[0].strip()
            if ReplyStrings != "":
                copy_cpv = ""
                Cpv_status = True
                all_string = ""
                try:
                    while Cpv_status == True:
                        phoneNumRegex = re.compile(r'\d\d\d\d\d\d\d\d-')
                        CPv_main = phoneNumRegex.search(ReplyStrings)
                        mainNumber = CPv_main.groups()
                        if CPv_main:
                            copy_cpv = CPv_main.group(), ", "
                            ReplyStrings = ReplyStrings.replace(CPv_main.group(), "")
                        else:
                            Cpv_status = False
                        result = "".join(str(x) for x in copy_cpv)
                        result = result.replace("-", "").strip()
                        result2 = result.replace("\n", "")
                        # print(result2)
                        all_string += result2.strip(",")
                except:
                    pass
                print(all_string.strip(","))
                SegField[36] = all_string
            else:
                SegField[36] = ""

            for SegIndex in range(len(SegField)):
                print(SegIndex, end=' ')
                print(SegField[SegIndex])
                SegField[SegIndex] = html.unescape(str(SegField[SegIndex]))
                SegField[SegIndex] = str(SegField[SegIndex]).replace("'", "''")

            if len(SegField[19]) >= 200:
                SegField[19] = str(SegField[19])[:200]+'...'

            if len(SegField[18]) >= 1500:
                SegField[18] = str(SegField[18])[:1500]+'...'

            
            if SegField[19] == '':
                wx.MessageBox(' Short Desc Blank ','bzp.uzp.gov.pl', wx.OK | wx.ICON_INFORMATION)
            else:
                check_date(get_htmlSource, SegField)
            # create_filename(get_htmlSource, SegField)
            a = True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n",
                  exc_tb.tb_lineno)
            a = False


def check_date(get_htmlSource, SegField):
    deadline = str(SegField[24])
    curdate = datetime.now()
    curdate_str = curdate.strftime("%Y-%m-%d")
    try:
        if deadline != '':
            datetime_object_deadline = datetime.strptime(deadline, '%Y-%m-%d')
            datetime_object_curdate = datetime.strptime(curdate_str, '%Y-%m-%d')
            timedelta_obj = datetime_object_deadline - datetime_object_curdate
            day = timedelta_obj.days
            if day > 0:
                insert_in_Local(get_htmlSource, SegField)
            else:
                print("Expired Tender")
                Global_var.expired += 1
        else:
            print("Deadline Not Given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
