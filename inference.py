import os
from openai import OpenAI
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

BASE_URL = os.getenv("BASE_URL", "http://localhost:7860")

print("[START]")

state = requests.post(f"{BASE_URL}/reset").json()["state"]

done = False
step_count = 0

while not done and step_count < 5:
    ticket = state["ticket"]

    prompt = f"Respond professionally: {ticket}"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        action = response.choices[0].message.content
    except:
        if "order" in ticket.lower():
            action = "Sorry, track your order using tracking link."
        elif "refund" in ticket.lower():
            action = "We apologize, refund will be processed."
        else:
            action = "We sincerely apologize and will resolve this quickly."

    res = requests.post(f"{BASE_URL}/step", json={"action": action}).json()

    print(f"[STEP] step={step_count} reward={res['reward']}")

    state = res["state"]
    done = res["done"]
    step_count += 1

print("[END]")