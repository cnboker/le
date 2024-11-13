from transformers import pipeline


def test_ssg_close_light():
   # Initialize the paraphrasing pipeline
    paraphrase = pipeline("text2text-generation", model="uer/t5-base-chinese-cluecorpussmall")

    input_text = "开玩extra0"
    # Generate paraphrases with specified parameters
    paraphrases = paraphrase(f"同义词:{input_text}", num_return_sequences=1, max_length=50)

    # Output check
    print("同义句生成结果:", paraphrases)  # Should be a list of dictionaries

    # Extract and print each generated paraphrase
    for paraphrase in paraphrases:
        if 'generated_text' in paraphrase:
            print(paraphrase['generated_text'])
        else:
            print("Error: 'generated_text' key not found in output:", paraphrase)