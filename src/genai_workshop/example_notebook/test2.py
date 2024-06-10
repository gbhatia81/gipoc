

# from huggingface_hub import notebook_login
# notebook_login()

# import torch
from datasets import load_dataset, Dataset
from peft import LoraConfig, AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer
import os
from datasets import Dataset, load_from_disk

model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
output_model="tinyllama-colorist-v10"

def formatted_train(input,response)->str:
    return f"<|im_start|>user\n{input}<|im_end|>\n<|im_start|>assistant\n{response}<|im_end|>\n"

from datasets import Dataset 
import pandas as pd 

#Load the training and test datasets from disk
train_ds = load_from_disk(f"{output_model}/train_dataset")
test_ds = load_from_disk(f"{output_model}/test_dataset")
# train_ds = False

if not train_ds:
    print ("Generating Training Data")
    df = pd.read_csv("jql.csv")
    df["text"] = df[["Question", "JQL"]].apply(lambda x: formatted_train(x["Question"],x["JQL"]), axis=1)
    data = Dataset.from_pandas(df)

    print(data)
    # data[0]
    ds_split_train_test = data.train_test_split(test_size=0.15/0.85)
    train_ds, test_ds = ds_split_train_test["train"], ds_split_train_test["test"]

    # Save the training and test datasets to disk
    train_ds.save_to_disk(f"{output_model}/train_dataset")
    test_ds.save_to_disk(f"{output_model}/test_dataset")



# print("Is CUDA available:", torch.cuda.is_available())
# print("Number of GPUs:", torch.cuda.device_count())
# if torch.cuda.is_available():
#     print("GPU Name:", torch.cuda.get_device_name(0))


def get_model_and_tokenizer(mode_id):
    tokenizer = AutoTokenizer.from_pretrained(mode_id)    
    tokenizer.pad_token = tokenizer.eos_token
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype="float16", bnb_4bit_use_double_quant=True
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        mode_id, 
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    model.config.use_cache=False
    # model.config.pretraining_tp=1 # 1 is default value
    return model, tokenizer

model, tokenizer = get_model_and_tokenizer(model_id)

print(model)

from transformers import GenerationConfig
from time import perf_counter

def formatted_prompt(question)-> str:
    return f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant:"

def generate_response(user_input, model):  
    prompt = formatted_prompt(user_input)
    
   
    generation_config = GenerationConfig(penalty_alpha=0.6,do_sample = True,
      top_k=5,temperature=0.5,repetition_penalty=1.2,
      max_new_tokens=1000,pad_token_id=tokenizer.eos_token_id
    )
    
    start_time = perf_counter()
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda')
    
    outputs = model.generate(**inputs, penalty_alpha=0.6,do_sample = True,
      top_k=5,temperature=0.5,repetition_penalty=1.2,
      max_new_tokens=1000)
  
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    output_time = perf_counter() - start_time
    print(f"Time taken for inference: {round(output_time,2)} seconds")

# query = 'Select all issues reported by Varun with "Completed" status in project XYZ in JQL'

# generate_response(user_input=query, model=model)

# Define the function to get the latest checkpoint
def get_latest_checkpoint(output_dir):
    checkpoint_dirs = [d for d in os.listdir(output_dir) if d.startswith("checkpoint-")]
    if not checkpoint_dirs:
        return None
    latest_checkpoint = max(checkpoint_dirs, key=lambda d: int(d.split('-')[-1]))
    return os.path.join(output_dir, latest_checkpoint)

latest_checkpoint = get_latest_checkpoint(output_model)

if latest_checkpoint:
    print(f"Resuming from checkpoint: {latest_checkpoint}")
else:
    print("No checkpoint found. Starting from scratch.")
    


peft_config = LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
    )
training_arguments = TrainingArguments(
        output_dir=output_model,
        per_device_train_batch_size=16,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        save_strategy="epoch",
        logging_steps=10,
        num_train_epochs=10,
        max_steps=250,
        fp16=True,
        evaluation_strategy="steps",
        eval_steps=0.2,
        
    )
trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        peft_config=peft_config,
        dataset_text_field="text",
        args=training_arguments,
        tokenizer=tokenizer,
        packing=False,
        max_seq_length=1024
    )
trainer.train(resume_from_checkpoint=latest_checkpoint)

from peft import AutoPeftModelForCausalLM, PeftModel
from transformers import AutoModelForCausalLM
import torch
import os

new_model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, load_in_8bit=False,
                                             device_map="auto",
                                             trust_remote_code=True)
model_path = f"{output_model}/checkpoint-250/"
# model_path = "tinyllama-colorist-v10/checkpoint-250/"
peft_model = PeftModel.from_pretrained(new_model, model_path, from_transformers=True, device_map="auto")
updated_model = peft_model.merge_and_unload()
generate_response(user_input='Select all issues reported by Varun with "Completed" status in project XYZ in JQL', model=updated_model)