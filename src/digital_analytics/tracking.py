STANDARD_EVENTS = {
    "page_view",
    "view_item_list",
    "select_item",
    "search",
    "view_item",
    "add_to_cart",
    "view_cart",
    "begin_checkout",
    "purchase",
}

CUSTOM_EVENTS = {
    "filter_applied",
    "dashboard_interaction",
}

ITEM_EVENTS = {
    "view_item_list",
    "select_item",
    "view_item",
    "add_to_cart",
    "view_cart",
    "begin_checkout",
    "purchase",
}


class DigitalAnalyticsValidationError(ValueError):
    """Raised when a behavioural event payload cannot be trusted analytically."""


def validate_event_payload(payload: dict) -> bool:
    """Validate the GA4-style ecommerce payloads used by the demo and dbt docs."""
    event_name = payload.get("event")
    if event_name not in STANDARD_EVENTS | CUSTOM_EVENTS:
        raise DigitalAnalyticsValidationError(f"Unrecognised event: {event_name}")

    ecommerce = payload.get("ecommerce", {})
    items = ecommerce.get("items", [])

    if event_name in ITEM_EVENTS:
        if not items:
            raise DigitalAnalyticsValidationError(f"{event_name} requires ecommerce.items")
        for item in items:
            if not item.get("item_id"):
                raise DigitalAnalyticsValidationError(f"{event_name} item_id cannot be null")
            if item.get("price") is not None and float(item["price"]) < 0:
                raise DigitalAnalyticsValidationError(f"{event_name} price cannot be negative")
            if item.get("discount") is not None and float(item["discount"]) < 0:
                raise DigitalAnalyticsValidationError(f"{event_name} discount cannot be negative")

    if event_name == "purchase":
        if not ecommerce.get("transaction_id"):
            raise DigitalAnalyticsValidationError("purchase requires transaction_id")
        if float(ecommerce.get("value", 0)) < 0:
            raise DigitalAnalyticsValidationError("purchase value cannot be negative")

    return True

