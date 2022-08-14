from dates import Date
import re

INPUT_FILE_1 = "./Input Files/current_dates.txt"
INPUT_FILE_2 = "./Input Files/archived_dates.txt"
OUTPUT_FILE_1 = "./Output Files/current_dates_updated.txt"
OUTPUT_FILE_2 = "./Output Files/archived_dates_updated.txt"

# Gets the number of lines for two files.
# If their length is not equal then -1 is returned.
def get_num_lines(file_1_path: str, file_2_path: str) -> int:
    file_1_num_lines = 0
    file_2_num_lines = 0
    with open(file_1_path, 'r') as file_1, open(file_2_path, 'r') as file_2:
        f1_line = "f1"
        f2_line = "f2"

        while f1_line != "" and f2_line != "":
            f1_line = file_1.readline()
            file_1_num_lines += 1
            f2_line = file_2.readline()
            file_2_num_lines += 1

    if file_1_num_lines == file_2_num_lines:
        return file_1_num_lines
    else:
        return -1

# Takes takes a string of dates and returns them as a list[str]
def split_dates(line: str, max_split: int = 0) -> 'list[str]':
    # cleans up the end of the string-list of commas, spaces and newlines
    line = re.sub("(^ *,? *)|(,* *\n*$)", '', line)

    # splits the string into a list of strings
    return re.split(", *", line, maxsplit=max_split) if len(line) >= 6 else None

# Gets the number of dates more recent than the comparison date.
# Dates are listed from most to least recent.
def num_newer_dates(list: 'list[str]', comparison_date: Date, inclusive: bool = False) -> int:
    if list == None:
        raise Exception("Expected [], given None.\n")
    elif list == []:
        return 0

    separator_index = 0
    for date in list:
        try:
            if inclusive and Date(date) >= comparison_date:
                separator_index += 1
            elif not inclusive and Date(date) > comparison_date:
                separator_index += 1
        except:
            raise Exception(date + " is an invalid Date.\n")
    return separator_index

def main():
    try:
        log = open("./log.txt", 'w')
        
        # vars
        today = Date.today()
        log.write("Today: " + str(today) + '\n')

        sub_14 = Date.fourteen_days_ago()
        log.write("14 days ago: " + str(sub_14) + '\n')

        # check that both files contain the same amount of lines
        num_lines_in_cur_dates = get_num_lines(INPUT_FILE_1, INPUT_FILE_2)
        if num_lines_in_cur_dates == -1:
            raise Exception("Error: Input files have an unequal number of lines")
        else:
            log.write("Num lines: " + str(num_lines_in_cur_dates) + '\n')

        try:
            # open files
            cur_dates_file = open(INPUT_FILE_1, 'r')
            arc_dates_file = open(INPUT_FILE_2, 'r')

            cur_dates_file_updated = open(OUTPUT_FILE_1, 'w')
            arc_dates_file_updated = open(OUTPUT_FILE_2, 'w')
            
            counter = 0
            while(counter < num_lines_in_cur_dates):
                cur_dates_line = cur_dates_file.readline()
                cur_dates_list = split_dates(cur_dates_line)

                arc_dates_line = arc_dates_file.readline()
                arc_dates_list = split_dates(arc_dates_line, 1)

                # if no dates to update, change nothing
                if cur_dates_list is None:
                    cur_dates_file_updated.write('\n')
                    arc_dates_file_updated.write(arc_dates_line)
                else:
                    separator_index = 0
                    try:
                        separator_index = num_newer_dates(cur_dates_list, sub_14, inclusive=True)
                    except Exception as e:
                        log.write("Error on line " + str(counter+1) + " in cur_dates.txt. " + e.args[0])

                    # write still valid dates to current_dates_updated.txt
                    valid_dates = cur_dates_list[:separator_index]
                    if valid_dates:
                        cur_dates_file_updated.write(''.join((x+", ") for x in valid_dates)[:-2] + '\n')
                    else:
                        cur_dates_file_updated.write('\n')

                    # check to make sure not adding duplicates to archived_dates_updated.txt
                    invalid_dates = cur_dates_list[separator_index:] if len(cur_dates_list[separator_index:]) > 0 else None

                    if arc_dates_list is None and invalid_dates is not None:
                        arc_dates_file_updated.write(''.join((x+", ") for x in invalid_dates)[:-2]  + '\n')
                    elif arc_dates_list is not None:
                        try:
                            last_arc_date = Date(arc_dates_list[0])
                        except Exception as e:
                            # print(e)
                            # print("Error on line "+ str(counter+1) +" in arc_dates.txt\n")
                            log.write("Error on line " + str(counter+1) + " in arc_dates.txt. date" + arc_dates_list[0] + " is an invalid Date.\n")

                        if invalid_dates is None:
                            arc_dates_file_updated.write(arc_dates_line)
                        else: 
                            separator_index = 0
                            try:
                                separator_index = num_newer_dates(reversed(invalid_dates), last_arc_date)
                            except Exception as e:
                                log.write("Error on line " + str(counter+1) + " in cur_dates.txt. " + e.args[0])        

                            # write all invalid dates
                            if separator_index == 0:
                                arc_dates_file_updated.write(''.join((x+", ") for x in invalid_dates) + arc_dates_line)
                            # write none of the invalid dates
                            elif separator_index == len(invalid_dates):
                                arc_dates_file_updated.write(arc_dates_line)
                            # write a subset of the invalid dates
                            else:
                                arc_dates_file_updated.write(''.join((x+", ") for x in invalid_dates[:-separator_index]) + arc_dates_line)
                        
                counter += 1
                # if counter > 20:
                #     break
        finally:
            cur_dates_file.close()
            arc_dates_file.close()

            cur_dates_file_updated.close()
            arc_dates_file_updated.close()

            print("Execution complete.")
            log.write("Execution completed successfully.\n")
            log.close()

    except Exception as exception:
        print(exception.args[0])
        log.write(exception.args[0] + '\n')

if __name__ == '__main__':
    main()