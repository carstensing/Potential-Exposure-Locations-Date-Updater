from dates import Date
import re

# Gets the number of lines for two files.
# If their length is not equal then -1 is returned.
def get_num_lines(file_1_path: str, file_2_path: str) -> int:
    file_1_num_lines = 0
    file_2_num_lines = 0
    with open(file_1_path, "r") as file_1, open(file_2_path, "r") as file_2:
        f1_line = "f1"
        f2_line = "f2"

        while f1_line != "":
            f1_line = file_1.readline()
            file_1_num_lines += 1
            if f1_line and f1_line[-1] != "\n":
                break

        while f2_line != "":
            f2_line = file_2.readline()
            file_2_num_lines += 1
            if f2_line and f2_line[-1] != "\n":
                break

    if file_1_num_lines == file_2_num_lines:
        return file_1_num_lines
    else:
        return -1

# Takes takes a string of dates and returns them as a list[str]
def split_dates(line: str, max_split: int = 0) -> "list[str]":
    # cleans up the end of the string-list of commas, spaces and newlines
    line = re.sub("(^ *,? *)|(,* *\n*$)", "", line)

    # splits the string into a list of strings
    return re.split(", *", line, maxsplit=max_split) if len(line) >= 6 else []

# Gets the number of dates more recent than the comparison date.
# Dates are listed from most to least recent.
def num_newer_dates(list: "list[str]", comparison_date: Date, inclusive: bool = False) -> int:
    if list == []:
        return 0

    previous_date = Date("12/31/99")
    num_newer_dates = 0
    for date in list:
        try:
            cur_date = Date(date)
        except:
            raise Exception(date + " is an invalid Date.\n")
        
        if previous_date < cur_date:
            raise Exception("Dates are not in order from newest to oldest.\n")
        if inclusive and cur_date >= comparison_date:
            num_newer_dates += 1
        elif not inclusive and cur_date > comparison_date:
            num_newer_dates += 1
        previous_date = cur_date
        
    return num_newer_dates

# Gets the output string for one line of current_dates_updated.txt and the dates that need to be archived.
def get_cur_output_string_and_invalid_dates(cur_dates_line: str, comparison_date: Date) -> "tuple[bool, list[str]]":
    cur_dates_list = split_dates(cur_dates_line)
    # if no dates to update, change nothing
    invalid_dates = []
    if not cur_dates_list:
        cur_output_string = "\n"
    else:
        try:
            separator_index = num_newer_dates(cur_dates_list, comparison_date, inclusive=True)
        except Exception as e:
            raise Exception("in cur_dates.txt. " + e.args[0])  

        # write still valid dates to current_dates_updated.txt
        valid_dates = cur_dates_list[:separator_index]

        if valid_dates:
            cur_output_string = "".join((x+", ") for x in valid_dates)[:-2] + "\n"
        else:
            cur_output_string = "\n"

        # check to make sure not adding duplicates to archived_dates_updated.txt
        invalid_dates = cur_dates_list[separator_index:]
    return (cur_output_string, invalid_dates)

# Gets the output string for one line of archived_dates_updated.txt.
def get_arc_output_string(arc_dates_line: str, invalid_dates: "list[str]") -> str:
    arc_dates_list = split_dates(arc_dates_line, 1)
    
    if not invalid_dates:
        arc_output_string = arc_dates_line
    elif not arc_dates_list:
        arc_output_string = "".join((x+", ") for x in invalid_dates)[:-2]  + "\n"
    else:
        # get most recent archived date
        try:
            newest_arc_date = Date(arc_dates_list[0])
        except Exception as e:
            raise Exception("in arc_dates.txt. " + e.args[0])   
        
        # get the number of dates we don"t want to write
        try:
            separator_index = num_newer_dates(invalid_dates, newest_arc_date)
        except Exception as e:
            raise Exception("in cur_dates.txt. " + e.args[0])        

        # write all invalid dates
        if separator_index == len(invalid_dates):
            arc_output_string = "".join((x+", ") for x in invalid_dates) + arc_dates_line
        # write none of the invalid dates
        elif separator_index == 0:
            arc_output_string = arc_dates_line
        # write a subset of the invalid dates
        else:
            arc_output_string = "".join((x+", ") for x in invalid_dates[:separator_index]) + arc_dates_line
    return arc_output_string

def main():
    INPUT_FILE_1 = "./Input Files/current_dates.txt"
    INPUT_FILE_2 = "./Input Files/archived_dates.txt"
    OUTPUT_FILE_1 = "./Output Files/current_dates_updated.txt"
    OUTPUT_FILE_2 = "./Output Files/archived_dates_updated.txt"
    LOG_FILE = "./log.txt"

    try:
        log = open(LOG_FILE, "w")
        
        # vars
        today = Date.today()
        log.write("Today: " + str(today) + "\n")

        sub_14 = Date.fourteen_days_ago()
        log.write("14 days ago: " + str(sub_14) + "\n")

        # check that both files contain the same amount of lines
        num_lines_in_cur_dates = get_num_lines(INPUT_FILE_1, INPUT_FILE_2)
        if num_lines_in_cur_dates == -1:
            raise Exception("Error: Input files have an unequal number of lines")
        else:
            log.write("Num lines: " + str(num_lines_in_cur_dates) + "\n")

        try:
            # open files
            cur_dates_file = open(INPUT_FILE_1, "r")
            arc_dates_file = open(INPUT_FILE_2, "r")

            cur_dates_file_updated = open(OUTPUT_FILE_1, "w")
            arc_dates_file_updated = open(OUTPUT_FILE_2, "w")
            
            counter = 0
            while(counter < num_lines_in_cur_dates):
                cur_dates_line = cur_dates_file.readline()
                arc_dates_line = arc_dates_file.readline()
                
                try:
                    temp = get_cur_output_string_and_invalid_dates(cur_dates_line, sub_14)
                    cur_output_string = temp[0]
                    cur_dates_file_updated.write(cur_output_string)
                    invalid_dates = temp[1]

                    arc_output_string = get_arc_output_string(arc_dates_line, invalid_dates)
                    arc_dates_file_updated.write(arc_output_string)
                except Exception as e:
                    # raise e
                    log.write("Error on line " + str(counter+1) + " " + e.args[0])

                counter += 1
        finally:
            cur_dates_file.close()
            arc_dates_file.close()

            cur_dates_file_updated.close()
            arc_dates_file_updated.close()
    except Exception as exception:
        # raise e
        print(exception.args[0])
        log.write(exception.args[0] + "\n")
    finally:
        print("Execution complete.")
        log.write("Execution completed successfully.\n")
        log.close()

if __name__ == "__main__":
    main()