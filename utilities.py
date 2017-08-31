"""
Author: Zach Morgan
Title: Utilities Module
"""

from rit_lib import *
import time


class Complaint(struct):
    _slots = ((str, "Date_received" ), (str, "Product"), (str, "Sub_product"), (str, "Issue"), (str, "Sub_issue"),
             (str, "Consumer_complaint_narrative" ), (str, "Company_public_response"), (str, "Company"),
             (str, "State"), (str, "ZIP_code"), (str, "Tags"), (str, "Consumer_consent_provided"), (str, "Submitted_via"),
             (str, "Date_sent_to_company"), (str, "Company_response_to_consumer"), (str, "Timely_response"),
             (str, "Consumer_disputed"), (str, "Complaint_ID"))

def mult_splitInfo(lst, mid_phrase = False, mult_line = False):
    """
    Purpose: Appropriately splits a multiple line complaint
    Pre-Condition: List split by commas, part of a multiple line complaint
    :return: appropriately split list of the line
    """
    firsti = 0
    info = []
    for index in range(len(lst)):
        lst[index] = lst[index].strip("\n ")
        if lst[index] == '' and not mid_phrase:
                info.append("UNK.")
                continue
        if lst[index] == '' and mid_phrase:
            continue
        if lst[index][ : ].strip("\n") == '"':
            info.append("empty quote")
            mid_phrase = False
            continue
        if lst[index][0] == '"':
            if lst[index][0:2] != '""':
                if not mid_phrase:
                    if lst[index][0] == '"' and lst[index][-1] == '"':
                        info.append(lst[index])
                        continue
                    if lst[index][-1] == '"':
                        info.append(lst[index])
                        continue
                    else:
                        firsti = index
                        mid_phrase = True
                        continue
                if mid_phrase:
                    lasti = index
                    phrase = ",".join(lst[firsti : lasti + 1]).lstrip('" ')
                    phrase = phrase.strip('"')
                    info.append(phrase)
                    mid_phrase = False
                    continue
        if lst[index][-1] == '"':
            if lst[index][-1:-3] != '""':
                if mid_phrase:
                    phrase = ",".join(lst[firsti : index + 1]).lstrip('" ')
                    phrase = phrase.strip('"')
                    info.append(phrase)
                    mid_phrase = False
                    continue
        elif not mid_phrase:
            info.append(lst[index])
    if mid_phrase:
        info.append(",".join(lst[firsti : ]))
        mult_line = True
        return info, mid_phrase, mult_line
    return info, mid_phrase, mult_line


def one_line_complaint(lst):
    """
    Purpose: Appropriately splits a complaint that is entirely on one line
    Pre-Condition: All 18 fields are in the lst parameter
    :param lst: list split by commas
    :return: lst split ready for complaintification
    """
    info = []
    mid_phrase = False
    for index in range(len(lst)):
        if '"' in lst[index]:
            if not mid_phrase:
                if lst[index][0] == '"' and lst[index][-1] == '"':
                    info.append(lst[index])
                    continue
                if lst[index][-1] == '"':
                    info.append(lst[index])
                    continue
                else:
                    firsti = index
                    mid_phrase = True
                    continue
            if mid_phrase:
                lasti = index
                phrase = ",".join(lst[firsti: lasti + 1]).lstrip('" ')
                phrase = phrase.strip('"')
                info.append(phrase)
                mid_phrase = False
                continue
        if lst[index] == '':
            info.append("UNK.")
            continue
        elif not mid_phrase:
            info.append(lst[index])
    return info


def joinInfo(lst):
    """
    Purpose: Stitches together two parts of a multiple line complaint
    lst: two parts of a multi line complaint
    return: Big list containing all fields that are supposed to be seperate, seperated and the others joined together
    """
    biglst = []
    len18 = False
    if lst[0][1]:
        if lst[1][0][0] != "empty quote":
            str = lst[0][0].pop(-1)
            a = [str.lstrip('"'), lst[1][0][0].strip('"')]
            lst[1][0][0] = ",".join(a)
    if lst[1][0][0] == "empty quote":
        lst[1][0].pop(0)
        lst[0][0][-1] = lst[0][0][-1].lstrip('"')
    for phrase in lst[0][0]:
            biglst.append(phrase)
    for phrase in lst[1][0]:
            biglst.append(phrase)
    if len(biglst) == 18:
        len18 = True
    return biglst, lst[1][1], len18

def read_complaint_data(filepath):
    """
    Purpose: main function that utilizes all other utility functions to create complaints and places them in the dictionary
    :param file: CSV file containing complaint data
    :return: dictionary with each complaint mapped to its unique complaint ID
    """
    start_time = time.time()
    print("Reading " + filepath + "...")
    entries = {}
    mult_line_complaint = []
    mid_phrase = False
    mult_line = False
    len18 = False
    biglst = []
    hard_reset = False
    for line in open(filepath):
        line = line.strip("\n")
        lst = line.split(",")
        if len(lst) == 1 and lst[0] == '':
            continue
        if lst[-1] == "Complaint ID":
            continue
        else:
            if len(biglst) > 40:
                mult_line_complaint = []
                biglst = []
                mult_line = False
                mid_phrase = False
                hard_reset = True
            if hard_reset:
                if len(lst) > 1 and not mult_line and lst[-1].isdigit() and (lst[-2] == "No" or lst[-2] == "Yes" or lst[-2] == ""):
                    ls = one_line_complaint(lst)
                    if len(ls) == 18:
                        entries[int(ls[-1])] = Complaint(ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11], ls[12], ls[13], ls[14], ls[15], ls[16], ls[17])
                        hard_reset = False
                        continue
                    else:
                        continue
            if len(lst) > 1 and not mult_line and lst[-1].isdigit() and (lst[-2] == "No" or lst[-2] == "Yes" or lst[-2] == ""):
                ls = one_line_complaint(lst)
                if len(ls) == 18:
                    entries[int(ls[-1])] = Complaint(ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11], ls[12], ls[13], ls[14], ls[15], ls[16], ls[17])
                    continue
                else:
                    pass
            if not mult_line:
                ls, mid_phrase, mult_line = mult_splitInfo(lst)
                mult_line_complaint.append((ls, mid_phrase))
                continue
            if mult_line:
                ls, mid_phrase, mult_line = mult_splitInfo(lst, mid_phrase, mult_line)
                mult_line_complaint.append((ls, mid_phrase))
                biglst, mid_phrase, len18 = joinInfo(mult_line_complaint)
                mult_line_complaint = [(biglst, mid_phrase)]
            if not mid_phrase and len18 and biglst[-1].isdigit():
                ls = biglst
                entries[int(ls[-1])] = Complaint(ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9], ls[10], ls[11], ls[12], ls[13], ls[14], ls[15], ls[16], ls[17])
                mult_line_complaint = []
                mult_line = False
                len18 = False
    tottime = time.time() - start_time
    print("Total entries: " + str(len(entries)) + "\n" + "Time elapsed: " + str(tottime) +"\n" + "Reading complete.")
    return entries

def main():
    entries = read_complaint_data("data/" + input("Enter Consumer Complaints file:"))
    products = {}
    input_loop = True
    while input_loop:
        product = (input("Enter Product phrase or press ENTER key to stop:")).lower()
        if product == "":
            break
        products[product] = product
    for ID, complaint in entries.items():
        temp = complaint.Product.split()
        for word in temp:
            if word.lower() in products:
                print(complaint.Complaint_ID + ", " + complaint.Product + ", " + complaint.Company + ", " + complaint.State)

if __name__ == "__main__":
    main()


