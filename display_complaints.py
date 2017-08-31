"""
Title: Display Pretty Print Module
Author: Zach Morgan
"""

from utilities import *

def pretty_print(str):
    """
    Purpose: prints a complaint formatted by the slot name, new line, 8 spaces, then the contents of the slot.
    This function contains the text within a space of 67 characters by searching for a whitespace when it hits 62
    and cutting the current word to the next line if it doesnt find one by 67
    :param str: text field
    :return: NONE
    """
    curr_line = -1
    look_for_white = False
    for index in range(len(str)):
        if index == len(str) - 1:
            print(str[index])
            continue
        if curr_line == 0:
            print("\n" + "        ", end="")
        if curr_line == -1:
            print("        ", end = "")
            curr_line += 1
        curr_line += 1
        if curr_line >= 62:
            look_for_white = True
        if look_for_white and curr_line > 67:
            look_for_white = False
            curr_line = 0
            continue
        if look_for_white:
            if str[index] == " ":
                look_for_white = False
                curr_line = 0
                continue
            else:
                print(str[index], end="")
        else:
            print(str[index], end = "")



def display_complaint(complaint):
    """
    Purpose: Puts the output of the pretty print with its matching header and prints everything
    :param complaint: complaint object
    :return: NONE
    """
    headers = ["Date_received:", "Product:", "Sub_product:" , "Issue:" , "Sub_issue:" , "Consumer_complaint_narrative:", "Company_public_response:" ,
                "Company:" , "State:" , "ZIP_code:" , "Tags:" , "Consumer_consent_provided?:" , "Submitted_via:" , "Date_sent_to_company:" ,
                "Company_response_to_consumer:" , "Timely_response?:" , "Consumer_disputed?:" , "Complaint_ID:"]
    print(headers[0])
    pretty_print(complaint.Date_received)
    print(headers[1])
    pretty_print(complaint.Product)
    print(headers[2])
    pretty_print(complaint.Sub_product)
    print(headers[3])
    pretty_print(complaint.Issue)
    print(headers[4])
    pretty_print(complaint.Sub_issue)
    print(headers[5])
    pretty_print(complaint.Consumer_complaint_narrative)
    print(headers[6])
    pretty_print(complaint.Company_public_response)
    print(headers[7])
    pretty_print(complaint.Company)
    print(headers[8])
    pretty_print(complaint.State)
    print(headers[9])
    pretty_print(complaint.ZIP_code)
    print(headers[10])
    pretty_print(complaint.Tags)
    print(headers[11])
    pretty_print(complaint.Consumer_consent_provided)
    print(headers[12])
    pretty_print(complaint.Submitted_via)
    print(headers[13])
    pretty_print(complaint.Date_sent_to_company)
    print(headers[14])
    pretty_print(complaint.Company_response_to_consumer)
    print(headers[15])
    pretty_print(complaint.Timely_response)
    print(headers[16])
    pretty_print(complaint.Consumer_disputed)
    print(headers[17])
    pretty_print(complaint.Complaint_ID)

def main():
    entries = read_complaint_data("data/" + input("Enter Consumer Complaints file:"))
    input_loop = True
    IDlst = []
    while input_loop:
        inp = input("Enter a Complaint ID (Ex. 13002) or press ENTER key to stop:")
        if inp == '':
            break
        IDlst.append(int(inp))
    for ID in IDlst:
        if ID in entries:
            display_complaint(entries[ID])
        else:
            print("\n" + "====================" + "\n" + str(ID) + " not in dataset" + "\n" + "====================" + "\n")

if __name__ == "__main__":
    main()

