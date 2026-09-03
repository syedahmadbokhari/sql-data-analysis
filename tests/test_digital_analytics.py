import pytest

from src.digital_analytics.product_catalog import load_demo_products
from src.digital_analytics.tracking import (
    DigitalAnalyticsValidationError,
    validate_event_payload,
)


def test_load_demo_products_uses_existing_catalogue():
    products = load_demo_products(limit=3)
    assert len(products) == 3
    assert {"item_id", "item_name", "item_brand", "price", "currency"} <= set(products[0])
    assert products[0]["currency"] == "GBP"


def test_valid_item_event_payload_passes():
    payload = {
        "event": "view_item",
        "ecommerce": {
            "items": [{
                "item_id": "SKU123",
                "item_name": "Demo Shoe",
                "price": 79.99,
                "discount": 0.2,
            }]
        },
    }
    assert validate_event_payload(payload) is True


def test_item_event_requires_item_id():
    payload = {
        "event": "add_to_cart",
        "ecommerce": {"items": [{"item_name": "Missing ID"}]},
    }
    with pytest.raises(DigitalAnalyticsValidationError, match="item_id"):
        validate_event_payload(payload)


def test_purchase_requires_transaction_id_and_non_negative_value():
    payload = {
        "event": "purchase",
        "ecommerce": {
            "value": -1,
            "items": [{"item_id": "SKU123", "price": 10}],
        },
    }
    with pytest.raises(DigitalAnalyticsValidationError, match="transaction_id"):
        validate_event_payload(payload)


def test_unknown_event_is_rejected():
    with pytest.raises(DigitalAnalyticsValidationError, match="Unrecognised event"):
        validate_event_payload({"event": "made_up_event"})
