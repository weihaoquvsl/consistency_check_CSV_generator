import pdfplumber
import pandas as pd
import re
from datetime import date
today = date.today()
print(today)

# initiate a connection to the pdf file
class parser:
    def __init__(self, pdf_file):
        self.fixed_text = ""
        self.pdf_file = pdf_file
# extract all text from the given pdf file into a string
    def generate_fixed_text(self):
        with pdfplumber.open(self.pdf_file) as pdf:
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                text = page.extract_text()
                self.fixed_text += text
# write the string into a file named fixed_text.txt
        text_file = open("fixed_text.txt", "w")
        text_file.write(self.fixed_text)
        text_file.close()

# select out the portion of pdf where check 4's output are located, which are in between the check 4 and check 5 titles
# store this portion of the pdf in check_4_stripped.txt file
    def generate_check_4_stripped(self):
        with open("fixed_text.txt") as infile, open("check_4_stripped.txt", "w") as outfile:
            copy = False
            for line in infile:
                if line.strip() == '''4. Check that F when present is strictly greater than 0 and strictly less than 1.''':
                    copy = True
                    continue
                elif line.strip() == '''5. List all drugs that have ka=0 in any of their experimental drug parameter list.''':
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)
    def query_check_4(self):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
# establish the pattern that must be extracted
        pattern = re.compile("ExpData ID: (.*), DPL ID: (.*), F: (.*), (.*)")
# open the stripped txt file and iterate through each line. Whenever a line matches the pattern, split the text
# split the text using regex at each indicated data index and append each item into a list, stripping the new line
        with open("check_4_stripped.txt") as file:
            for i in file:
                if pattern.match(i):
                    x = re.split("ExpData ID: |, DPL ID: |, F: |, ", i)
                    list1.append(x[1])
                    list2.append(x[2].strip(" \n"))
                    list3.append(x[3].strip(" \n"))
                    list4.append(x[4].strip(" \n"))
# create a dataframe using the generated lists and name the columns
        df = pd.DataFrame(list(zip(list1, list2, list3, list4)))
        df.columns = ["ExpData ID", "DPL ID", "F", "PF"]
        print(df)
# Export the created dataframe into a csv with no index
        df.to_csv(f"{today} check_4.csv", index = False)

    def generate_check_2_stripped(self):
        with open("fixed_text.txt") as infile, open("check_2_stripped.txt", "w") as outfile:
            copy = False
            for line in infile:
                if line.strip() == '''2. Check that every drug with validation data has at least one in vivo or in vitro''':
                    copy = True
                    continue
                elif line.strip() == '''3. Check that average weights for all SSGS are between 0 and 200 kg.''':
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)
    def query_check_2(self):
        list1 = []
        list2 = []
        pattern = re.compile("Drug ID: (.*), Drug Name: (.*)")
        with open("check_2_stripped.txt") as file:
            for i in file:
                if pattern.match(i):
                    x = re.split("Drug ID: |, Drug Name: ", i)
                    list1.append(x[1])
                    list2.append(x[2].strip(" \n"))
        df = pd.DataFrame(list(zip(list1, list2)))
        df.columns = ["Drug ID", "Drug Name"]
        print(df)
        df.to_csv(f"{today} check_2.csv", index = False)

    def generate_check_46_stripped(self):
        with open("fixed_text.txt") as infile, open("check_46_stripped.txt", "w") as outfile:
            copy = False
            for line in infile:
                if line.strip() == '''46. Identify all exp. data ids that have a clearance record without at least one''':
                    copy = True
                    continue
                elif line.strip() == '''47. Identify all exp. data ids that have a clearance record with a clearance parameter''':
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)

    def query_check_46(self):
        list1 = []
        pattern = re.compile("[0-9]")
        with open("check_46_stripped.txt") as file:
            for i in file:
                if pattern.match(i):
                    list1.append(i.strip())
        s = pd.Series(list1, name = "experimental_data_id")
        print(s)
        s.to_csv(f"{today} check_46.csv", index = False)

    def generate_check_47_stripped(self):
        with open("fixed_text.txt") as infile, open("check_47_stripped.txt", "w") as outfile:
            copy = False
            for line in infile:
                if line.strip() == '''47. Identify all exp. data ids that have a clearance record with a clearance parameter''':
                    copy = True
                    continue
                elif line.strip() == '''---------------------------------------------------R&D Checks''':
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)

    def query_check_47(self):
        list1 = []
        pattern = re.compile("[0-9]")
        with open("check_47_stripped.txt") as file:
            for i in file:
                if pattern.match(i):
                    list1.append(i.strip())
        s = pd.Series(list1, name = "experimental_data_id")
        print(s)
        s.to_csv(f"{today} check_47.csv", index = False)

    def generate_check_33_stripped(self):
        with open("fixed_text.txt") as infile, open("check_33_stripped.txt", "w") as outfile:
            copy = False
            for line in infile:
                if line.strip() == '''33. Check that for all IV bolus validation data with a time/concentration observation''':
                    copy = True
                    continue
                elif line.strip() == '''36. Check for drugs where systemic clearance is > hepatic blood flow, but <= cardiac''':
                    copy = False
                    continue
                elif copy:
                    outfile.write(line)

    def query_check_33(self):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        pattern = re.compile("\[")
        with open("check_33_stripped.txt") as file:
            for i in file:
                if pattern.match(i):
                    x = re.split("\[|, |\]\n", i)
                    list1.append(x[1])
                    list2.append(x[2])
                    list3.append(x[3])
                    list4.append(x[4])

        df = pd.DataFrame(list(zip(list1, list2, list3, list4)))
        df.columns = ["validation_data_id", "calculated_cmax", "owner", "days since validity status change"]
        print(df)
        df.to_csv(f"{today} check_33.csv", index=False)


x = parser("")
x.generate_fixed_text()
x.generate_check_4_stripped()
x.query_check_4()
x.generate_check_2_stripped()
x.query_check_2()
x.generate_check_46_stripped()
x.query_check_46()
x.generate_check_47_stripped()
x.query_check_47()
x.generate_check_33_stripped()
x.query_check_33()
