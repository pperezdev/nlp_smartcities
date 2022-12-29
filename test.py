from transformers import AutoTokenizer, AutoModelWithLMHead
import torch
import back

result = back.FileManagers().read_document("action_research__wikipedia")
text =result.data

print(text)


tokenizer = AutoTokenizer.from_pretrained("deep-learning-analytics/wikihow-t5-small")
model = AutoModelWithLMHead.from_pretrained("deep-learning-analytics/wikihow-t5-small")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

preprocess_text = text.strip().replace("\n","")
tokenized_text = tokenizer.encode(preprocess_text, return_tensors="pt").to(device)

summary_ids = model.generate(
            tokenized_text,
            max_length=150, 
            num_beams=2,
            repetition_penalty=2.5, 
            length_penalty=1.0, 
            early_stopping=True
        )

output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print ("\n\nSummarized text: \n",output)