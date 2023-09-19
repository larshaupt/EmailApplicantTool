# Email Applicant Processing Tool

This Python script is designed to automate the process of filtering and managing contact requests received via email. It connects to an IMAP email account, retrieves emails that match specific criteria, extracts relevant information, and performs actions like saving emails to a local folder and moving emails to designated folders within the email account. This README provides an overview of the script's functionality and usage.

## Prerequisites

Before using this script, ensure you have the following dependencies installed:

- [imap_tools](https://github.com/ikvk/imap_tools): A Python library for working with IMAP email accounts.
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): A library for web scraping HTML and XML documents.
- [pandas](https://pandas.pydata.org/): A data manipulation library.
- [matplotlib](https://matplotlib.org/): A library for creating static, animated, and interactive visualizations in Python.

You can install these dependencies using `pip`:

```bash
pip install imap-tools beautifulsoup4 pandas matplotlib
```
## Configuration

1. **Account Credentials**: You will be prompted to enter your email username and password when you run the script. These credentials are used to log in to your IMAP email account.

2. **IMAP Server and Port**: The script is set up to work with the Bluewin.ch IMAP server on port 993. You can change these settings by modifying the `imap_server` and `imap_port` variables in the script.

## Functionality

The script performs the following tasks:

1. **Fetching Emails**: It connects to the specified IMAP server, logs in with your credentials, and fetches emails.

2. **Filtering Emails**: It filters emails received after a specified date (in this case, August 24, 2023) and with the subject "Contact request."

3. **Extracting Information**: The script extracts relevant information from the emails, including the sender's name, email address, message text, and other features.

4. **Classifying Occupations**: It classifies the occupation of the sender based on the message content. Currently, it recognizes "student," "phd," and "intern" as potential occupations.

5. **Selecting Candidates**: Based on predefined criteria (e.g., message length, occupation), the script selects candidates who meet certain requirements. You can adjust these criteria as needed.

6. **Saving Emails**: It saves the selected candidates' emails into separate text files within a specified folder (in this case, the "round_1" folder).

7. **Moving Emails**: It moves the selected candidates' emails to a designated folder within your email account (in this case, the "Second_chance" folder).

8. **Cleaning Up**: It deletes all emails from the "Round_1" folder to maintain a clean inbox.

## Usage

1. Ensure you have configured the script with your email credentials, IMAP server settings, and other preferences.

2. Run the script. It will prompt you to enter your email username and password.

3. The script will perform the tasks outlined above and display relevant information as it runs.

4. Review the selected candidates' emails in the "round_1" folder on your local system and in the "Second_chance" folder within your email account.

5. Customize the selection criteria and other parameters in the script to meet your specific needs.

Please exercise caution when using this script, especially with email accounts containing important messages. It's recommended to test the script with a secondary or dedicated email account before using it with your primary account.