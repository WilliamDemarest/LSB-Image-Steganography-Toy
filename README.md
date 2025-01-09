# LSB-Image-Steganography-Toy
Functions and script for performing least significant bit steganography with png images.  
  
  
lsb.py -- functions used for performing lsb steganography on a 24png array of the sort created by cv2.imread()
process.py -- functions and script to encode and decode files using lsb steganography. Accepts command line arguments. If any or all necessary arguments are not specified, promts that accept input will be produced. Run with -h or --help for information on argument ussage.  
README.md -- ur lookin at it  


Dependencies:  
process.py uses "opencv-python" and "argparse" libraries.

Notes:  
- There are cases to handle what I expect to be the most common issues, but it's not comprehensive at all. There should still be many ways to break or crash it, some I know of and surely many I do not. Work in progress.  
- This is not a secure way of hiding or sharing information, the content is not encrypted by the script. The first things encoded are the length of the content (plus the length of the name) and the file name.
