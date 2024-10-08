#!/usr/bin/env python
from roko_summary.schemas import InputSchema
from roko_summary.db import get_messages_between_dates
from naptha_sdk.utils import get_logger
from openai import OpenAI

logger = get_logger(__name__)


def run(inputs: InputSchema, *args, **kwargs):
    """The Roko summary module is given an input directory in which it expects
    to find two sqlite databases: twitter.sqlite, telegram.sqlite which it 
    queries.
    """

    if "cfg" not in kwargs.keys():
        logger.error("Configuration error.")
        return
    cfg = kwargs["cfg"]

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
    for dates ranging from {start_date} to {end_date} based on the following content, 
    delimited by triple backticks.

    This content is noisy; ignore messages, posts or content that you cannot make sense of.

    Your summary should be coherent and logical, drawing only on the information provided.
    Include a mention of any new members that have been added to the community.

    Reply with ONLY the summary in markdown format.

    CONTENT:
    ```
    {content}
    ```
    """

    messages.append({"role": "user", "content": prompt})

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    response = completion.choices[0].message.content

    return response
