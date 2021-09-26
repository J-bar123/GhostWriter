# The project is based on Tensorflow's Text Generation with RNN tutorial
# Copyright Petros Demetrakopoulos 2020
import tensorflow as tf
import numpy as np
import os
import time
# The project is based on Tensorflow's Text Generation with RNN tutorial
# Copyright Petros Demetrakopoulos 2020
import tensorflow as tf
import numpy as np
import os
import time
from random import seed
from random import randint
import sys
import urllib.request

stopChars = [',', '(', ')', '.', '-', '[', ']', '"']


corpus_path = "/tmp/data.txt"
text = open(corpus_path, 'rb').read().decode(encoding='utf-8')
text = preprocessText(text)
corpus_words = corpusToList(text)
map(str.strip, corpus_words)  # trim words

vocab = sorted(set(corpus_words))
print('Corpus length (in words):', len(corpus_words))
print('Unique words in corpus: {}'.format(len(vocab)))


word2idx = {u: i for i, u in enumerate(vocab)}
idx2words = np.array(vocab)
word_as_int = np.array([word2idx[c] for c in corpus_words])
# The maximum length sentence we want for a single input in words
seqLength = 10
examples_per_epoch = len(corpus_words)//(seqLength + 1)

# Create training examples / targets
wordDataset = tf.data.Dataset.from_tensor_slices(word_as_int)

# generating batches of 10 words each
sequencesOfWords = wordDataset.batch(seqLength + 1, drop_remainder=True)

def yuh(): 
    corpus_path = "/tmp/data.txt"
    text = open(corpus_path, 'rb').read().decode(encoding='utf-8')
    text = preprocessText(text)
    corpus_words = corpusToList(text)
    map(str.strip, corpus_words)  # trim words

    vocab = sorted(set(corpus_words))
    print('Corpus length (in words):', len(corpus_words))
    print('Unique words in corpus: {}'.format(len(vocab)))


    word2idx = {u: i for i, u in enumerate(vocab)}
    idx2words = np.array(vocab)
    word_as_int = np.array([word2idx[c] for c in corpus_words])
    # The maximum length sentence we want for a single input in words
    seqLength = 10
    examples_per_epoch = len(corpus_words)//(seqLength + 1)

# Create training examples / targets
    wordDataset = tf.data.Dataset.from_tensor_slices(word_as_int)

# generating batches of 10 words each
    sequencesOfWords = wordDataset.batch(seqLength + 1, drop_remainder=True)

def preprocessText(text):
    text = text.replace('\n', ' ').replace('\t', '')
    processedText = text.lower()
    for char in stopChars:
        processedText = processedText.replace(char, ' ')
    return processedText


def corpusToList(corpus):
    corpusList = [w for w in corpus.split(' ')]
    # removing empty strings from list
    corpusList = [i for i in corpusList if i]
    return corpusList

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text


def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)


def generateLyrics(model, startString, temp):
    # Number of words to generate
    num_generate = 30

    # Converting our start string to numbers (vectorizing)
    start_string_list = [w for w in startString.split(' ')]
    input_eval = [word2idx[s] for s in start_string_list]
    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = []

    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)

        predictions = predictions / temp
        predicted_id = tf.random.categorical(
            predictions, num_samples=1)[-1, 0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(' ' + idx2words[predicted_id])

    return (startString + ''.join(text_generated))


def doSomeWork(artist):
    url = '''https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fkendrick.txt?alt=media&token=604b7b6c-2ef0-4611-ab6e-a08dd53e99be'''
    urllib.request.urlretrieve(url, '/tmp/data.txt')

    if artist == "kanye": 
        url = '''
        https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fkanye.h5?alt=media&token=a0b94c61-e696-453d-9a16-110af66f6afd'''
    if artist == "nas": 
        url = '''
        https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fnas.h5?alt=media&token=037ef224-be5f-4449-a89c-c1897e164289'''
    if artist == "biggie": 
        url = '''https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fbiggie.h5?alt=media&token=3244a8e2-017c-472f-a66b-7810a198d038'''
    if artist == "jayz": 
        url = '''https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fjayz.h5?alt=media&token=500ff44d-60fe-4774-9c85-5ea6f06da81b'''
    if artist == "ross" or artist == "kendrick" or artist == "50cent": 
        url = '''
        https://firebasestorage.googleapis.com/v0/b/shellhacks-327117.appspot.com/o/models%2Fkendrick.h5?alt=media&token=6ceff75d-5a71-49d4-b927-e727888d872f
        '''
    

    named = "/tmp/" + artist + ".h5"
    if (artist == "biggie") or artist == "50cent":
        named = "/tmp/kendrick" + ".h5"

    urllib.request.urlretrieve(url, named)




    yuh()
    

    model = tf.keras.models.load_model(named)

    seed(1)
    input_str = vocab[randint(0, len(vocab))]
    lyricz = []

    for i in range(10):
        lyrics = generateLyrics(model, startString=input_str, temp=0.6)
        temp = lyrics.replace("nigga", "homie").replace("niggas", "homies").replace("nigger", "homie").replace(
            "niggers", "homies").replace("faggot", "maggot").replace("fag", "mag").replace('\r', '')
        lyricz.append(lyrics.replace("nigga", "homie").replace('\r', ''))
        input_str = temp.split()[-1]

    return jsonify({
        "Success": "It worked",
        "Url": " ".join(lyricz)
    })
