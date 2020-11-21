import difflib
import pathlib
import argparse

from .utils import fail_with_message, progress_with_message, success_with_message

try:
    import PyPDF2
except ImportError:
    fail_with_message(
        'Please install required dependencies before using this package.\n\t> pip3 install -r requirements.txt --user')


def parse_file(path: str):
    if not pathlib.Path(path).exists():
        raise argparse.ArgumentTypeError('invalid file path')
    return path


def parse_ratio(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "%r not a floating-point literal" % (x,))
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % (x,))
    return x


def diff(content1: str, content2: str):
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


def sanitize(pad_input: PyPDF2.PdfFileReader, pdf_output: PyPDF2.PdfFileWriter, title_ratio: float, content_ratio: float):
    prev_page = pad_input.getPage(0)
    nb_pages = pad_input.getNumPages()
    for i in range(1, nb_pages):
        progress_with_message('Sanitizing pdf ...', i / nb_pages)
        current_page = pad_input.getPage(i)
        current_content = current_page.extractText()
        prev_content = prev_page.extractText()

        diff_title = diff(get_title(prev_content), get_title(current_content))
        diff_content = diff(get_content(prev_content),
                            get_content(current_content))
        title_has_changed = diff_title.ratio() < title_ratio
        content_has_changed = (diff_content.ratio() < content_ratio
                               and (has_deleted_item(diff_content) or len(prev_content) > len(current_content)))

        if has_content(prev_content) and (title_has_changed or content_has_changed):
            pdf_output.addPage(prev_page)

        prev_page = current_page
    pdf_output.addPage(prev_page)


parser = argparse.ArgumentParser(
    description="Quickly remove useless page from a huge pdf to get a readable pdf")
parser.add_argument('input_file', type=parse_file,
                    help='pdf file to be sanitized')
parser.add_argument('output_file', type=str,
                    help='output sanitized pdf file name')
parser.add_argument('--title-ratio', type=parse_ratio,
                    help='float between [0, 1] which is responsible of detecting similar pages from title. The higher the ratio, the more sensitive the sanitizer will be to any changes. (default: 0.5)', default=.5, dest='title_ratio')
parser.add_argument('--content-ratio', type=parse_ratio,
                    help='float between [0, 1] which is responsible of detecting similar pages from content. The higher the ratio, the more sensitive the sanitizer will be to any changes. (default: 0.8)',
                    default=.8, dest='content_ratio')


def main():
    args = parser.parse_args()
    pdf_input = PyPDF2.PdfFileReader(args.input_file)
    pdf_output = PyPDF2.PdfFileWriter()
    sanitize(pdf_input, pdf_output, args.title_ratio, args.content_ratio)
    with open(args.output_file, 'wb') as f:
        pdf_output.write(f)
    success_with_message(f'Your file has been sanitized at {args.output_file}')


if __name__ == '__main__':
    main()
