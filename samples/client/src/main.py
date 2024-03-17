from typing import Dict
import httpx
from loguru import logger
import os

MOCK_REQUESTER_URL: str = "http://mock-requester:8000/collect"


def make_request_to_mock_requester(body: Dict | None = None):
    logger.info(
        f"Sending request to mock-requester using url '{MOCK_REQUESTER_URL}'..."
    )
    if body:
        logger.info(f"Sending body: ({body})")
        response = httpx.post(MOCK_REQUESTER_URL, json=body)
    else:
        response = httpx.post(MOCK_REQUESTER_URL)
    logger.info(
        f"Request to mock-requester was sent. Got status code '{response.status_code}'"
    )


EXTERNAL_API_FIRST_URL: str = "http://external-api:8000/request-history"
EXTERNAL_API_SECOND_URL: str = "http://external-api-second:8000/request-history"


def make_request_to_external_api_first():
    logger.info(f"Sending request to external-api using url '{EXTERNAL_API_FIRST_URL}'...")
    response = httpx.get(EXTERNAL_API_FIRST_URL)
    logger.info(response.json())

def make_request_to_external_api_second():
    logger.info(f"Sending request to external-api-second using url '{EXTERNAL_API_SECOND_URL}'...")
    response = httpx.get(EXTERNAL_API_SECOND_URL)
    logger.info(response.json())


def simple_request_scenario():
    logger.info("CLIENT starting.")
    logger.info("Checking history from external-api. There should be no history yet.")
    make_request_to_external_api_first()
    make_request_to_mock_requester()
    logger.info(
        "Sending request to external-api once again to see the history of requests."
    )
    make_request_to_external_api_first()


def simple_request_with_placeholder_scenario():
    logger.info("CLIENT starting.")
    logger.info("Checking history from external-api. There should be no history yet.")
    make_request_to_external_api_first()
    make_request_to_mock_requester({"givenKey": "ThisIsGivenKeyFromClient"})
    logger.info(
        "Sending request to external-api once again to see the history of requests."
    )
    make_request_to_external_api_first()


def request_chain_with_values_from_side_effects_scenario():
    logger.info("CLIENT starting.")
    logger.info("Checking history from external-api. There should be no history yet.")
    make_request_to_external_api_first()
    logger.info("Checking history from external-api-second. There should be no history yet.")
    make_request_to_external_api_second()
    make_request_to_mock_requester()
    logger.info(
        "Sending request to external-api once again to see the history of requests."
    )
    make_request_to_external_api_first()
    logger.info(
        "Sending request to external-api-second once again to see the history of requests."
    )
    make_request_to_external_api_second()


if __name__ == "__main__":
    scenario = os.environ.get("SCENARIO")
    logger.info(f"Chosen scenario: {scenario}")
    if scenario == "simple-request":
        simple_request_scenario()
    elif scenario == "simple-request-with-placeholder":
        simple_request_with_placeholder_scenario()
    elif scenario == "request-chain-with-values-from-side-effects":
        request_chain_with_values_from_side_effects_scenario()

