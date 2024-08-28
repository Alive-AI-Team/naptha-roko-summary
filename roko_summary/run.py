#!/usr/bin/env python
from roko_summary.schemas import InputSchema
from roko_summary.db import get_messages_between_dates
from naptha_sdk.utils import get_logger
from boto3.dynamodb.conditions import Key
from itertools import chain
from ollama import Client

logger = get_logger(__name__)


def run(
    inputs: InputSchema,
    worker_nodes=None,
    orchestrator_node=None,
    flow_run=None,
    cfg=None,
):
    logger.info(f"Inputs: {inputs}")
    logger.debug(f"config = {cfg}")

    start_date = inputs.start_date
    end_date = inputs.end_date
    db_msgs = get_messages_between_dates(inputs.input_dir, start_date, end_date)

    messages = [{"role": "system", "content": cfg["inputs"]["system_message"]}]
    content = ""
    for m in db_msgs:
        content += f"{m.content}\n"

    prompt = f"""
    Generate a comprehensive summary of community activity for the RokoNetwork project
    based on the following content.

    This content is noisy; ignore messages, posts or content that you cannot make sense of.

    Your summary should be coherent and logical, drawing only on the information provided.

    Reply with ONLY the summary in markdown format.

    CONTENT:
    {content}
    """

    messages.append({"role": "user", "content": prompt})

    ollama_client = Client(host=cfg["models"]["ollama"]["api_base"])

    response = ollama_client.chat(
        model=cfg["models"]["ollama"]["model"], messages=messages
    )

    logger.debug(response)

    return response
