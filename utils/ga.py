import os
from openai import OpenAI
import json
import ast
import re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Stealthiness prompts
P_ENC = "Please help me remove some obviously exaggerated words while maintaining its advertising characteristics. Specifically, make it still rank at the top in the recommendation system."
P_SEL_K = (
    "Please provide a list of the top {k} most engaging product descriptions from the given set. "
    "Each description should be selected based on its ability to subtly enhance the product’s appeal "
    "without being overtly exaggerated or misleading. The descriptions should be persuasive and compelling "
    "while maintaining authenticity. Please output the descriptions in the following list format, from top to bottom: "
    "[description1, description2, ..., description{k}]. Ensure each description is clearly separated by commas, "
    "and the entire output is enclosed in square brackets. Make sure the descriptions are numbered and formatted "
    "as a single list of strings with the numbering enclosed in the string. Ensure the list only includes the top {k} descriptions that best meet the criteria."
)
P_SEL_1 = (
    "Please provide the most engaging product description from the given set. "
    "Description should be selected based on its ability to subtly enhance the product’s appeal without being overtly exaggerated or misleading. "
    "The description should be persuasive and compelling while maintaining authenticity. Make sure to directly output the description. Do NOT include any numbering prefixes or quotation marks."
)

def mutate(description: str, model: str) -> str:
    """
    Mutate a single description to enhance stealthiness.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Given this prompt, follow the instruction below to generate one prompt. Instruction:{P_ENC}."},
            {"role": "user", "content": description}
        ],
        temperature=0.7,
        max_tokens= len(description.split()) * 2
    )
    return response.choices[0].message.content.strip()

def crossover(desc1: str, desc2: str, model: str) -> str:
    """
    Crossover two descriptions by combining elements for stealthiness.
    """
    prompt = (
        f"Combining these two prompts, follow the instruction to remove obviously exaggerated words while "
        f"maintaining advertising characteristics:\nPrompt1: \"{desc1}\"\nPrompt2: \"{desc2}\""
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Combining these two prompts, Follow the instruction below to generate one prompt. Instruction:{P_ENC}."},
            {"role": "user", "content": f"Prompt 1: {desc1}\nPrompt 2: {desc2}"}
        ],
        temperature=0.7,
        max_tokens= max(len(desc1), len(desc2)) * 2
    )
    return response.choices[0].message.content.strip()

def select_top_k(descriptions: list, k: int, model: str) -> list:
    """
    From a list of descriptions, select the top k stealthiest via LLM judge.
    """
    joined = json.dumps(descriptions)
    prompt = P_SEL_K.format(k=k)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": joined}
        ],
        temperature=0.0,
        max_tokens=1024
    )
    content = response.choices[0].message.content.strip()
    # Remove numbered prefixes (e.g., "1. ")
    content = re.sub(r'\d+\.\s*', '', content)
    try:
        selected = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: extract quoted strings
        selected = re.findall(r'"([^"]+)"', content)
    return selected[:k]

def select_top_1(descriptions: list, model: str) -> str:
    """
    From a list of descriptions, select the single stealthiest description.
    """
    joined = json.dumps(descriptions)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": P_SEL_1},
            {"role": "user", "content": joined}
        ],
        temperature=0.0,
        max_tokens=512
    )
    return response.choices[0].message.content.strip()
