import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analyzer import comment_to_check, load_revievs, open_database, save_database, remove_punctuations


def test_comment_to_check_split():
    comment = 'test sentence'
    got = comment_to_check(comment)
    expected = {'test', 'sentence'}
    assert set(got) == expected


def test_comment_to_check_lower():
    comment = 'TEST'
    got = comment_to_check(comment)
    expected = {'test'}
    assert got == expected


# def test_compute_sentiment():
#     input_words = {'awesome', 'movie', 'awful'}
#     pos_words = {'awesome' : 1, 'movie' : 1, 'awful' : 0}
#     neg_words = {'awful' : 1, 'awesome' : 0, 'movie' : 0}
#     got = compute_sentiment(input_words, pos_words, neg_words)
#     expected = 1
#     assert got == expected


def test_remove_punctuations():
    text = 'Sentence.tested ,punc?'
    got = remove_punctuations(text)
    expected = 'Sentence tested  punc '
    assert got == expected


def test_presistance(tmpdir):
    with tmpdir.as_cwd():
        revievs = ['Testing', 'list']
        save_database(revievs)
        got = open_database()
        assert got == revievs


def test_load_revievs(tmpdir):
    with tmpdir.as_cwd():
        path =r'C:\Users\pedom\OneDrive\Praktyczny_Python_materialy\MyProject\tests\data\1_3.txt'
        got = load_revievs(path)
        expected ={'this': 1, 'is': 1, 'of': 1, "'officer": 1, "gentleman.'": 1, 'imitation': 1, 'pale': 1, 'a': 1, 'and': 1}, 1
        assert got == expected