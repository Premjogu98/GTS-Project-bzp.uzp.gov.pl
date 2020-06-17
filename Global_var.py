duplicate = 0
inserted = 0
expired = 0
skipped = 0
deadline_Not_given = 0
From_Date = ''
todate = ''
Skipped = ""
Total=0
QC_Tender = 0


def Process_End():
    print("Deadline Date Was Dead")
    print("Total: ",Total)
    print('Duplicate: ' , duplicate)
    print('Expired: ' , expired)
    print('Inserted: ' , inserted)
    print('Skipped: ' , skipped)
    print('deadline Not given: ' , deadline_Not_given)
    print('QC Tender: ' , QC_Tender)



