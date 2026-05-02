from transformers import pipeline
import os

# Use a small multilingual model (Flan-T5-base supports multiple languages)
model_name = "google/flan-t5-base"
explainer = pipeline("text2text-generation", model=model_name)

def generate_explanation(factors, language="en"):
    if language != "en":
        # For multilingual, we could use a different prompt or model; Flan-T5 handles many languages.
        prompt = f"Explain why dropout risk is high based on these factors: {', '.join(factors)}. Provide explanation in {language}."
    else:
        prompt = f"Explain why dropout risk is high based on these factors: {', '.join(factors)}."
    result = explainer(prompt, max_length=100, do_sample=False)[0]['generated_text']
    return result