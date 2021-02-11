# Auto Reserve

Auto Reserve is a script to automate gym reservations at the University of Maryland. This is for educational purposes only.

![Alt text](/screenshot1.png?raw=true "Screenshot1")

# Setup

1. The first time you use the "run()" function in main_exe.py, be sure to provide a seed One Time Use code. These can be found at https://identity.umd.edu/mfaprofile.
2. In otu_gen.py, change the filename variable to point to a CSV that you store your login information in the first (username), second (password), and third (UID) row of column 1.
3. Clear the CSV named "otu_codes"
4. Specify the exact time using the format "10:00 AM" (including the space between the last digit and AM).
5. Copy/paste or type the exact title of the workout you want to select.
