import os
from settings import *

MALLET = "mallet-2.0.6/bin/mallet "

def import_dir():
    cmd = MALLET + "import-dir "
    cmd += "--input %s " % (DATA_DIR)
    cmd += "--output %s " % (MALLET_INPUT_FILE)
    cmd += "--keep-sequence --remove-stopwords "
    cmd += "--token-regex [A-Za-z0-9]+"
    os.system(cmd)

def train_topics():
    cmd = MALLET + "train-topics "
    cmd += "--input %s " % (MALLET_INPUT_FILE)
    cmd += "--inferencer-filename %s " % (INFERENCER_FILE)
    cmd += "--num-topics %d " % (NUM_TOPICS)
    cmd += "--output-state %s " % (OUTPUT_STATE)
    cmd += "--optimize-interval %d " % (OPTIMIZE_INTERVAL)
    cmd += "--output-topic-keys %s " % (TOPIC_KEYS_FILE)
    cmd += "--num-top-words %d " % (NUM_TOP_WORDS)

    os.system(cmd)

def infer_topics():
    cmd = MALLET + "infer-topics "
    cmd += "--input %s " % (MALLET_INPUT_FILE)
    cmd += "--inferencer %s " % (INFERENCER_FILE)
    cmd += "--output-doc-topics %s" % (INFERRED_FILE)
    os.system(cmd)


import_dir()
train_topics()
infer_topics()
