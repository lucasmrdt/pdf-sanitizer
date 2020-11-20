#!/usr/bin/env python3

import PyPDF2
import sys
import difflib

TITLE_THRESHOLD = .5
CONTENT_THRESHOLD = .8

if not len(sys.argv) == 3:
    print(f'{sys.argv[0]} input_file.pdf output_file', file=sys.stderr)
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

input_file = None
try:
    input_file = open(INPUT_FILE, 'rb')
except OSError:
    print(f'❌  file {INPUT_FILE} not found', file=sys.stderr)
    sys.exit(1)

pdf_input = PyPDF2.PdfFileReader(input_file)
pdf_output = PyPDF2.PdfFileWriter()


def diff(content1, content2):
    return difflib.SequenceMatcher(None, content1, content2)


def has_deleted_item(diff):
    for operation, *_ in diff.get_opcodes():
        if operation == 'delete':
            return True
    return False


def get_title(content):
    return content.split('\n')[0]


def get_content(content):
    return content.replace(get_title(content), '').strip()


def has_content(content):
    return len(get_content(content)) != 0


print(' 🔄  Processing ...', end='\r')

prev_page = pdf_input.getPage(0)
for i in range(1, pdf_input.getNumPages()):
    current_page = pdf_input.getPage(i)
    current_content = current_page.extractText()
    prev_content = prev_page.extractText()

    diff_title = diff(get_title(prev_content), get_title(current_content))
    diff_content = diff(get_content(prev_content),
                        get_content(current_content))
    title_has_changed = diff_title.ratio() < TITLE_THRESHOLD
    content_has_changed = (diff_content.ratio() < CONTENT_THRESHOLD
                           and (has_deleted_item(diff_content) or len(prev_content) > len(current_content)))

    # print(f'[PREV]{prev_content}[PREV]')
    # print(f'[NEXT]{current_content}[NEXT]')
    # print(i, content_has_changed, diff_content.get_opcodes())

    if has_content(prev_content) and (title_has_changed or content_has_changed):
        pdf_output.addPage(prev_page)

    prev_page = current_page

pdf_output.addPage(prev_page)

with open(sys.argv[2], 'wb') as f:
    pdf_output.write(f)

print(f'✅  Your file has been optimized at {OUTPUT_FILE}')
