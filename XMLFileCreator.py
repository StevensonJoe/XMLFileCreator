#xmltest.py

# CURRENTLY ONLT CREATES EMPTY OUT Requests
print('importing datetime...')
import datetime
from datetime import datetime as DT
print('importing cElementTree...')
import xml.etree.cElementTree as ET
import xml.dom.minidom
print('---START---')

def main():
    RequestType = 'Type1'
    FilePath = "" # file path to get request txt file

    ReturningSiteCodes = {'SITE1':'SITE0001','SITE2':'SITE0002'} # input site name followed by site code

    # open Requests.txt and grab data, format into a list
    with open(f"{FilePath}Requests.txt","r") as RequestsFile:
        RequestList = RequestsFile.read().replace('\n','\t').split('\t')
    SlotList = [RequestList[x:x+5] for x in range(0, len(RequestList),5)]
    slots = ET.Element("slots")

    # loop through each request in the list and call CreateSlot for each
    for count,i in enumerate(SlotList):
        print(count+1,i)
        if len(i) < 4:
            print(f'line {count+1} missing info, skipping')
        else:
            if i[4] == '':
                i[4] = 'SITE1' # if no site name is included then default to SITE1

            DestinationCode = ReturningSiteCodes[i[4].strip()]
            CreateSlot(slots, RequestType, i, DestinationCode)
            if count == 0:
                XMLFileName = f"REQUESTS{DT.strftime(DT.strptime(' '.join(i[1:3]), '%d-%b-%y %H:%M'),'%d%b%Y')}.xml" # create unique file name


    # create XML file 
    print(f'\nCreating file: {XMLFileName}')
    tree = ET.ElementTree(slots)
    print(f'\nxml file saved to {FilePath}\\Type1Files\\{XMLFileName}')
    tree.write(f"{FilePath}\\Type1Files\\{XMLFileName}")
    input("done...")



def CreateSlot(slots, RequestType, i, DestinationCode):
    slot = ET.SubElement(slots, "slot")
    LatestDeliveryDate = DT.strptime(' '.join(i[1:3]), '%d-%b-%y %H:%M')

    if RequestType == 'Type1': # create custom node values here if needed
        Node1 = '' 
        Node2 = ''
        Node3 = ''
        Node4 = ''
        # if latest delivery date is Monday then set earliest collection date for latest delivery date - 2days
        if LatestDeliveryDate.weekday() == 0:
            CollWindowStart = f'{LatestDeliveryDate.replace(hour=18, minute=0) - datetime.timedelta(days=2)}'
            CollWindowStart = DT.strptime(CollWindowStart,'%Y-%m-%d %H:%M:%S')
        else:
            # if latest delivery not Monday then earliest collection = latestdelivery - 1day
            CollWindowStart = f'{LatestDeliveryDate.replace(hour=18, minute=0) - datetime.timedelta(days=1)}'
            CollWindowStart = DT.strptime(CollWindowStart,'%Y-%m-%d %H:%M:%S')
        
    else:
        print('Error: Unknown Request Type')
        quit()

    
    # assign each element a value
    ET.SubElement(slot,"Node1").text = Node1
    ET.SubElement(slot,"Node2").text = Node2
    ET.SubElement(slot,"Node3").text = Node3
    ET.SubElement(slot,"Node4").text = Node4
    ET.SubElement(slot,"CollectionWindowStart").text = f'{CollWindowStart}'
    ET.SubElement(slot,"CollectionWindowEnd").text = f'{LatestDeliveryDate}' #f'{LatestDeliveryDate.replace(hour=18, minute=0)}'
    ET.SubElement(slot,"DeliveryWindowStart").text = f'{CollWindowStart.replace(hour=20, minute=0)}'
    ET.SubElement(slot,"DeliveryWindowEnd").text = f'{LatestDeliveryDate.replace(hour=23, minute=0)}'
    ET.SubElement(slot,"DestinationRef").text = DestinationCode
    ET.SubElement(slot,"Priority").text = ''
    ET.SubElement(slot,"SourceRef").text = i[3]
    ET.SubElement(slot,"RequestDate").text = DT.strftime(DT.now() + datetime.timedelta(hours=2),'%d-%b-%y') #DT.strftime(DT.strptime(i[1],'%d-%b-%y')  - datetime.timedelta(days=1),'%d-%b-%y')
    ET.SubElement(slot,"BookingDate").text = DT.strftime(DT.strptime(i[1],'%d-%b-%y')  - datetime.timedelta(days=1),'%d-%b-%y')
    ET.SubElement(slot,"PercentFill").text = ''
    ET.SubElement(slot,"CreatedBy").text = ''
    ET.SubElement(slot,"Comments").text = ''
    ET.SubElement(slot,"PriorityType").text = ''
    ET.SubElement(slot,"DeliveryDate").text = i[1]
    ET.SubElement(slot,"TargetDeliveryTime").text = f'{LatestDeliveryDate.replace(hour=23, minute=0)}'



if __name__ == '__main__':
    main()
