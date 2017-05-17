from .prints import fix_newline_signs

indent = "    "
comment = "# "

# generates text for row data file
def generate_standard_data_file_content(data_dictionary, data_content):
    result = ""
    for row in data_content:
        if type(row) is str:
            result += comment + row + "\n"
        elif type(row) is list:
            comments = True
            for element in row:
                if element == "":
                    comments = False
                    # ends of comments
                else:
                    if comments:
                        # add comment
                        result += indent + comment + element + "\n"
                    else:
                        # add variable
                        # handle with dot-walking
                        splitted = element.split(".")
                        to_add = dict(data_dictionary)
                        for key in splitted:
                            to_add = to_add[key]
                        result += indent + element + " = " + to_add + "\n"

            result += "\n"
    return result

# returns 'data_content' for 'generate_standard_data_file_content' function
def generate_standard_data_file_schema(file_content):
    result = []
    file_content = fix_newline_signs(file_content)
    line_content = file_content.split("\n")

    saved_field_data = []
    status = 0
    # status:
        # 0 - nothing or end of section label
        # 1 - field comment
        # 2 - field content
    for line in line_content:
        if line == '': # empty line
            if status > 0:
                result.append(saved_field_data)
                saved_field_data = []
            status = 0
        elif line.startswith(comment):
            if status > 0:
                result.append(saved_field_data)
                saved_field_data = []
            result.append(line[len(comment):])
            status = 0
        elif line.startswith(indent): # comment
            if line.startswith(indent + comment):
                comment_line = line[len(indent + comment):]
                if status in (0, 1):
                    saved_field_data.append(comment_line)
                else:
                    result.append(saved_field_data)
                    saved_field_data = [comment_line]
                status = 1
            else:
                keyword = line[len(indent):].split("=")[0].strip()
                if status in (0, 1):
                    saved_field_data.append("")
                saved_field_data.append(keyword)
                status = 2
    if status > 0:
        result.append(saved_field_data)
        status = 0
    return result

# returns dictionary with all key-values from file
def parse_data_to_dict(string):
    result = {}
    lines = string.split("\n")
    for line in lines:
        if line.startswith(indent) and not line.startswith(indent+comment):
            splitted = line.split("=")
            key = splitted[0].strip()
            value = splitted[1].strip()
            result[key] = value
    return result