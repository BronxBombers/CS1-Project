"""
Author: Zach Morgan
Title: Company-based Analysis
"""

from utilities import *
from collections import defaultdict
import operator

def make_company_map(dataset):
    """
    Purpose: Creates a dictionary with the key being the two letter state abbreviation, and the value being a
    dictionary that uses the companies products as the key, and a list of complaints that match the company
    and the certain product
    :param dataset: dictionary of complaitns mapped to their own ID
    :return: company dictionary of dictionaries
    """
    companymap = defaultdict(dict)
    for key in dataset:
        if dataset[key].Company in companymap:
            if dataset[key].Product in companymap[dataset[key].Company]:
                companymap[dataset[key].Company][dataset[key].Product].append(dataset[key])
            else:
                companymap[dataset[key].Company][dataset[key].Product] = [dataset[key]]
        else:
            companymap[dataset[key].Company] = {dataset[key].Product: [dataset[key]]}
    return companymap

def findmax(dictionary):
    """
    Purpose: Utility function used to find the max value in a dictionary
    :param dictionary (and pre-condition): dictionary that uses integers for values, and whatever for keys
    :return:
    """
    key, value = list(dictionary.keys()), list(dictionary.values())
    return key[value.index(max(value))]

def split_dictionary(companymap):
    """
    Purpose: Utility function used to split the dictionary of dictionaries into a company based and product based dictionary
    :param companymap: company map dictionary
    :return: product dictionary with value being the amount of complaints for that product, and a company dictionary with
    the values being the amount of complaints that company has
    """
    company_complaints = {}
    product_complaints = {}
    for key in companymap:
        for product in companymap[key]:
            if product in product_complaints:
                product_complaints[product] += len(companymap[key][product])
            if key in company_complaints:
                company_complaints[key] += len(companymap[key][product])
            if not key in company_complaints:
                company_complaints[key] = len(companymap[key][product])
            if not product in product_complaints:
                product_complaints[product] = len(companymap[key][product])
    return company_complaints, product_complaints

def compute_statistics(dataset):
    """
    Purpose: computes various statistics of the provided dataset
    :param dataset: dictionary of complaints based on ID, not company, the company map is created within the function
    :return: NONE
    """
    companymap = make_company_map(dataset)
    company_complaints, product_complaints = split_dictionary(companymap)
    median = sorted(list(company_complaints.values()))
    if (len(median) % 2) == 1:
        median_num = median[(len(median) - 1) // 2]
    else:
        first = median[len(median) // 2]
        second = median[first + 1]
        median_num = (first + second) / 2
    total_complaints = len(dataset)
    total_companies = len(companymap)
    total_products = len(product_complaints)
    most_company = findmax(company_complaints)
    most_company_percent = (company_complaints[most_company] / total_complaints) * 100
    most_product = findmax(product_complaints)
    most_product_percent = (product_complaints[most_product] / total_complaints) * 100
    print("Statistics" + "\n\n" + "Total complaints: " + str(total_complaints) + "\n" + "Total companies: " + str(total_companies) + "\n" + "Total Products: " + str(total_products) + "\n")
    print("Complaints per Company" + "\n\n" + "Average per company: " + str(total_complaints / total_companies) + "\n" +"Median per company: "+ str(median_num) + "\n\n" +
          "Most complained about company: " + str(most_company) + ": "  + str(company_complaints[most_company]) + " (" + str(most_company_percent)[0 : 5] + "%)" + "\n" + "Most complained about product: " + str(most_product)
          + " : " + str(product_complaints[most_product]) + " (" + str(most_product_percent)[0 : 5] + "%)")

def list_company_complaints(companymap, topnumber = 3):
    """
    Purpose: pretty prints information about the top x number of companies based on complaint amount
    :param companymap: company map dictionary
    :param topnumber: user input integer that decides how many companies are displayed
    :return: NONE
    """
    print("Top " + str(topnumber) + " Companies and their Complaints" + "\n")
    company_complaints = split_dictionary(companymap)[0]
    complaints_sorted = sorted(company_complaints.items(), key=operator.itemgetter(1))
    for index in range(1, topnumber + 1):
        company_name = complaints_sorted[-index][0]
        print(complaints_sorted[-index][0] + " : " + str(complaints_sorted[-index][1]) + " complaints")
        for product in companymap[company_name]:
            print("        " + str(len(companymap[company_name][product])) + "  " + product + " complaints.")
        print("")

def main():
    file = input("Enter Consumer Complaints File:")
    entries = read_complaint_data("data/" + file)
    companymap = make_company_map(entries)
    compute_statistics(entries)
    print("\n\n")
    number = int(input("Enter number of top company summaries to view. Hit Enter for default value (3):"))
    print("\n")
    if number == "":
        list_company_complaints(companymap)
    else:
        list_company_complaints(companymap, number)

if __name__ == "__main__":
    main()