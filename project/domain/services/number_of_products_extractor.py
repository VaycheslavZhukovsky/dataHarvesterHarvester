import re
import json

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
        logger.error("JSON_LD_PRODUCT not found in HTML")
        return 0

    json_text = match.group(1).strip()
    logger.debug("JSON found, attempting to parse JSON-LD.")

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        logger.exception("JSON_LD_PRODUCT parsing error")
        return 0

    offer_count = data.get("offers", {}).get("offerCount")

    if offer_count is None:
        logger.warning("offerCount is missing in JSON_LD_PRODUCT")
        return 0

    try:
        count = int(offer_count)
        logger.info(f"Number of items: {count}")
        return count
    except (TypeError, ValueError):
        logger.error(f"offerCount has an incorrect value: {offer_count}")
        return 0
