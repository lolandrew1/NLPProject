import encoder
import torch
from transformers import DistilBertForQuestionAnswering
from transformers import DistilBertTokenizerFast
from torch.utils.data import DataLoader
from transformers import AdamW
from tqdm import tqdm

# Based on the huggingface transformer documentation 
class SquadDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

def tune():
    train_encodings, answers = encoder.tokenize()
    encoder.add_positions(train_encodings, answers)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    train_dataset = SquadDataset(train_encodings)

    model = DistilBertForQuestionAnswering.from_pretrained("distilbert-base-uncased")

    if torch.cuda.is_available():
        device = torch.device('cuda') 
    else:
        device = torch.device('cpu')

    model.to(device)
    model.train()
    
    # initialize adam optimizer with weight decay (reduces chance of overfitting)
    optim = AdamW(model.parameters(), lr = 5e-5)

    train_loader = DataLoader(train_dataset, batch_size = 16, shuffle = True)

    for epoch in range(3):
        model.train()
        
        loop = tqdm(train_loader, leave=True)
        for batch in loop:
            
            optim.zero_grad()
            
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            start_positions = batch['start_positions'].to(device)
            end_positions = batch['end_positions'].to(device)
            
            outputs = model(input_ids, 
                            attention_mask = attention_mask,
                            start_positions = start_positions,
                            end_positions = end_positions)
            
            loss = outputs[0]
            loss.backward()
            optim.step()
            
            loop.set_description(f'Epoch {epoch}')
            loop.set_postfix(loss=loss.item())

    model_path = 'models/distilbert-custom'
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    model.eval()
    return model





