import sys, os, argparse

def get_config():
    config = argparse.Namespace()
    
    # ConversationalChatbot
    config.mode = 'rule-based'

    # ChatbotAI
    config.ptm = 'microsoft/DialoGPT-medium'

    # ChatbotRuleBased
    config.data_dir = 'data/inp_rep.csv'
    config.top_k = 5
    config.partial_query = True
    config.num_of_samples = 5000
    config.bleu_weights = [0.34, 0.33, 0.33]

    return config


