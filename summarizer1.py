# transformer_summarizer.py

from typing import List
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class TransformerSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: int = -1):
        self.model_name = model_name
        self.device = device
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self._pipe = pipeline("summarization", model=self._model, tokenizer=self._tokenizer, device=device)

    def _chunk_text(self, text: str, max_tokens: int = 800, overlap: int = 200) -> List[str]:
        tokens = self._tokenizer.encode(text, truncation=False)
        if len(tokens) <= max_tokens:
            return [text]

        chunks = []
        start = 0
        while start < len(tokens):
            end = min(len(tokens), start + max_tokens)
            chunk = tokens[start:end]
            chunk_text = self._tokenizer.decode(chunk, skip_special_tokens=True)
            chunks.append(chunk_text)
            if end == len(tokens):
                break
            start += max_tokens - overlap
        
        return chunks

    def summarize(self, text: str, min_length: int = 30, max_length: int = 120) -> str:
        text = text.strip()
        if not text:
            return ""

        input_tokens = len(self._tokenizer.encode(text))
        
        
        if input_tokens <= 64:
            max_length = 50 

        chunks = self._chunk_text(text)
        summaries = []
        
        for chunk in chunks:
            result = self._pipe(chunk, min_length=min_length, max_length=max_length, truncation=True)
            summaries.append(result[0]["summary_text"].strip())

        if len(summaries) > 1:
            combined_text = " ".join(summaries)
            final_summary = self._pipe(combined_text, min_length=min_length, max_length=max_length, truncation=True)
            return final_summary[0]["summary_text"].strip()

        return summaries[0]

def main():
    summarizer = TransformerSummarizer(model_name="facebook/bart-large-cnn")
    
    print("Please enter the text you want to summarize:")
    notice_text = input()  # Takes input from the user
    
    summary = summarizer.summarize(notice_text)
    
    print("\nGenerated Summary:")
    print(summary)

if __name__ == "__main__":
    main()
