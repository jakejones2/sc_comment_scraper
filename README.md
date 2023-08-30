## Emergency To do

- the 'tracks' parent url crashes, but playlist works fine
- check progress bar when retrieving from parent
- make app replayable, currently crashes on second press of start
- didn't strip whitespace from urls in manual merge, also crashed
- add 'files created here' label to finished scroll bar
- check file browsing button
- check from artist/playlist functions
- rename app?
- scroll bar was weird with beyonce tracks, 4 urls, 60 per url, no filters and unhide chrome browser

## Setup

1. Install and set up **virtualenvwrapper**: https://virtualenvwrapper.readthedocs.io/en/latest/
2. Set up and `workon` a virtual env and install all project dependencies from `requirements.txt`
3. Navigate to `sc_comment_scraper/src`
4. Run the command `add2virtualenv .` (this adds the module to PYTHONPATH)
5. Change dir into `sc_comment_scraper/src/app`
6. Run `py main.py`

## Example

1. Run all the steps in the Setup section above - the GUI should pop up
2. Select _manual_ in _URL Input Method_
3. Enter `https.//soundcloud.com/bonobo/bonobo-and-jacques-greene-fold` in the _URL Entry_ box (or another track URL that you know has comments)
4. Check _Merge csv files as_ in _Scraping Settings_, and enter a filename (e.g. 'example')
5. Check _None_ in _Filters_
6. Press _Start_
7. Once completed, check the `src/csv_exports` directory and look for your CSV files

## Help

This is an old project - my first one! There are plenty of bugs and badly-written bits of code... If you are not getting the results you think you should be, try close the app (ctrl C in the terminal) and start over. Also try searching for the `csv_exports` folder in case this has been created somewhere other than the package root. Otherwise, try adjusting the settings and filters, or choose a new url!

If the writing to CSV fails, the data may still be available via a backup UI in the terminal.
