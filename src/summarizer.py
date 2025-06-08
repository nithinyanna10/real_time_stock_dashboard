from transformers import pipeline

# Use BART-Large-CNN for summarization
summarize = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, max_length=130, min_length=30):
    summary = summarize(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
