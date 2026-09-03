-- Fact: reusable product/list-view to checkout/purchase funnel by channel/device.
-- Missing steps remain zero; the model does not invent checkout or purchase
-- behaviour when events are absent.

SELECT
    event_date,
    source,
    medium,
    campaign,
    device_category,
    COUNT(DISTINCT CASE WHEN event_name = 'view_item_list' THEN session_id END) AS list_view_sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN session_id END) AS product_view_sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END) AS add_to_cart_sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN session_id END) AS checkout_sessions,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END) AS purchase_sessions,
    COUNT(DISTINCT session_id) AS total_sessions,
    1.0 * COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view_item_list' THEN session_id END), 0)
        AS list_to_product_view_rate,
    1.0 * COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN session_id END), 0)
        AS product_view_to_cart_rate,
    1.0 * COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN session_id END), 0)
        AS cart_to_checkout_rate,
    1.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN session_id END), 0)
        AS checkout_to_purchase_rate,
    1.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN session_id END)
        / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view_item_list' THEN session_id END), 0)
        AS overall_funnel_conversion_rate,
    MAX(CASE WHEN is_synthetic THEN 1 ELSE 0 END) AS contains_synthetic_data
FROM {{ ref('stg_ga4_events') }}
GROUP BY event_date, source, medium, campaign, device_category
