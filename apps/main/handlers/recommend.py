import os
import pickle
import bert

from tensorflow.keras.models import load_model

FullTokenizer = bert.bert_tokenization.FullTokenizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# load tokenizer
vocab_file = os.path.join(BASE_DIR, 'bert/assets/vocab.txt')
do_lower_case = True
tokenizer = FullTokenizer(vocab_file, do_lower_case)

# Load th BERT Model
bert_model = load_model(os.path.join(BASE_DIR, 'bert'))

# Load Embedding Dictionary
with open(os.path.join(BASE_DIR, 'AnimeEmbedd.pb'), 'rb') as f:
    AnimeEmbedd = pickle.load(f)

# Load LSHash table
with open(os.path.join(BASE_DIR, 'AnimeLSH.pb'), 'rb') as f:
    AHash = pickle.load(f)


def prepare_input(anime_synopsis, max_seq_length=512):
    """
    :param anime_synopsis:
    :param max_seq_length:
    :return:
    """

    def get_masks(tokens):
        """
        :param tokens:
        :return:
        """

        if len(tokens) > max_seq_length:
            raise IndexError("Token length more than max seq length!")

        return [1]*len(tokens) + [0] * (max_seq_length - len(tokens))

    def get_segments(tokens):
        """
        :param tokens:
        :return:
        """

        if len(tokens)>max_seq_length:
            raise IndexError("Token length more than max seq length!")
        segments = []
        current_segment_id = 0
        for token in tokens:
            segments.append(current_segment_id)
            if token == "[SEP]":
                current_segment_id = 1
        return segments + [0] * (max_seq_length - len(tokens))

    def get_ids(tokens):
        """
        :param tokens:
        :return:
        """

        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_ids = token_ids + [0] * (max_seq_length-len(token_ids))
        return input_ids

    syn_tokens = tokenizer.tokenize(anime_synopsis)
    syn_tokens = ["[CLS]"] + syn_tokens + ["[SEP]"]

    input_ids = get_ids(syn_tokens)
    input_masks = get_masks(syn_tokens)
    input_segments = get_segments(syn_tokens)

    return [[input_ids], [input_masks], [input_segments]]


def get_similar(anime_id, anime_synopsis):
    """
    :param anime_id:
    :param anime_synopsis:
    :return:
    """

    if anime_id in AnimeEmbedd:
        query_embedd = AnimeEmbedd[anime_id]
    else:
        input_data = prepare_input(anime_synopsis)
        query_embedd, _ = bert_model.predict(input_data)

    response = AHash.query(query_embedd.flatten(), num_results=10, distance_func='hamming')

    similar_animes = []
    for i in range(len(response)):
        similar_animes.append(response[i][0][1])

    return similar_animes
