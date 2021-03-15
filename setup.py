import nltk

# TODO automate install of other modules
def install_nltk_data():
    print('Installing punkt....')
    nltk.download('punkt')
    print('Install Complete.')


if __name__ == "__main__":
    install_nltk_data()
