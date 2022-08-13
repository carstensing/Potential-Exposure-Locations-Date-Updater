from dates import Date
import re

INPUT_FILE_1 = "./Input Files/current_dates.txt"
INPUT_FILE_2 = "./Input Files/archived_dates.txt"
OUTPUT_FILE_1 = "./Output Files/current_dates_updated.txt"
OUTPUT_FILE_2 = "./Output Files/archived_dates_updated.txt"

# Gets the number of lines for two files.
# If their length is not equal then -1 is returned.
# TODO fix line with EOF not being counted
def get_num_lines(file_1_path: str, file_2_path: str) -> int:
    file_1_num_lines = 0
    file_2_num_lines = 0
    with open(file_1_path, 'r') as file_1, open(file_2_path, 'r') as file_2:
        for line in file_1:
            file_1_num_lines += 1

        for line in file_2:
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
                    # TODO get_separator_index()
                    separator_index = 0
                    for date in cur_dates_list:
                        try:
                            if Date(date) < sub_14:
                                break
                            else:
                                separator_index += 1
                        except Exception as e:
                            # print(e)
                            # print("Error on line "+ str(counter+1) +" in cur_dates.txt\n")
                            log.write("Error on line " + str(counter+1) + " in cur_dates.txt\n")

                    valid_dates = cur_dates_list[:separator_index]
                    cur_dates_file_updated.write(''.join((x+", ") for x in valid_dates) + '\n')

                    # check to make sure not adding duplicates
                    invalid_dates = cur_dates_list[separator_index:] if len(cur_dates_list[separator_index:]) > 0 else None

                    if arc_dates_list is None and invalid_dates is not None:
                        arc_dates_file_updated.write(''.join((x+", ") for x in invalid_dates) + '\n')
                    elif arc_dates_list is not None:
                        try:
                            last_arc_date = Date(arc_dates_list[0])
                        except Exception as e:
                            # print(e)
                            # print("Error on line "+ str(counter+1) +" in arc_dates.txt\n")
                            log.write("Error on line "+ str(counter+1) +" in arc_dates.txt\n")

                        if invalid_dates is None:
                            arc_dates_file_updated.write(arc_dates_line)
                        else: 
                            separator_index = 0
                            for invalid_date in reversed(invalid_dates):
                                try:
                                    # print(invalid_date)
                                    if Date(invalid_date) <= last_arc_date:
                                        separator_index += 1
                                    else:
                                        break
                                except Exception as e:
                                    # print(e)
                                    # print("Error on line "+ str(counter+1) +" in cur_dates.txt\n")
                                    log.write("Error on line "+ str(counter+1) +" in cur_dates.txt\n")           

                            if separator_index == 0:
                                arc_dates_file_updated.write(''.join((x+", ") for x in invalid_dates) + arc_dates_line)
                            elif separator_index == len(invalid_dates):
                                arc_dates_file_updated.write(arc_dates_line)
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
            log.close()

            print("Execution complete.")

    except Exception as exception:
        print(exception.args[0])
        log.write(exception.args[0] + '\n')

if __name__ == '__main__':
    main()