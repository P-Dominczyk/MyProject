import glob, pickle, sys

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


def load_revievs(path) -> None:
    ''' Load and parse reviews and return a dictionary of words and it occures '''
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


def comment_to_check(comment) -> dict:
    '''Creat a set of words'''
    comment = remove_punctuations(comment)
    comment = comment.lower().split()
    words_in_comment = set(comment)
    return(words_in_comment)


def compute_sentiment(input_words, pos_words, neg_words) -> float:
    ''' Compute sentense sentiment '''
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
    return(overall_sentiment)


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


def open_database(DATABASE: str) -> None:
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
    revievs = open_database(DATABASE)
    pos_words = revievs[1]
    neg_words = revievs[0]
    neg_counter = revievs[2]
    pos_counter = revievs[3]
    choice = input('You wanna save it as positive <p> or negative <n> comment?\n If u wanna cancel operation, press anything else.')
    if choice.lower() == 'p':
        pos_counter += 1
        for word in (comment):
            pos_words[word] = pos_words.get(word, 0) + 1
            
    elif choice.lower() == 'n':
        neg_counter += 1
        for word in (comment):
            neg_words[word] = neg_words.get(word, 0) + 1
            
    else:
         print('You cancel adding comment.')
         sys.exit(2)
    revievs = [neg_words, pos_words, neg_counter, pos_counter]
    return revievs
         



@click.group()
def cli():
    pass

@cli.command()
def train():
    '''Use to train program, if it dont have data base'''
    print('This may take a while...')
    neg_words, neg_counter = load_revievs(NEGATIV_PATH)
    pos_words, pos_counter = load_revievs(POSITIVE_PATH)
    revievs = [neg_words, pos_words, neg_counter, pos_counter]
    save_database(revievs)
    print('Done :)')

@cli.command()
@click.argument('comment', required=False)
def check(comment: str):
    '''Use to chcek sentiment of words and sentence'''
    try:
        len(comment) !=0
    except:
         comment = input('Type your comment to chek: ')
    revievs = open_database(DATABASE)
    pos_words = revievs[1]
    neg_words = revievs[0]
    comment = comment_to_check(comment)
    overall_sentiment = compute_sentiment(comment, pos_words, neg_words)
    sentiment_raport(comment, overall_sentiment)


@cli.command()
def raport():
     '''Use to show how many comments program learnd'''
     revievs = open_database(DATABASE)
     neg_counter = revievs[2]
     pos_counter = revievs[3]
     print(f'I have learnd {pos_counter} positives comments and {neg_counter} negative comments\n In total its {neg_counter+pos_counter} comments')
     if neg_counter>pos_counter:
          print('Add some positive comments to keep balanced in test data')
     if neg_counter<pos_counter:
          print('Add some negative comments to keep balanced in test data')


@cli.command()
@click.argument('comment', required=False)
def add(comment: str):
    '''Use to add comment to database'''
    try:
        len(comment) !=0
    except:
         comment = input('Type your comment to add: ')
    comment = comment_to_check(comment)
    revievs = add_to_database(comment)
    save_database(revievs)
    print('Done')
     

if __name__ == '__main__':
    cli()

    #przerobic add
    #dodac potwierdzenie w train

#potwierdzenie