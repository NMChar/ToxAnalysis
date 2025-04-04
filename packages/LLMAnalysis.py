from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "microsoft/BioGPT-Large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def key_finding(abstract):
    prompt = (
        "Abstract:  \n"
    )

    prompt += f"{abstract}\n\n"

    prompt += "Summarize the key finding: \n"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=250,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary.split("Summarize the key finding:")[1].strip().split("< / FREETEXT > < / ABSTRACT >")[0].strip()