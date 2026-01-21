import re
import json

from project.infrastructure.exceptions.parsing_errors import JsonBlockNotFoundError, JsonParsingError, \
    OfferCountMissingError, OfferCountInvalidError
from project.infrastructure.logging.logger_config import setup_logger

logger = setup_logger(__name__)


def get_number_of_products(html: str) -> int:
    logger.debug("I'm starting the search for JSON_LD_PRODUCT in the HTML.")

    match = re.search(
        r'<script type="application/ld\+json" data-qa="JSON_LD_PRODUCT".*?>(.*?)</script>',
        html,
        re.DOTALL
    )

    if not match:
        message = "JSON_LD_PRODUCT not found in HTML"
        logger.error(message)
        raise JsonBlockNotFoundError(message)

    json_text = match.group(1).strip()
    logger.debug("JSON found, attempting to parse JSON-LD.")

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        message = "JSON_LD_PRODUCT parsing error"
        logger.exception(message)
        raise JsonParsingError(message) from exc

    offer_count = data.get("offers", {}).get("offerCount")

    if offer_count is None:
        message = "offerCount is missing in JSON_LD_PRODUCT"
        logger.warning(message)
        raise OfferCountMissingError(message)

    try:
        count = int(offer_count)
        logger.info(f"Number of items: {count}")
        return count
    except (TypeError, ValueError) as exc:
        message = f"offerCount has an incorrect value: {offer_count}"
        logger.error(message)
        raise OfferCountInvalidError(message) from exc
