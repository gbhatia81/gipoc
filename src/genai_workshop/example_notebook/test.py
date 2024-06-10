import torch
from transformers import pipeline
from transformers import GenerationConfig

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

# We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    
    {"role": "user", "content": "Select all issues reported by Varun with 'Completed' status in project XYZ in JQL"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

generation_config = GenerationConfig(penalty_alpha=0.6,do_sample = True,
      top_k=5,temperature=0.5,repetition_penalty=1.2,
      max_new_tokens=1000
  )


outputs = pipe(prompt, penalty_alpha=0.6,do_sample = True,
      top_k=5,temperature=0.5,repetition_penalty=1.2,
      max_new_tokens=1000)
# outputs = pipe(prompt, generation_config = generation_config)

print(outputs[0]["generated_text"])