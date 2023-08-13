import os
from typing import List
from llama import Llama


os.environ["RANK"] = "0"
os.environ["WORLD_SIZE"] = "1"
os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_PORT"] = "29501"
CHECKPOINT_LOC = "llama_model"
TOKENIZER_LOC = "llama_model/tokenizer.model"
MAX_SEQ_LEN: int = 1000
MAX_BATCH_SIZE: int = 4
generator = Llama.build(
    ckpt_dir=CHECKPOINT_LOC,
    tokenizer_path=TOKENIZER_LOC,
    max_seq_len=MAX_SEQ_LEN,
    max_batch_size=MAX_BATCH_SIZE,
)


def complete_prompt(
    generator,
    prompt: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_gen_len: int = 64,
):
    results = generator.text_completion(
        [prompt],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    assert len(results) == 1

    return results[0]["generation"]


def format_prompt(question: str, game: str, context_info: List[str]):
    prompt = f"""Below are descriptions from the rules of the board game called '{game}':
"""
    for context in context_info:
        prompt += f"- {context} \n"

    prompt += f"\nCorrectly answer the following question."
    prompt += f"\n{question} \n\nAnswer:"
    print(prompt)
    return prompt


def answer_question(question: str, game: str, context_info: List[str]):
    prompt = format_prompt(question, game, context_info)
    return complete_prompt(generator=generator, prompt=prompt)
