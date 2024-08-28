#!/usr/bin/env python
from roko_summary.schemas import InputSchema
from roko_summary.db import get_messages_between_dates
from naptha_sdk.utils import get_logger
from ollama import Client
import yaml

logger = get_logger(__name__)


def run(
    inputs: InputSchema,
    worker_nodes=None,
    orchestrator_node=None,
    flow_run=None,
    cfg=None,
):
    """The Roko summary module is given an input directory in which it expects
    to find two sqlite databases: twitter.sqlite, telegram.sqlite which it 
    queries.
    """

    logger.info(f"Inputs: {inputs}")
    logger.debug(f"config = {cfg}")

    start_date = inputs.start_date
    end_date = inputs.end_date
    db_msgs = get_messages_between_dates(inputs.input_dir, start_date, end_date)

    messages = [{"role": "system", "content": cfg["inputs"]["system_message"]}]
    content = ""
    for m in db_msgs:
        content += f"{m['content']}\n"

    prompt = f"""
    Generate a comprehensive summary of community activity for the RokoNetwork project
    based on the following content.

    This content is noisy; ignore messages, posts or content that you cannot make sense of.

    Your summary should be coherent and logical, drawing only on the information provided.

    Reply with ONLY the summary in markdown format.

    CONTENT:
    {content}
    """

    logger.info(prompt)

    messages.append({"role": "user", "content": prompt})

    ollama_client = Client(host=cfg["models"]["ollama"]["api_base"])

    response = ollama_client.chat(
        model=cfg["models"]["ollama"]["model"], messages=messages
    )

    logger.debug(response)

    return response

if __name__ == "__main__":

    cfg_path = f"roko_summary/component.yaml"
    with open(cfg_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    inputs = InputSchema(
        start_date="2024-07-01 00:00:00", 
        end_date="2024-08-01 00:00:00", 
        input_dir="b2febe52defb4185b8c6adf6ac5b531b"
    )
    response = run(inputs, cfg)
