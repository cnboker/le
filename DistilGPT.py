from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 加载模型和分词器
#　model_name = "distilgpt2"
model_name = "uer/gpt2-chinese-cluecorpussmall"  # 或 "thu-coai/CDial-GPT2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 设置 `pad_token_id` 为 `eos_token_id` 以避免警告
if model.config.pad_token_id is None:
    model.config.pad_token_id = model.config.eos_token_id

def generate_text(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # 如果需要，可以传递 `attention_mask` 参数
    attention_mask = inputs["attention_mask"]

    # 生成响应
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=attention_mask,
        max_length=max_length,
        do_sample=True,
        temperature=0.7,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# 测试生成
print(generate_text("中国有多少人."))