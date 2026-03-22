import os
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_feedback(feedback):

    prompt = f"""
    Analyze this customer feedback.

    Return in this format:

    Sentiment: Positive / Neutral / Negative
    Summary: short explanation
    Improvement: suggestion

    Feedback:
    {feedback}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


def extract_sentiment(text):

    text = text.lower()

    if "positive" in text:
        return "Positive"
    elif "negative" in text:
        return "Negative"
    else:
        return "Neutral"


def generate_overall_report(all_feedback):

    combined = "\n".join(all_feedback)

    prompt = f"""
    Analyze the following customer feedback and generate a business report.

    Include:
    - Overall sentiment
    - Top 3 complaints
    - Top 3 positive aspects
    - Business improvement suggestions

    Feedback:
    {combined}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


df = pd.read_csv("feedback.csv")

results = []
sentiments = []

print("Analyzing feedback...\n")

for feedback in df["feedback"]:

    analysis = analyze_feedback(feedback)

    sentiment = extract_sentiment(analysis)

    sentiments.append(sentiment)

    results.append({
        "feedback": feedback,
        "analysis": analysis,
        "sentiment": sentiment
    })


result_df = pd.DataFrame(results)

result_df.to_csv("analysis_results.csv", index=False)

print("Saved individual analysis to analysis_results.csv")

print("\nGenerating overall report...")

overall_report = generate_overall_report(df["feedback"].tolist())

with open("overall_report.txt","w") as f:
    f.write(overall_report)

print("Saved overall report to overall_report.txt")


print("\nGenerating sentiment chart...")

sentiment_counts = result_df["sentiment"].value_counts()

plt.figure(figsize=(6,4))
sentiment_counts.plot(kind="bar")

plt.title("Customer Feedback Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig("sentiment_distribution.png")

print("Sentiment chart saved to sentiment_distribution.png")