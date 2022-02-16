"""Assignment 10

Contact Tracing App
	- Create a python program that will read QRCode using your webcam
	- You may use any online QRCode generator to create QRCode
	- All personal data are in QRCode 
	- You may decide which personal data to include
	- All data read from QRCode should be stored in a text file including the date and time it was read

Note: 
	- Search how to generate QRCode
	- Search how to read QRCode using webcam
	- Search how to create and write to text file
	- Your source code should be in github before Feb 19
	- Create a demo of your program (1-2 min) and send it directly to my messenger. """

# lagay ko lng references and guide ko para madali ko mabalikan: 
# https://www.geeksforgeeks.org/webcam-qr-code-scanner-using-opencv/
# https://medium.com/@stasinskipawel/create-and-read-qr-code-with-python-in-3-minutes-opencv-and-qrcode-38ecc3a6258a
# https://www.programiz.com/python-programming/file-operation
# https://www.geeksforgeeks.org/get-current-date-and-time-using-python/

# qr generator used
# https://goqr.me/#


#1st try, d pa tapos, tinesting lng ung cv2 module, gumawa ng sample qr code, nadedetect na dapat ng webcam ung qr
#2nd try, writes all information from scanned qrs to a txt file 
#3rd try, prevents repeat writing of the same qr, added time and date of scan, created more qr codes, added comments, added instructions, added auto open of txt file


import sys
import cv2
import datetime
import os

def instructions():
    print ("\nThis program scans for QR Code and store its data to a txt file. Similar to a Contact Tracing App.")
    while True:
        start = input("Enter 's' to start the program. Capital 'Q' to exit.  ").lower()
        if start[0] == 'q': 
            print ("The program is closing. Try again next time.")
            sys.exit()
        elif start[0] == 's':
            print ("The QR Scanner is opening ...\nShow your QR Code to to enter the building.")
            break


def qr_scanning():     
    counter = 0                                                      # need ung counter mmya
    cam = cv2.VideoCapture(0)                                        # open webcam and scans for qr
    detector = cv2.QRCodeDetector()

    while True:                                                      # loop para tuloy tuloy at realtime ung pagscan nya ng qr
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
      
        if data:                                                     # if may nascan na syang qr                   
            date_n_time = date_time()                                 # cinall out agad ung func na nakassign sa pagkuha ng time para mas close or accurate sya sa time na nascan ung pic
            person = data                               
            print("--- QR Code scanned ---\n" + person + "\n")      # pinrint ko lng ung laman ng qr para alam kong nascan na siya
            counter = write_txt(person, counter, date_n_time)                   # call out func sa pagwrite sa txt file ng info ng mga qrs
        cv2.imshow("QR Scanner", img) 

        if cv2.waitKey(1) == ord("Q"):                                   # Enter Q para mastop ung scanning (dapat capital "Q" ung pagpindot)
            print ("\nScanning complete. Manually open 'file3.txt' in cases that it did not open automatically.\n")
            os.startfile('file3.txt')                                  # open the txt file automatically
            break
    cam.release()
    cv2.destroyAllWindows()


def date_time():      
    DT_right_now = datetime.datetime.now()                       # kuha ng date and time

    # assign to var lng para mas madali siya ilagay sa final date and time
    year = DT_right_now.year
    day = DT_right_now.day
    month = DT_right_now.month
    hour = DT_right_now.hour
    minute = DT_right_now.minute
    second = DT_right_now.second

    #final date and time
    date_n_time = (f"Date of Arrival (M/D/Y): {month} / {day} / {year}\nTime of Arrival: {hour} : {minute} : {second}")
    return date_n_time


def write_txt(person, counter, date_n_time):                         # write all info ng qr to txt file
    try:                                                           # gumamit ako ng try and finally para sure na maclose ung file pag tapos na
        if counter == 0:                                         # kapag counter 0, unang qr plng, ibig sabihin wala pang txt file kaya magcecreate muna (kapag may existing txt file na irerewrite ung nakasulat)
            file = open("file3.txt","w")                         # w ung parameter para magcreate ng bago or rewrite kapag may existing
            file.write(person + "\n" + date_n_time +"\n\n")                       # write sa txt file ng info ng qr and ng date and time of scan
            counter  =+ 1
        else:                                                       # kapag hindi first qr
            file = open('file3.txt', 'r')                            # r ung parameter para read lng muna
            repeat = file.read().find(person)                       # checks the txt file kung repeat scan na tong qr 
            if repeat != -1:                                         # aka if may repeat, if not -1 kasi -1 ang nirereturn na value ng find func kapag hnidi nahanap
                print("-- ALREADY SCANNED --\n")
            else:                                                   # kapag bago ung qr
                file = open("file3.txt","a")                        # a ung parameter kasi append sya, idadagdag nya lng sa dulo
                file.write(person + "\n" + date_n_time +"\n\n")         # append sa txt file ng info ng qr and ng date and time of scan
        return counter   

    finally:
        file.close()                                                 # close file para iwas issues


def main():
    instructions()
    qr_scanning()

if __name__ == "__main__":
	main()