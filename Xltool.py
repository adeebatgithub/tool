###################################################
# XLTOOL
# Author       : Adeebdanish
# Version      : 2.0
# Description  : 
###################################################

import os
import sys
from os.path import exists

import openpyxl
from util import locio


class file_handle:

    def __init__(self):

        if sys.platform == "linux":
            r = exists("/storage/emulated/0/Xltool/")
            if not r:
                os.mkdir("/storage/emulated/0/Xltool/")

    def file_inp(self, path):

        try:
            self.book = openpyxl.load_workbook(path)
            self.worksheets = len(self.book.worksheets)
            self.path = path

        except FileNotFoundError:
            print(f"[!] file not found : '{path}'")
            quit()
        except openpyxl.utils.exceptions.InvalidFileException:
            print(f"[!] file not supported : '{path}'")
            quit()

    def get_sheet_name(self):

        sheet_names = self.book.sheetnames
        print("\033[1;32m[~] sheets: ", end="")
        print(*sheet_names, end="", sep="\n[~] ")
        print("\033[0m")

    def sheet_inp(self, sheet_name):

        try:
            self.sheet = self.book[sheet_name]
            self.sheet_name = sheet_name
        except KeyError:
            print(f"worksheet not found : '{sheet_name}'")
            quit()

    def get_file_name(self, path):
        if "/" in path:
            return path.split("/")[-1]
        return path

    def save_file(self):

        file_name = self.get_file_name(self.path)
        path = "/storage/emulated/0/Xltool/" + file_name
        self.book.save(path)
        print("")
        print()
        print(f"[*] file Saved to : Xltool/{file_name}")
        self.book.close()


class dupe:

    def __init__(self, sheet):

        self.sheet = sheet

    def full_row(self):

        dupe_lst = []

        for test_row in self.sheet:
            if [cell.value for cell in test_row] == [None for n in range(0, len(test_row))]:
                continue
            for check_row in self.sheet:
                if [str(cell.value).strip() for cell in test_row] == [str(cell.value).strip() for cell in check_row]:
                    if test_row[0].row in dupe_lst:
                        continue
                    if test_row[0].row != check_row[0].row:
                        print(f"\033[1;32m[~] duplicate found : {test_row[0].row} > {check_row[0].row}\033[0m")
                        dupe_lst.append(check_row[0].row)
        return dupe_lst

    def by_header(self, header):

        temp_dict = {}
        dupe_lst = []
        header_index = 0

        for row in self.sheet:
            lst = [cell.value for cell in row]
            if header in lst:
                header_index = lst.index(header)

        for row in self.sheet:
            cell = row[header_index]
            if str(cell.value).strip() in temp_dict:
                print(
                    f"\033[1;32m[~] duplicates found : {temp_dict[str(cell.value).strip()]} > {cell.row}  [ {str(cell.value).strip()} ]\033[0m")
                dupe_lst.append(cell.row)
            else:
                if cell.value != None:
                    temp_dict[str(cell.value).strip()] = cell.row

        return dupe_lst

    def by_col(self, col):

        dupe_lst = []
        temp_dict = {}

        for row in self.sheet:
            for cell in row:
                if col.upper() in cell.coordinate:
                    if cell.value in temp_dict.keys():
                        print(
                            f"\033[1;32m[~] duplicates found : {temp_dict[cell.value]} > {cell.row}  [ {cell.value} ]\033[0m")
                        dupe_lst.append(cell.row)
                    else:
                        if cell.value != None:
                            temp_dict[cell.value] = cell.row
        return dupe_lst


class print_sheet:

    def __init__(self, sheet):

        self.sheet = sheet

        self.content_to_dict()

    def content_to_dict(self):

        self.content_dict = {0: [col for col in range(1, len(self.sheet[1]) + 1)]}
        self.max_len = 0

        for row in self.sheet:
            self.content_dict[row[0].row] = []
            for cell in row:
                value = cell.value
                if value == None:
                    value = ""
                value = str(value).strip()
                if len(str(value)) > self.max_len:
                    self.max_len = len(value)
                self.content_dict[cell.row].append(value)

    def lst(self):
        for row, values in self.content_dict.items():
            if row == 0: continue
            for value in values:
                print(str(value).ljust(self.max_len + 2), end="")
            print()

    def table(self):
        for row, values in self.content_dict.items():

            space = len(str(max(self.content_dict.keys()))) + 2
            print(f" [{str(row).center(space)}", end="")
            for value in values:
                space = int(self.max_len) + 2
                if value == None:
                    value = ""
                print(f"| {str(value).ljust(space)}", end="")
            print("]")

    def headers(self):

        head_values = 0
        head_row = 0
        max_len = 0

        for row, values in self.content_dict.items():
            if row == 0: continue
            lst = []
            for value in values:
                if value != "":
                    lst.append(value)
            if len(lst) > max_len:
                head_values = lst
                head_row = row
                max_len = len(lst)

        return head_values, head_row

    def json(self):

        head_values, head_row = self.headers()
        if head_values != 0:
            for row, values in self.content_dict.items():
                if row == 0: continue
                if row == head_row: continue
                print("{ row: " + str(row), end=", ")
                for head, value in zip(head_values, values):
                    if head == "": continue
                    print("\033[0;33m" + str(head) + "\033[0m :" + str(value).strip(), end=", ")
                print("}")
        else:
            locio.print_er("can't find headers")


class remove:

    def __init__(self, sheet):

        self.sheet = sheet

    def delete_row(self, lst):

        count = 0
        for row in lst:
            self.sheet.delete_rows(row - count)
            count += 1

    def blank(self):

        row_lst = []

        for row in self.sheet:
            count = 0
            for cell in row:
                if cell.value == None:
                    count += 1
            if len(row) == count:
                row_lst.append(row[0].row)
        print("")
        self.delete_row(row_lst)
        print("[~] Blank rows removed")
        print()

    def dupe(self, dupe_lst):

        print()
        self.delete_row(dupe_lst)
        print("[~] Duplicates removed")
        print()


class search:

    def __init__(self, content, txt, headers):

        self.content = content
        self.txt = txt
        self.headers = headers

    def full(self):

        for row, values in self.content.items():
            for value in values:
                if str(value) == self.txt:
                    print("{ row: " + str(row), end=", ")
                    for head, value in zip(self.headers, values):
                        if head == "": continue
                        print("\033[0;33m" + str(head) + "\033[0m: " + str(value).strip(), end=", ")
                    print("}")

    def by_header(self, header):

        head_index = self.headers.index(header)
        for row, values in self.content.items():
            if str(values[head_index]) == self.txt:
                print("{ row: " + str(row), end=", ")
                for head, value in zip(self.headers, values):
                    if head == "": continue
                    print("\033[0;33m" + str(head) + "\033[0m :" + str(value).strip(), end=", ")
                print("}")

    def by_col(self, sheet, col):

        for row in sheet:
            for cell in row:
                if col.upper() not in cell.coordinate: continue
                if cell.value == None: continue
                if str(cell.value) == self.txt:
                    values = [cell.value for cell in self.sheet[cell.row]]

                    print("{ row: " + str(row[0].row), end=", ")
                    for head, value in zip(self.headers, values):
                        if head == "": continue
                        print("\033[0;33m" + str(head) + "\033[0m: " + str(value).strip(), end=", ")
                    print("}")


class main(file_handle, dupe, print_sheet, remove, search):

    def __init__(self, argv):

        file_handle.__init__(self)

        self.argv = argv

    def file_init(self):

        argv = self.argv
        if "-wb" in argv:
            path = argv[argv.index("-wb") + 1]
        else:
            print("[!] file not provided ")
            quit()

        file_handle.file_inp(self, path)

        if "-s" in argv:
            sheet_name = argv[argv.index("-s") + 1]
            if sheet_name == "SN":
                file_handle.get_sheet_name(self)
                quit()
        else:
            print("[!] sheet not provided ")
            quit()

        file_handle.sheet_inp(self, sheet_name)

    def dupe_tool(self):

        argv = self.argv

        dupe.__init__(self, self.sheet)

        try:
            condition = argv[argv.index("-d") + 1]
            head = condition.split("=")[0]
        except:
            head = "def"

        conditions = {
            "H": dupe.by_header,
            "C": dupe.by_col,
        }

        if head in conditions:

            param = condition.split("=")[1]
            conditions[head](self, param)

        else:

            dupe.full_row(self)

    def display(self):

        argv = self.argv

        try:
            mode = argv[argv.index("-p") + 1]
        except:
            mode = "def"

        modes = {
            "json": print_sheet.json,
            "def": print_sheet.json,
            "table": print_sheet.table,
            "list": print_sheet.lst,
        }

        if mode in modes:

            modes[mode](self)

        else:
            print(f"[!] Err : print mode not found : {mode}")

    def get_dupe_lst(self, condition):

        conditions = {
            "H": dupe.by_header,
            "C": dupe.by_col,
        }

        head = condition.split("=")[0]
        if head in conditions:

            param = condition.split("=")[1]
            dupe_lst = conditions[head](self, param)

        else:
            return dupe.full_row(self)

        return dupe_lst

    def remove_tool(self):

        argv = self.argv
        remove.__init__(self, self.sheet)

        if "-rb" in argv:
            remove.blank(self)

        if "-rd" in argv:

            try:
                condition = argv[argv.index("-rd") + 1]
            except:
                condition = "def"
            dupe_lst = self.get_dupe_lst(condition)

            remove.dupe(self, dupe_lst)

    def search_tool(self):
        try:
            txt = self.argv[self.argv.index("-f") + 1]
        except:
            print("[!] Err: Text not provided ")
            quit()

        header, _ = print_sheet.headers(self)
        search.__init__(self, self.content_dict, txt, header)

        try:
            condition = self.argv[self.argv.index("-f") + 2]
        except:
            condition = "def"

        if "H" in condition:
            param = condition.split("=")[1]
            search.by_header(self, param)

        if "C" in condition:

            param = condition.split("=")[1]
            search.by_col(self, self.sheet, param)

        else:

            search.full(self)

    def __call__(self):

        self.file_init()
        print_sheet.__init__(self, self.sheet)
        argv = self.argv

        if "-d" in argv:
            self.dupe_tool()

        if "-rb" in argv or "-rd" in argv:
            self.remove_tool()

        if "-o" in argv:
            file_handle.save_file(self)

        if "-f" in argv:
            self.search_tool()

        if "-p" in argv:
            self.display()


class xltool(file_handle, print_sheet, remove, search):

    def __init__(self):
        file_handle.__init__(self)

    def find(self):
        print_sheet.__init__(self, self.sheet)

        txt = input("content: ")
        print()
        header, _ = print_sheet.headers(self)
        search.__init__(self, self.content_dict, txt, header)

        search.full(self)


if __name__ == "__main__":
    tool = main(sys.argv)
    tool()
