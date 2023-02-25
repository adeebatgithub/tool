

class dupe_tools():
    
    def __init__(self, sheet):
        self.sheet = sheet
        
    def full_row(self):
            
        dupe_lst = []
            
        for test_row in self.sheet:
            if [cell.value for cell in test_row] == [None for n in range(0,len(test_row))]:
                continue
            for check_row in self.sheet:
                if [cell.value for cell in test_row] == [cell.value for cell in check_row]:
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
            if cell.value in temp_dict.keys():
                print(f"\033[1;32m[~] duplicates found : {cell.row} > {temp_dict[cell.value]}  [ {cell.value} ]\033[0m")
                dupe_lst.append(cell.row)
            else:
                if cell.value != None:
                    temp_dict[cell.value] = cell.row
                    
        return dupe_lst