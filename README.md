# Virtual Assistant

This is my virtual text-based assistant. I made it in order to bypass the need for an interface for many smaller
functions.

## Techniques Used

* Natural Language processing
* LancasterStemmer used to stem words and NLTK stopwords list was used as a base for my custom list
* Multiple APIs for home automation

## TO DO

* Speech Recognition
* Weather info on request
* Open specific folders
* Roku control

## Executable Creation (WIP)

Run this with Pyinstaller within the script directory

```cmd
pyinstaller Main.py --name "Virtual Assistant" --icon icon.ico --distpath EXE --onefile
```

### Icon made by Freepik from flaticon.com
