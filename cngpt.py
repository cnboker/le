from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 加载中文 GPT-2 模型和分词器
model_name = "uer/gpt2-chinese-cluecorpussmall"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 检查模型配置，设置 pad_token_id 为 eos_token_id，以防止生成警告
if model.config.pad_token_id is None:
    model.config.pad_token_id = model.config.eos_token_id

# 定义要生成的中文文本的开头
prompt = "无聊怎么办"
inputs = tokenizer(prompt, return_tensors="pt")
# 为输入数据创建 attention_mask
attention_mask = inputs["input_ids"] != model.config.pad_token_id
# 生成文本
#with torch.no_grad():
output_ids = model.generate(
    inputs["input_ids"],
    attention_mask=attention_mask,  # 传递 attention_mask
    max_length=200,          # 生成文本的最大长度
    do_sample=True,          # 使用采样生成更自然的文本
    temperature=0.7,         # 控制生成的随机性，较低温度生成更保守的文本
    top_k=50,                # 仅考虑最高概率的前K个词
    top_p=0.9                # Nucleus采样，限制词的累积概率
)

# 解码生成的ID，转换成中文文本
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("生成的文本：", output_text)
