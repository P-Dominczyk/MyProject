import glob
import pickle
import sys
from os.path import exists as file_exists

import click

# python MyProject\Project.py check "This was an awesome movie! 10/10"
# python MyProject\Project.py train
# python MyProject\Project.py add
# python MyProject\Project.py raport

NEGATIV_PATH = r'C:/Users/pedom/OneDrive/Praktyczny_Python_materialy/M03/data/aclImdb/train/neg/*.txt'
POSITIVE_PATH = r'C:/Users/pedom/OneDrive/Praktyczny_Python_materialy/M03/data/aclImdb/train/pos/*.txt'
PUNCTUATIONS = '!@#$%^&*():_+?.,><\'\"-'
DATABASE = 'Revievs DataBase.db'


def remove_punctuations(content) -> str:
    '''Replace punctuations with spaces in text'''
    for punc in PUNCTUATIONS:
        content = content.replace(punc, ' ')
    return content


def load_revievs(path) -> list[dict, int]:
    ''' Load and parse reviews and return a dictionary of words and it occurs '''
    words = {}
    comment_counter = 0
    filenames = glob.glob(path)
    for filename in filenames:
        comment_counter += 1
        with open(filename, 'r') as stream:
            content = stream.read()
            content = content.replace('<br />', ' ')
            comment = remove_punctuations(content)
            comment = content.lower().split()
            for word in set(comment):
                words[word] = words.get(word, 0) + 1
    return words, comment_counter


def comment_to_check(comment: str) -> set:
    '''Create a set of words from input text'''
    comment = remove_punctuations(comment)
    comment = comment.lower().split()
    words_in_comment = set(comment)
    return (words_in_comment)


def compute_sentiment(input_words: set, pos_words: dict, neg_words: dict) -> float:
    overall_sentiment = 0
    print('Sentiment:| Word:')
    print('----------|------------')

    for word in input_words:
        if word in (pos_words or neg_words):
            all_ = pos_words[word] + neg_words[word]
            sent = (pos_words[word] - neg_words[word])/all_
        else:
            sent = 0
        overall_sentiment += sent

        print(f'{sent:^10.6f}|{word}')
        print('----------|------------')
    return (overall_sentiment)


def sentiment_raport(input_words, overall_sentiment) -> None:
    '''Print sentiment raport'''
    overall_rating = overall_sentiment/len(input_words)
    if overall_rating > 0:
        label = 'positive'
    elif overall_rating < 0:
        label = 'negative'
    else:
        label = 'neutral'
    print(f'This sentence is {label}.\nSentiment = {overall_rating}')


def open_database() -> None:
    try:
        with open(DATABASE, 'rb') as stream:
            revievs = pickle.load(stream)
    except FileNotFoundError:
        print('Database not found. Use "train" option to create it.')
        sys.exit(1)
    return revievs


def save_database(revievs: list) -> None:
    with open(DATABASE, 'wb') as stream:
        pickle.dump(revievs, stream)


def add_to_database(comment: set) -> list:
    revievs = open_database()
    pos_words = revievs[1]
    neg_words = revievs[0]
    neg_counter = revievs[2]
    pos_counter = revievs[3]
    choice = input(
        'You wanna save it as positive <p> or negative <n> comment?\n If u wanna cancel operation, press anything else.')
    if choice.lower() == 'p':
        pos_counter += 1
        for word in (comment):
            pos_words[word] = pos_words.get(word, 0) + 1

    elif choice.lower() == 'n':
        neg_counter += 1
        for word in (comment):
            neg_words[word] = neg_words.get(word, 0) + 1

    else:
        print('You cancel adding a comment.')
        sys.exit(2)
    revievs = [neg_words, pos_words, neg_counter, pos_counter]
    return revievs


def overwrite_check():
    if file_exists(DATABASE):
        print('Warning! The existing database will be overwritten.')
        answer = input(
            'For overewrie press <y>, press anything else fo cancel.   ')
        if answer.lower() != 'y':
            print('You have cancelled an operation.')
            sys.exit(3)


@click.group()
def cli():
    pass


@cli.command()
def train():
    '''Use to train the programme if it does not have a database.'''
    overwrite_check()
    print('This may take a while...')
    neg_words, neg_counter = load_revievs(NEGATIV_PATH)
    pos_words, pos_counter = load_revievs(POSITIVE_PATH)
    revievs = [neg_words, pos_words, neg_counter, pos_counter]
    save_database(revievs)
    print('Done :)')


@cli.command()
@click.argument('comment', required=False)
def check(comment: str):
    '''Use to check the sentiment of words and sentences.'''
    try:
        len(comment) != 0
    except:
        comment = input('Type your comment to check: ')
    revievs = open_database()
    pos_words = revievs[1]
    neg_words = revievs[0]
    comment = comment_to_check(comment)
    overall_sentiment = compute_sentiment(comment, pos_words, neg_words)
    sentiment_raport(comment, overall_sentiment)


@cli.command()
def raport():
    '''Use to show how many comments the programme has learned.'''
    revievs = open_database()
    neg_counter = revievs[2]
    pos_counter = revievs[3]
    print(f'I have learnd {pos_counter} positives comments and {neg_counter} negative comments\n In total its {neg_counter+pos_counter} comments')
    if neg_counter > pos_counter:
        print('Add some positive comments to keep the test data balanced')
    if neg_counter < pos_counter:
        print('Add some negative comments to keep the test data balanced')


@cli.command()
@click.argument('comment', required=False)
def add(comment: str):
    '''Use to add a comment to the database'''
    try:
        len(comment) != 0
    except:
        comment = input('Enter your comment to add: ')
    comment = comment_to_check(comment)
    revievs = add_to_database(comment)
    save_database(revievs)
    print('Done')


if __name__ == '__main__':
    cli()
