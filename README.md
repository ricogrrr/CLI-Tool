# File Organizer CLI Tool

A powerful command-line utility that automatically organizes files in a directory by categorizing them based on their file extensions.

## Features

- **Automatic Categorization**: Sorts files into folders based on their type (images, documents, audio, video, etc.)
- **Dry Run Mode**: Preview changes before actually moving files
- **Recursive Organization**: Option to organize files in subdirectories
- **Conflict Handling**: Automatically handles filename conflicts
- **Detailed Logging**: Keeps track of all operations with timestamped logs
- **Statistics**: View storage usage by category

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone this repository or download the source code:
```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x file_organizer.py
```

## Usage

### Basic Usage
Organize files in the current directory:
```bash
python file_organizer.py
```

### Additional Options
Organize a specific directory:
```bash
python file_organizer.py /path/to/directory
```

Preview changes without moving files (dry run):
```bash
python file_organizer.py -n
```

Recursively organize files in subdirectories:
```bash
python file_organizer.py -r
```

Show statistics after organizing:
```bash
python file_organizer.py -s
```

Display help message:
```bash
python file_organizer.py -h
```

## File Categories

Files are organized into the following categories based on their extensions:

| Category | File Extensions |
|----------|----------------|
| images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .tiff, .webp |
| documents | .pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx |
| audio | .mp3, .wav, .flac, .aac, .ogg, .wma |
| video | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm |
| archives | .zip, .rar, .7z, .tar, .gz, .bz2 |
| code | .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go, .ts, .jsx, .json |
| others | All other file extensions |

## Example

Before:
```
Downloads/
├── report.pdf
├── vacation.jpg
├── presentation.pptx
├── music.mp3
├── archive.zip
└── script.py
```

After running `python file_organizer.py Downloads/`:
```
Downloads/
├── documents/
│   ├── report.pdf
│   └── presentation.pptx
├── images/
│   └── vacation.jpg
├── audio/
│   └── music.mp3
├── archives/
│   └── archive.zip
├── code/
│   └── script.py
└── logs/
    └── file_organizer_20250228_120000.log
```

## Logging

Logs are stored in the `logs` directory with timestamps. Each log file contains details of file operations, including:
- Files moved
- Directories created
- Errors encountered
- Statistics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- GUI interface
- Custom categorization rules
- File type detection based on content
- Scheduled organization
- Undo functionality