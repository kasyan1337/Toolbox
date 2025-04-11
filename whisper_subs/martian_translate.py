import os
import argparse
import re
import sys

from transformers import MarianMTModel, MarianTokenizer


def translate_text(text, tokenizer, model, model_type, target_language):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    if model_type == "M2M100":
        # For M2M100, use get_lang_id
        forced_bos_token_id = tokenizer.get_lang_id(target_language)
        generated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)
    elif model_type == "NLLB":
        # For NLLB, force target language by converting the token, e.g. "<2en>" for English.
        forced_bos_token = f"<2{target_language}>"
        forced_bos_token_id = tokenizer.convert_tokens_to_ids(forced_bos_token)
        generated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)
    else:  # Default: MarianMT
        generated = model.generate(**inputs)
    return tokenizer.decode(generated[0], skip_special_tokens=True)


def translate_srt(content, tokenizer, model, model_type, target_language):
    blocks = re.split(r'\n\s*\n', content.strip())
    translated_blocks = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3:
            translated_blocks.append(block)
            continue
        index_line = lines[0]
        timestamp_line = lines[1]
        text_lines = lines[2:]
        text_to_translate = " ".join(text_lines)
        translated_text = translate_text(text_to_translate, tokenizer, model, model_type, target_language)
        translated_block = "\n".join([index_line, timestamp_line, translated_text])
        translated_blocks.append(translated_block)
    return "\n\n".join(translated_blocks)


def translate_txt(content, tokenizer, model, model_type, target_language):
    translated_text = translate_text(content, tokenizer, model, model_type, target_language)
    sentences = re.split(r'(?<=[.!?])\s+', translated_text)
    formatted_text = "\n".join(sentence.strip() for sentence in sentences if sentence.strip())
    return formatted_text


def main():
    parser = argparse.ArgumentParser(
        description="Translate existing subtitle files (.srt and .txt) in the 'output' folder from a source language to a target language and save them in 'output_translated' with _{target_language} appended to the filename."
    )
    parser.add_argument("--source_language", type=str, default="en", help="Source language code (e.g., en, sk)")
    parser.add_argument("--target_language", type=str, default="sk", help="Target language code (e.g., sk, en)")
    parser.add_argument("--translation_model", type=str, default="MarianMT",
                        help="Translation model to use. Options: MarianMT, M2M100, NLLB")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "output")
    output_dir = os.path.join(base_dir, "output_translated_martian")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model_type = args.translation_model

    if model_type == "MarianMT":
        model_name = f"Helsinki-NLP/opus-mt-{args.source_language}-{args.target_language}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        translation_model = MarianMTModel.from_pretrained(model_name)
    elif model_type == "M2M100":
        from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
        model_name = "facebook/m2m100_418M"
        tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        translation_model = M2M100ForConditionalGeneration.from_pretrained(model_name)
        tokenizer.src_lang = args.source_language
    elif model_type == "NLLB":
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        translation_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    else:
        print(f"Unknown translation model: {model_type}")
        sys.exit(1)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".srt", ".txt")):
            input_file_path = os.path.join(input_dir, filename)
            with open(input_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if filename.lower().endswith(".srt"):
                translated_content = translate_srt(content, tokenizer, translation_model, model_type,
                                                   args.target_language)
            else:
                translated_content = translate_txt(content, tokenizer, translation_model, model_type,
                                                   args.target_language)
            base_name, ext = os.path.splitext(filename)
            output_filename = f"{base_name}_{args.target_language}{ext}"
            output_file_path = os.path.join(output_dir, output_filename)
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            print(f"Translated '{filename}' to '{output_filename}'.")


if __name__ == "__main__":
    main()