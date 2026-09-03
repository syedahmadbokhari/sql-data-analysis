-- Staging: GA4 ecommerce events exported to BigQuery.
-- This model expects a GA4 BigQuery export-style source. Local development may
-- use a clearly labelled synthetic fixture with the same flattened columns.

SELECT
    event_id,
    user_pseudo_id,
    session_id,
    event_name,
    event_timestamp,
    event_date,
    page_location,
    source,
    medium,
    campaign,
    device_category,
    new_vs_returning,
    item_id,
    item_name,
    item_brand,
    item_category,
    price,
    quantity,
    discount,
    currency,
    transaction_id,
    value,
    is_synthetic
FROM {{ source('digital_raw', 'raw_ga4_events') }}
WHERE event_name IN (
    'page_view',
    'view_item_list',
    'select_item',
    'search',
    'view_item',
    'add_to_cart',
    'view_cart',
    'begin_checkout',
    'purchase',
    'filter_applied',
    'dashboard_interaction'
)
  AND event_timestamp IS NOT NULL
