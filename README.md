# NIST NSRL RDS Hash
First GitHub Repo and coding project that I felt like sharing. 
I'm working on building a way to easily select files from the RDS downloads and export a sha1 or md5 hash list for importing into forensics tools for known file hash sets. 
AI is helping me along the way.

## NSRL Hash Extractor

This project includes a simple GUI tool to extract MD5 or SHA1 hashes from one
or more NIST NSRL SQLite databases. You can drag and drop the database files
onto the window or browse for them and export a combined text file containing
the hashes.

Because it relies only on the Python standard library (with optional
`tkinterdnd2` for drag and drop), the script is portable across operating
systems where Python is available.

### Requirements

- Python 3.8+
- `tkinterdnd2` package for drag-and-drop support (`pip install tkinterdnd2`)
  (optional; the program falls back to a file browser if unavailable)

### Usage

1. Run `python nsrl_gui.py`.
2. Drag and drop one or more NSRL `.db` files onto the window (or click
   *Browse* to select multiple files).
3. Choose the hash type (MD5 or SHA1).
4. Click **Export Hashes** and choose the output text file location.
5. Import the generated file into your hash set manager.
