import os

import docx2txt

from views.utils import get_name_of_file

skipped_files = []


def conver_word_to_text(input_folder, output_folder):
    if not os.path.exists(input_folder):
        return "Input folder doesn't exist"

    if not os.path.exists(output_folder):
        return "Output folder doesn't exist"

    for file in os.listdir(input_folder):
        arr = file.split(".")
        filename = get_name_of_file(file)
        extension = arr[-1]
        if extension not in ["doc", "docx"]:
            print(f"{file} skipped")
            continue
        try:
            text = docx2txt.process(os.path.join(input_folder, file))
            with open(os.path.join(output_folder, filename + ".txt"), "w") as txt_file:
                txt_file.write(text)
        except Exception as ex:
            print(ex)
            skipped_files.append(file)

    print(skipped_files)
    return "Success"
