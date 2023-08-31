# SoundCloud Comment Scraper

First ever coding project - a GUI for scraping and filtering SoundCloud comments. Needs a bit of work but does the job!

Built with Python, Selenium and Tkinter. Has an array of built-in and custom filters which can be stacked. Originally intended for music research, hence the GUI. Would have been more effective as a web app but I learnt a lot about Tkinter in the process...

## Setup

1. Install and set up **virtualenvwrapper**: https://virtualenvwrapper.readthedocs.io/en/latest/
2. Set up and `workon` a virtual env and install all project dependencies from `requirements.txt`
3. Navigate to `sc_comment_scraper/src`
4. Run the command `add2virtualenv .` (this adds the module to PYTHONPATH): https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html#add2virtualenv
5. Change dir into `sc_comment_scraper/src/app`
6. Run `py main.py`

## Example

1. Run all the steps in the **Setup** section above - the GUI should pop up
2. Select _manual_ in _URL Input Method_
3. Enter `https.//soundcloud.com/bonobo/bonobo-and-jacques-greene-fold` in the _URL Entry_ box (or another track URL that you know has comments)
4. Check _Merge csv files as_ in _Scraping Settings_, and enter a filename (e.g. 'example')
5. Check _None_ in _Filters_
6. Press _Start_
7. Once completed, check the `src/csv_exports` directory and look for your CSV files

## Help

This is an old project - my first one! There are plenty of bugs and badly-written bits of code so apologies if things don't always run smoothly...

If you get errors, the first thing to check are the **advanced scraping settings**. Try increase the `wait time` to account for a slower network.

If you are still not getting the results you think you should be, try close the app (ctrl C in the terminal) and start over. Also try searching for the `csv_exports` folder in case this has been created somewhere other than the package root. Otherwise, try adjusting the other settings and filters, or choose a new url!

If the writing to CSV fails, the data may still be available via a backup UI in the terminal.

On macOS at least, screenshots will crash the app...

## To Do

### Refactoring

- Replace error handling with robust testing/type checking and only targeted try/except blocks (no catch-alls)
- Review OOP structure throughout: currently lots of large, tightly-coupled classes and functions with poor cohesion.
- Fix selenium waiting - time.sleep() is not the best way to go about this! Need to use implicit waits etc.
- Rewrite scraping code to select timestamp, datetime and comment body all at the same time and bind this data in an object. Would prevent errors if DOM data incomplete.
- Filter system's use of eval() is insecure. Could move this code into a method in the Filter class.

### Extensions

- Complete the data analysis frame, analyse themes, spam etc.
- add 'files created here' label to finished scroll bar
- validate GUI interface more - highlight empty inputs, add placeholders etc. Maybe a help button explaining a few things.
- UHD mode only works on Windows
- MacOS doesn't seem to automatically find txt files in some cases?
- Make into a web app?
