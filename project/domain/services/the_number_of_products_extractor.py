import json
import re


def get_the_number_of_products(html) -> int:
    match = re.search(
        r'<script type="application/ld\+json" data-qa="JSON_LD_PRODUCT".*?>(.*?)</script>',
        html,
        re.DOTALL
    )
    if match:
        json_text = match.group(1).strip()
        data = json.loads(json_text)

        offer_count = data.get("offers", {}).get("offerCount")
        return int(offer_count)
    else:
        print("JSON_LD_PRODUCT не найден")
