#!/usr/bin/env python
from roko_summary.schemas import InputSchema
from roko_summary.aws import get_dynamodb
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

    dynamodb = get_dynamodb()
    table = dynamodb.Table("social-posts")

    start_date = inputs.start_date
    end_date = inputs.end_date
    sources = inputs.sources

    items = list(
        chain.from_iterable(
            table.query(
                KeyConditionExpression=Key("source").eq(source)
                & Key("created_at").between(start_date, end_date),
                ScanIndexForward=False,
            ).get("Items", [])
            for source in sources
        )
    )

    messages = [{"role": "system", "content": cfg["inputs"]["system_message"]}]

    sources_str = ", ".join(sources)

    content = "\n\n".join(
        (
            "\n"
            + ("Tweet" if item["source"] == "twitter" else "Message")
            + ": "
            + item["text"]
        )
        for item in items
    )

    prompt = f"""
    Generate a summary of community activity for the RokoNetwork project
    based on the following content from {sources_str}

    This content is noisy; ignore messages, posts or content that you cannot make sense of.

    Your summary should be coherent and logical, drawing only on the information provided.

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
