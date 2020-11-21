![](./assets/preview.png)

# ![](https://img.shields.io/badge/status-beta-orange) sanitized PDF

> Quickly remove useless page from a huge pdf to get a readable pdf.

![](https://img.shields.io/badge/linux-OK-green) ![](https://img.shields.io/badge/mac-OK-green) ![](https://img.shields.io/badge/windows-not_tested-orange)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

```bash
git clone https://github.com/lucasmrdt/pdf-sanitizer
cd pdf-sanitizer
pip3 install -r requirements.txt --user
```

## Usage

```bash
> ./pdf-sanitizer -h
usage: pdf-sanitizer [-h] [--title-ratio TITLE_RATIO]
                     [--content-ratio CONTENT_RATIO]
                     input_file output_file

Quickly remove useless page from a huge pdf to get a readable pdf

positional arguments:
  input_file            pdf file to be sanitized
  output_file           output sanitized pdf file name

optional arguments:
  -h, --help            show this help message and exit
  --title-ratio TITLE_RATIO
                        float between [0, 1] which is responsible of detecting
                        similar pages from title. The higher the ratio, the
                        more sensitive the sanitizer will be to any changes.
                        (default: 0.5)
  --content-ratio CONTENT_RATIO
                        float between [0, 1] which is responsible of detecting
                        similar pages from content. The higher the ratio, the
                        more sensitive the sanitizer will be to any changes.
                        (default: 0.8)
```

## Example

```bash
> ./pdf-sanitizer my_huge_file.pdf my_readable_file.pdf
✅  Your file has been sanitized at my_readable_file.pdf
```

---

## Contributing

- [ ] Test on windows

Fell free to add more useful features, test it and report issues.

## Support

Reach out to me at one of the following places!

- Website at <a href="https://lucas-marandat.fr" target="_blank">`lucas-marandat.fr`</a>
- LinkedIn at <a href="https://www.linkedin.com/in/lucasmrdt/" target="_blank">`@lucasmrdt`</a>

## License

[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
