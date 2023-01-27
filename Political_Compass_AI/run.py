# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/run.ipynb.

# %% auto 0
__all__ = ['split_string', 'return_iters', 'collate_batch', 'run']

# %% ../nbs/run.ipynb 0
from fastcore.script import call_parse
def split_string(string):
    # Removing the parentheses and splitting the string by comma
    parts = string[1:-1].split(",")
    # Removing the whitespace and quotes from the parts
    parts = [part.strip().strip("'") for part in parts]
    return parts[0], parts[1]

def return_iters(db:str # Path to db
                 ):
    train_iter = []
    test_iter = []
    file = open(db, 'r', encoding='latin1')
    mapping = {
        "Libertarian Left": 1,
        "Libertarian Right": 2,
        "Authoritarian Left": 3,
        "Authoritarian Right": 4,
        "Centrist": 5,
        "Authoritarian Center": 6,
        "Left": 7,
        "Right": 8,
        "Libertarian Center": 9,
    }
    lines = file.readlines()
    for line in lines:
        opinion,text = split_string(line)
        train_iter+=[(mapping[opinion],text)]
        test_iter+=[(mapping[opinion],text)]
    train_iter = iter(train_iter)
    test_iter = iter(test_iter)
    file.close()
    return train_iter, test_iter

# %% ../nbs/run.ipynb 1
from torchtext.data.utils import get_tokenizer
# from Political_Compass_AI.data_processing import return_iters
# from Political_Compass_AI.data_processing import split_string
from data_processing import yield_tokens
from data_processing import collate_batch
from model import TextClassificationModel
from training import train
from training import evaluate
from torchtext.data.functional import to_map_style_dataset
from torchtext.vocab import build_vocab_from_iterator
from torch.utils.data import DataLoader
from torch.utils.data.dataset import random_split
import time
import torch
import pandas as pd

def collate_batch(
        batch
):
    global text_pipeline
    global db
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    label_pipeline = lambda x: int(x) - 1
    label_list, text_list, offsets = [], [], [0]
    for (_label, _text) in batch:
        label_list.append(label_pipeline(_label))
        processed_text = torch.tensor(text_pipeline(_text), dtype=torch.int64)
        text_list.append(processed_text)
        offsets.append(processed_text.size(0))
    label_list = torch.tensor(label_list, dtype=torch.int64)
    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text_list = torch.cat(text_list)
    return label_list.to(device), text_list.to(device), offsets.to(device)
@call_parse
def run(
    _db:str # dn path to run alignment distribution
    ,emsize = 128
    ,LR = 5
    ,BATCH_SIZE = 32
    ,optimizer = "Adagrad"
    ,EPOCHS = 20


):
    global text_pipeline
    global db
    db=_db
    tokenizer = get_tokenizer('basic_english')
    text_pipeline = lambda x: vocab(tokenizer(x))
    label_pipeline = lambda x: int(x) - 1
    train_iter, test_iter = return_iters(db)
    vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
    vocab.set_default_index(vocab["<unk>"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    train_iter, test_iter = return_iters(db)
    dataloader = DataLoader(train_iter, batch_size=8, shuffle=False, collate_fn=collate_batch)
    train_iter, test_iter = return_iters(db)
    num_class = len(set([label for (label, text) in train_iter]))
    vocab_size = len(vocab)
    model = TextClassificationModel(vocab_size, emsize, num_class).to(device)
    run_ledger = open("Run_Ledger.txt", 'a')
    criterion = torch.nn.CrossEntropyLoss()
    _optimizer=optimizer
    if optimizer=="Adagrad":
        optimizer = torch.optim.Adagrad(model.parameters(), lr=LR)
    elif optimizer=="SGD":
        optimizer = torch.optim.SGD(model.parameters(), lr=LR)
    else:
        print("Choose a different optimizer")
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=0.1)
    total_accu = None
    train_iter, test_iter = return_iters(db)
    train_dataset = to_map_style_dataset(train_iter)
    test_dataset = to_map_style_dataset(test_iter)
    num_train = int(len(train_dataset) * 0.95)
    split_train_, split_valid_ = \
        random_split(train_dataset, [num_train, len(train_dataset) - num_train])

    train_dataloader = DataLoader(split_train_, batch_size=BATCH_SIZE,
                                  shuffle=True, collate_fn=collate_batch)
    valid_dataloader = DataLoader(split_valid_, batch_size=BATCH_SIZE,
                                  shuffle=True, collate_fn=collate_batch)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE,
                                 shuffle=True, collate_fn=collate_batch)
    first_flag = True
    for epoch in range(1, EPOCHS + 1):
        epoch_start_time = time.time()
        train(train_dataloader, model, optimizer, epoch)
        accu_val = evaluate(valid_dataloader, model)
        if total_accu is not None and total_accu > accu_val:
            scheduler.step()
        else:
            total_accu = accu_val

        print('-' * 59)
        print('| end of epoch {:3d} | time: {:5.2f}s | '
              'valid accuracy {:8.3f} '.format(epoch,
                                               time.time() - epoch_start_time,
                                               accu_val))
        print('-' * 59)

    accu_test = evaluate(test_dataloader,model)

    df_Log = {"Database_file":[],"Epochs":[],"LR":[],"Batch_Size":[],
              "Final_accu":[],"Optimzer":[],"accu_test":[]}

    df_Log["Database_file"].append(db)
    df_Log["Epochs"].append(str(EPOCHS))
    df_Log["LR"].append( str(LR))
    df_Log["Batch_Size"].append(str(BATCH_SIZE))
    df_Log["Final_accu"].append(str(accu_val))
    df_Log["Optimzer"].append(_optimizer)
    df_Log["accu_test"].append(accu_test)

    dataframe = pd.DataFrame(df_Log)
    dataframe.to_csv('Run_Ledger.csv',mode='a', index=False,sep="\t")
    print(str(accu_test))
    return model
