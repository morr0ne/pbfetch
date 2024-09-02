from re import sub, fullmatch, compile
from subprocess import Popen, PIPE

# current_loading_spinner = "/"


def get_console_width():
    console_width = Popen(["tput", "cols"], stdout=PIPE)
    console_width = int(float(console_width.communicate()[0].strip()))

    return console_width


console_width = get_console_width()


def replace_keyword(template, keyword, stat):
    template = template.splitlines()
    replaced_template = []

    for line in template:
        line = "<rgb(255,255,255)></rgb>" + line.rstrip()

        # if no keyword add line to replace template and continue
        if keyword not in line:
            replaced_template.append(line)
            continue

        # # keyword to init stretching to the right
        # stretch = "$stretch"

        # # check if keyword is to stretch line to console width
        # if stretch in line:
        #     # split line at keyword
        #     split_line = line.split(stretch)

        #     # use char directly to the left of keyword as char
        #     copy_char = split_line[0][-1]

        #     difference = console_width - len(line)

        #     # if keyword at very beginning or very end of line
        #     if len(split_line) == 1:
        #         # if difference is 0 or less, just remove stretch tag
        #         if difference > 0:
        #             line = line.replace(stretch, copy_char * (difference))
        #         else:
        #             line = line.replace(stretch, "")

        #         replaced_template.append(line)
        #         continue

        #     # if keyword NOT at very beginning or end then stretch
        #     first_half = split_line[0]
        #     second_half = split_line[1]

        #     second_half = (copy_char * difference) + second_half

        #     line = first_half + second_half
        #     replaced_template.append(line)
        #     continue

        is_error = False

        # Store the length of what we are using to replace it
        stat_len = len(stat)

        if stat == "ERROR":
            is_error = True
            stat = "<rgb(255,0,0)>ERROR</rgb>"

        # Split the string on the word
        split_line = line.split(keyword)

        split_line[1] = split_line[1].ljust(stat_len)

        # Measure the length of the second element in the split
        before_strip_length = len(split_line[1])

        # Remove the whitespace of the second element in the split
        split_line[1] = split_line[1].lstrip()

        # Measure the length after stripping to figure out how
        #   many whitespaces we removed
        after_strip_length = len(split_line[1])

        # Use those values to calculate the whitespaces
        whitespace_count = before_strip_length - after_strip_length

        # Figure out the max length the replacement can be
        keyword_length = len(keyword)
        max_allowed_length = keyword_length + whitespace_count

        # handle error color tags conflicting with formatting
        if is_error:
            max_allowed_length += 20

        # Make sure our replaceText isn't too long
        stat = stat.ljust(max_allowed_length, " ")

        if stat_len > max_allowed_length:
            stat = stat[:max_allowed_length]

        # Pad replaceText with spaces to match the whitespace we removed
        # insert color reset bytecode at the beginning of each line
        # to prevent buggy behavior
        replaced_template.append(split_line[0] + stat + split_line[1])

    template = "\n".join(replaced_template)

    return template


def split_at_length(line):
    START_FLAG = "<"
    END_FLAG = ">"

    COMMAND_PATTERNS = [
        compile(
            r"rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)"
        ),
        compile(r"\/rgb"),
    ]

    current_count = 0
    skip_count = 0
    return_buffer = ""
    line_length = len(line)

    # Loop through each character in the string one at a time
    for i in range(0, line_length):
        # Capture the current character we are looking at
        current_char = line[i]

        # Add that current character to our return buffer
        return_buffer += current_char

        # Allow for us to skip parts of the text
        if skip_count > 0:
            skip_count -= 1
            continue

        # TODO: add here a conditional that checks if the last
        #   few characters in the string match a keyword, if so
        #   then add the stat value to the buffer and return buffer

        # If the current character is the starting flag we need to check
        #   if the following character are a command
        if current_char == START_FLAG:
            # Create a buffer to push the next characters to
            buffer = ""

            # Loop through the string from the current location to
            #   the next END_FLAG capturing the characters as we go
            for j in range(1, line_length - i):
                # Capture the current character at this index
                buffer_char = line[i + j]

                # If the captured character is our end flag then stop
                if buffer_char == END_FLAG:
                    break

                # Add it to our buffer
                buffer += buffer_char

            # Check to see if buffer is a command
            if fullmatch(COMMAND_PATTERNS[0], buffer, flags=0) or fullmatch(
                COMMAND_PATTERNS[1], buffer, flags=0
            ):
                # print(buffer)  # debug
                # Skip the characters that exist in our command
                skip_count = len(buffer) + len(END_FLAG)
                # We KNOW this is a command tag and we don't want to count it, so
                #   continue out of this for loop cycle before the count
                continue

        # count
        current_count += 1

        # IF we have reached our max length, stop counting and return what we have
        if current_count >= console_width:
            break

    return return_buffer


def final_touches(return_text):
    return_text = sub(
        r"<rgb\(\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*,\s*([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\s*\)\>",
        r"[38;2;\g<1>;\g<2>;\g<3>m",
        return_text,
    )
    return_text = str(sub(r"\<\/rgb\>", "[39m", return_text))

    return return_text


def replace_keywords(template, stats_dict):
    # Replace all of the keywords in the dictionary
    for keyword, stat in stats_dict.items():
        if stat is None:
            stat = "ERROR"

        template = replace_keyword(template, keyword, stat)

    # Make sure each line does not exceed max_line_length
    lines = template.splitlines()

    for i in range(0, len(lines)):
        lines[i] = split_at_length(lines[i])

    template = "\n".join(lines)
    return_text = final_touches(template)

    return return_text
