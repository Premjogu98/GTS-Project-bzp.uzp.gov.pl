from selenium import webdriver
import time
from datetime import datetime
import Global_var
import sys, os
import ctypes
from Scraping_data import Scraping_data


def ChromeDriver():
    File_Location = open(
        "D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\bzp.uzp.gov.pl\\Location For Database & Driver.txt", "r")
    TXT_File_AllText = File_Location.read()
    Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
    browser = webdriver.Chrome(executable_path=str(Chromedriver))
    browser.get('http://searchbzp.uzp.gov.pl/Search.aspx')
    browser.maximize_window()
    time.sleep(2)

    for From_Date in browser.find_elements_by_xpath('//*[@id="MainContent_dateDataPublikacjiOd_I"]'):
        From_Date.send_keys(str(Global_var.From_Date))
        time.sleep(1.5)
        break

    for To_Date in browser.find_elements_by_xpath('//*[@id="MainContent_dateDataPublikacjiDo_I"]'):
        To_Date.send_keys(str(Global_var.todate))
        time.sleep(1.5)
        break

    for Order_Mode in browser.find_elements_by_xpath('//*[@id="MainContent_ddlOrderMode_B-1"]'):
        Order_Mode.click()
        time.sleep(1.5)
        for Order_Mode1 in browser.find_elements_by_xpath('//*[@id="MainContent_ddlOrderMode_DDD_L_LBI1T0"]'):
            Order_Mode1.click()
            time.sleep(1.5)
        break

    for Type_of_advertisement in browser.find_elements_by_xpath('//*[@id="MainContent_ddlAnnouncementType2_B-1"]'):
        Type_of_advertisement.click()
        time.sleep(1.5)
        for Type_of_advertisement1 in browser.find_elements_by_xpath('//*[@id="MainContent_ddlAnnouncementType2_DDD_L_LBI1T0"]'):
            Type_of_advertisement1.click()
            time.sleep(1.5)
        break

    for Search in browser.find_elements_by_xpath('//*[@id="MainContent_btnSzukaj"]'):
        Search.click()
        break

    time.sleep(2)

    Nav_link(browser)


def Nav_link(browser):
    pages = ''
    for pages in browser.find_elements_by_xpath('//*[@class="dxp-lead dxp-summary"]'):
        pages = pages.get_attribute('innerText').strip()   # Eg :  Strona 1 z 40 (elementy 791)
        if 'Strona' in pages:
            pages = pages.partition('Strona 1 z')[2].partition('(')[0].strip()  # Collecting pages range
        if 'Page' in pages:
            pages = pages.partition('Page 1 of')[2].partition('(')[0].strip()
        break
    if pages == "":
        pages = "1"
    else:pass
    tr = 0
    page_tr = 2
    for next_page in range(int(pages)):
        a = False
        while a == False:
            try:
                for tr1 in range(0, 20, 1):
                    browser.switch_to.window(browser.window_handles[0])
                    for publish_date in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXDataRow'+str(tr)+'"]/td[4]'):
                        pubdate = publish_date.get_attribute("innerText")
                        datetime_object = datetime.strptime(pubdate, '%Y-%m-%d')
                        publish_date1 = datetime_object.strftime("%Y-%m-%d")
                        if publish_date1 >= Global_var.From_Date:
                            print("♥ Tender Date Alive ♥")
                            purchaser = ''
                            Tender_id = ''
                            Title = ''
                            reference_number = ''
                            for purchaser in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXDataRow'+str(tr)+'"]/td[5]'):
                                purchaser = purchaser.get_attribute('innerText').strip()
                                if ',' in purchaser:
                                    purchaser_split_list = purchaser.split(",")
                                    purchaser = str(purchaser_split_list[0])
                                break
                            for Tender_id in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXDataRow'+str(tr)+'"]/td[3]'):
                                Tender_id = Tender_id.get_attribute('innerText').strip()
                                break
                            for Title in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXDataRow'+str(tr)+'"]/td[8]'):
                                Title = Title.get_attribute('innerText').strip()
                                if '-' in Title:
                                    Title = Title.replace('-', '').replace('"','')
                                break
                            for reference_number in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXDataRow'+str(tr)+'"]/td[9]'):
                                reference_number = reference_number.get_attribute('innerText').strip()
                                if '-' in Title:
                                    Title = Title.replace('-', '')
                                break
                            b = 1
                            while b == 1:
                                try:
                                    for click_on_Zobacz_button in browser.find_elements_by_xpath('/html/body/form/div[4]/div/table[22]/tbody/tr/td/table[1]/tbody/tr['+str(page_tr)+']/td[1]/a'):
                                        click_on_Zobacz_button = click_on_Zobacz_button.get_attribute('href')
                                        if click_on_Zobacz_button != '':
                                            browser.execute_script("window.open('');")
                                            browser.switch_to.window(browser.window_handles[1])
                                            browser.get(str(click_on_Zobacz_button))
                                            b = 0
                                        else:
                                            for click_on_Zobacz_button1 in browser.find_elements_by_xpath(
                                                    '/html/body/form/div[4]/div/table[19]/tbody/tr/td/table[1]/tbody/tr['+str(page_tr)+']/td[1]/a'):
                                                click_on_Zobacz_button1 = click_on_Zobacz_button1.get_attribute('href')
                                                browser.execute_script("window.open('');")
                                                browser.switch_to.window(browser.window_handles[1])
                                                browser.get(str(click_on_Zobacz_button1))

                                    b = 0
                                except:
                                    print('Link nahi mil raha hai click karne ke liye Bhai !!!')
                                    time.sleep(1.5)
                                    b = 1
                            time.sleep(1.5)
                            try:
                                browser.switch_to.window(browser.window_handles[1])
                            except:
                                browser.switch_to.window(browser.window_handles[0])
                            clicking_process(browser, purchaser, reference_number, Title, Tender_id)
                            Global_var.Total += 1
                            print(" Total: " + str(
                                Global_var.Total) + " Duplicate: " + str(
                                Global_var.duplicate) + " Expired: " + str(
                                Global_var.expired) + " Inserted: " + str(
                                Global_var.inserted) + " Skipped: " + str(
                                Global_var.skipped) + " Deadline Not given: " + str(
                                Global_var.deadline_Not_given) + " QC Tenders: " + str(
                                Global_var.QC_Tender), "\n")
                            # browser.refresh()
                            page_tr += 1
                            tr += 1
                        else:
                            ctypes.windll.user32.MessageBoxW(0, "Total: " + str(
                                    Global_var.Total) + "\n""Duplicate: " + str(
                                    Global_var.duplicate) + "\n""Expired: " + str(
                                    Global_var.expired) + "\n""Inserted: " + str(
                                    Global_var.inserted) + "\n""Skipped: " + str(
                                    Global_var.skipped) + "\n""Deadline Not given: " + str(
                                    Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
                                    Global_var.QC_Tender) + "", "bzp.uzp.gov.pl", 1)
                            Global_var.Process_End()
                            browser.close()
                            break
                for pages_button in browser.find_elements_by_xpath('//*[@id="MainContent_gvSzukaj_DXPagerBottom_PBN"]'):
                    pages_button.click()
                    time.sleep(2)
                    break
                a = True
                page_tr = 2
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n",
                      fname,
                      "\n", exc_tb.tb_lineno)
                time.sleep(5)
                a = False

    # IF range Complete Then it will be exit
    ctypes.windll.user32.MessageBoxW(0, "Total: " + str(
        Global_var.Total) + "\n""Duplicate: " + str(
        Global_var.duplicate) + "\n""Expired: " + str(
        Global_var.expired) + "\n""Inserted: " + str(
        Global_var.inserted) + "\n""Skipped: " + str(
        Global_var.skipped) + "\n""Deadline Not given: " + str(
        Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(
        Global_var.QC_Tender) + "", "bzp.uzp.gov.pl", 1)
    Global_var.Process_End()
    browser.quit()
    sys.exit()


def clicking_process(browser, purchaser, reference_number, Title, Tender_id):
    a = False
    while a == False:
        try:
            for Web_page in browser.find_elements_by_xpath("/html"):
                get_htmlSource = Web_page.get_attribute("outerHTML").replace('href="../', 'href="https://bzp.uzp.gov.pl/').replace('<input type="submit" name="ctl00$ContentPlaceHolder1$btnWydrukStrony" value="Wydruk strony" id="ctl00_ContentPlaceHolder1_btnWydrukStrony" class="no-print">', '')
                Scraping_data(get_htmlSource, browser,purchaser,reference_number,Title,Tender_id)
                try:
                    browser.switch_to.window(browser.window_handles[1])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[0])
                except:pass
                time.sleep(2)
            a = True
        except Exception as e:
            browser.switch_to.window(browser.window_handles[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname,
                  "\n", exc_tb.tb_lineno)
            time.sleep(5)
            a = False

            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])


ChromeDriver()
