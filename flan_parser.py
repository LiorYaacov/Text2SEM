from spelling.spell_corrector import spell_correct
from prompts import build_prompt
import json
import re

def clean_instruction(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    text = text.strip()
    # text = spell_correct(text)  # Correct spelling errors
    return text

def parse_instruction_t5(instruction, tokenizer, model):
    instruction = clean_instruction(instruction)
    prompt = build_prompt(instruction)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=128)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)


    ## Generate JSON from output text
    # Try extracting a well-formed JSON block
    match = re.search(r"\{.*?\}", output_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass  # fall through to custom fix

    # Fallback: wrap it into JSON manually
    fallback_text = output_text.strip()

    # Ensure braces are there
    if not fallback_text.startswith("{"):
        fallback_text = "{" + fallback_text
    if not fallback_text.endswith("}"):
        fallback_text = fallback_text + "}"

    # Try removing trailing quote errors
    fallback_text = re.sub(r'"\s*}', '}', fallback_text)  


    try:
        return json.loads(fallback_text)
    except json.JSONDecodeError:
        return {"error": "JSON parsing failed", "raw_output": output_text}


'''
    ### Fallback Parsing Logic ###
    # Attempt to extract key-value pairs from the output text
    # Fallback fix attempt
    fixed_output = output_text.strip()
    if not fixed_output.startswith("{"):
        fixed_output = "{" + fixed_output
    if not fixed_output.endswith("}"):
        fixed_output = fixed_output + "}"

    try:
        parsed = json.loads(fixed_output)
    except json.JSONDecodeError:
        return {"error": "JSON parsing failed", "raw_output": output_text}

    # Final field correction fallback
    if "left" in parsed and "direction" not in parsed:
        parsed["direction"] = "left"
        parsed["distance"] = int(parsed["left"])
        del parsed["left"]
    elif "right" in parsed and "direction" not in parsed:
        parsed["direction"] = "right"
        parsed["distance"] = int(parsed["right"])
        del parsed["right"]
    elif "up" in parsed and "direction" not in parsed:
        parsed["direction"] = "up"
        parsed["distance"] = int(parsed["up"])
        del parsed["up"]
    elif "down" in parsed and "direction" not in parsed:
        parsed["direction"] = "down"
        parsed["distance"] = int(parsed["down"])
        del parsed["down"]

    return parsed



'''