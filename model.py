import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from nltk.translate.bleu_score import sentence_bleu
import pandas as pd
import random
import time

from config import get_config

class ConversationalChatbot(object):
    def __init__(self, config=get_config()):
        super(ConversationalChatbot, self).__init__()

        assert config.mode in ['rule-based', 'ai'], print("ConversationalChatbot's mode must be 'rule-based' or 'ai'")
        self.mode = config.mode
        self.bot_history = ''   
        # current implemetation only record the latest bot response 
        # to generate the next response with users' input

        self.chatbot = {}
        self.chatbot['ai'] = ChatbotAI(config)
        self.chatbot['rule-based'] = ChatbotRuleBased(config)

    def change_mode(self, mode):
        assert mode in ['rule-based', 'ai'], print("ConversationalChatbot's mode must be 'rule-based' or 'ai'")
        self.mode = mode

    def generate_answer(self, inp):
        t = time.time()
        self.bot_history = self.chatbot[self.mode].generate_answer(inp, self.bot_history)
        print('reply after {:.4f} second'.format(time.time()-t))
        return self.bot_history


class ChatbotAI(object):
    def __init__(self, config):
        super(ChatbotAI, self).__init__()

        ptm = config.ptm
        self.ptm = ptm
        self.tokenizer = AutoTokenizer.from_pretrained(ptm)
        self.model = AutoModelForCausalLM.from_pretrained(ptm)

    def generate_answer(self, inp, bot_history):
        eos = self.tokenizer.eos_token
        input_str = inp + eos + bot_history + eos
        bot_input_ids = self.tokenizer.encode(input_str, return_tensors='pt')

        bot_output_ids = self.model.generate(bot_input_ids, max_length=100, pad_token_id=self.tokenizer.eos_token_id)
        output = self.tokenizer.decode(bot_output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return output


class ChatbotRuleBased(object):
    def __init__(self, config):
        super(ChatbotRuleBased, self).__init__()

        self.data = pd.read_csv(config.data_dir)
        self.data['bleu'] = 0
        self.top_k = config.top_k
        self.bleu_weights = config.bleu_weights
        
        # for fast response, query on a part of the dataset
        self.partial_query = config.partial_query
        self.num_of_samples = config.num_of_samples

    def generate_answer(self, inp, bot_history):
        data = self.data.sample(n=self.num_of_samples) if \
            self.partial_query else self.data

        # calculate BLEU score ~ similarity bw user input and template input, with bot_history added
        # this function would yield x as 'topic-complement' of bot_history w.r.t inp, as natural way to develop the conversation
        # may change to 2-gram to reduce query time
        data['bleu'] = data['inp'].apply(lambda x: sentence_bleu(
            [bot_history.lower(), x], inp.lower(), weights=self.bleu_weights))
        
        # select output from top 5 templates with highest bleu
        data.sort_values(by='bleu', ascending=False, inplace=True)
        print(data.head(self.top_k))
        candidates = data['rep'][0:self.top_k].to_list()
        output = random.choice(candidates)

        # may sample a number of template answer from self.data to reduve the computing time -> comparison of output ai/rule-based/rb-reduce, trade off

        return output