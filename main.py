from flan_parser import parse_instruction_t5
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if __name__ == "__main__":

    # Base
    tokenizer = AutoTokenizer.from_pretrained("./flan_t5_base")
    model = AutoModelForSeq2SeqLM.from_pretrained("./flan_t5_base")


    while True:
        command = input("\n🗣️  Enter an instruction (or 'q' to quit):\n> ")
        if command.lower() == 'q':
            break

        parsed = parse_instruction_t5(command, tokenizer, model)
        if parsed is None:
            print("\nError parsing the instruction. Please try again.")
        else:
            print("\nParsed output:\n", parsed)
