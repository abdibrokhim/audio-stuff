import os.path
import pandas as pd

from transformers import AutoTokenizer, AutoModel
from torch.nn import functional as F

from views.utils import get_name_of_file

tokenizer = AutoTokenizer.from_pretrained('deepset/sentence_bert')
model = AutoModel.from_pretrained('deepset/sentence_bert')


skipped_files = []


def facebook_sentiment_analyse(folder, output_folder, labels):
    if not os.path.exists(folder):
        return "Input folder not found"

    if not os.path.exists(output_folder):
        return "Output folder not found"

    values_list = []
    for file in os.listdir(folder):
        try:
            with open(os.path.join(folder, file), 'r') as f:
                sentence = "".join(f.readlines())

            inputs = tokenizer.batch_encode_plus([sentence] + labels,
                                                 return_tensors='pt',
                                                 pad_to_max_length=True)
            input_ids = inputs['input_ids']
            attention_mask = inputs['attention_mask']
            output = model(input_ids, attention_mask=attention_mask)[0]
            sentence_rep = output[:1].mean(dim=1)
            label_reps = output[1:].mean(dim=1)

            # now find the labels with the highest cosine similarities to
            # the sentence
            similarities = F.cosine_similarity(sentence_rep, label_reps)
            closest = similarities.argsort(descending=True)

            values = [get_name_of_file(file)]
            for index in closest:
                values.append(similarities[index].item())
                print(f'label: {labels[index]} \t similarity: {similarities[index]}')
            values_list.append(values)

        except Exception as ex:
            print(ex)
            skipped_files.append(file)

    df = pd.DataFrame(values_list, columns=["filename"]+labels)
    df.index += 1
    df.to_csv(output_folder + "/" + "facebook_sentiment_analysis.csv")
    print(skipped_files)
    return "Success"

# l = ['business', 'art & culture', 'politics']
# facebook_sentiment_analyse("/home/dilshodbek/dota", "/home/dilshodbek/dota", l)
