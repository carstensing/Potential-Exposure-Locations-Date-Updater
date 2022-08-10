# open files

# iterate through each both at the same time

# update each one respectively

from dates import Date
import re

input_file_1 = "./Input Files/current_dates.txt"
input_file_2 = "./Input Files/archived_dates.txt"
output_file_1 = "./Output Files/current_dates_updated.txt"
output_file_2 = "./Output Files/archived_dates_updated.txt"

#
def equal_num_lines(file_1_path, file_2_path):
    """
    :type nums: string
    :type target: string
    :rtype: int
    """
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

def main():
    log = open("./log.txt", 'w')
    try:
        # vars
        today = Date.today()
        log.write("Today: " + str(today) + '\n')

        sub_14 = Date.fourteen_days_ago()
        log.write("14 days ago: " + str(sub_14) + '\n')

        # check that both files contain the same amount of lines
        num_lines_in_cur_dates = equal_num_lines(input_file_1, input_file_2)
        if num_lines_in_cur_dates == -1:
            raise Exception("Error: Input files have an unequal number of lines")

        # open files
        cur_dates_file = open(input_file_1, 'r')
        arc_dates_file = open(input_file_2, 'r')

        cur_dates_file_updated = open(output_file_1, 'w')
        arc_dates_file_updated = open(output_file_2, 'w')
        
        counter = 0

        while(counter < num_lines_in_cur_dates):
            cur_dates_line = cur_dates_file.readline()
            cleaned_cur_dates_line = re.sub("(,* *\n*$)", '', cur_dates_line)
            cur_dates_list = re.split(", ?", cleaned_cur_dates_line) if len(cleaned_cur_dates_line) > 0 else None

            arc_dates_line = arc_dates_file.readline()
            cleaned_arc_dates_line = re.sub("(,* *\n*$)", '', arc_dates_line)
            arc_dates_list = re.split(", ?", cleaned_arc_dates_line, maxsplit=1) if len(cleaned_arc_dates_line) > 0 else None

            if cur_dates_list is None:
                cur_dates_file_updated.write('\n')
                arc_dates_file_updated.write(arc_dates_line)
            else:
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

    except Exception as exception:
        print(exception.args[0])
        log.write(exception.args[0] + '\n')
        pass
    else:
        pass
    finally:
        cur_dates_file.close()
        arc_dates_file.close()

        cur_dates_file_updated.close()
        arc_dates_file_updated.close()
        log.close()
    
        print("Execution complete.")

if __name__ == '__main__':
    main()