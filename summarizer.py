from transformers import pipeline

try:
    summarizer = pipeline("text-classification", model="facebook/bart-large-mnli")
except:
    summarizer = None

def summarize_text(text: str) -> str:
    if not text:
        return ""
    if summarizer and len(text.split()) > 10:
        result = summarizer(text, truncation=True, max_length=130, min_length=30)
        return result[0]['summary_text']
    else:
        return '. '.join(text.split('.')[:2]).strip()
