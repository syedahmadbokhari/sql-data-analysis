# GA4 Interview Story

## 30-second explanation

I extended a traditional retail transaction analytics project with a GA4 and GTM behavioural layer. The original platform showed what products sold and how revenue varied by brand, discount and time. The digital layer shows how users interact before purchase: product list views, product views, search, add-to-cart and checkout intent. This lets the analysis connect customer behaviour to product revenue without claiming synthetic or demo interactions are real production traffic.

## 60-second explanation

The project started as a retail data platform with Python ingestion, SQLite/PostgreSQL, dbt models, BigQuery scripts, Power BI/Tableau assets and a Streamlit dashboard. Because the existing Streamlit app is an analytics dashboard rather than a storefront, I added a small tracked retail demo page that reuses the same product catalogue data. GTM is injected from `GTM_CONTAINER_ID`, so no container ID is committed. The page pushes GA4 ecommerce-style events into `dataLayer`; GTM can then forward them to GA4. On the modelling side, I added a lightweight dbt staging/funnel example for GA4 export data rather than pretending a full live behavioural mart exists.

## 2-minute technical explanation

I first audited the repository and found that the web-facing app was Streamlit, focused on analytics and recommendations, not ecommerce browsing. Streamlit does not give the same stable client-side control as a normal storefront, so I avoided forcing GTM into it just to claim tracking. Instead, I built a minimal retail behaviour demo using the existing cleaned product tables from `data/retailDB.sqlite`. It serves the product list locally, injects GTM from an environment variable, and pushes structured `dataLayer` ecommerce events such as `view_item_list`, `select_item`, `search`, `view_item`, `add_to_cart` and `begin_checkout`.

For analytics engineering, I documented the GA4 tracking plan and added dbt model definitions that assume a GA4 BigQuery export or a clearly labelled synthetic fixture. `stg_ga4_events` validates recognised event names and `fct_digital_funnel` calculates step and overall conversion when the source data exists. Purchase is modelled but not fired in the demo because there is no real purchase workflow. I also added Python validation tests for event payloads, including required `item_id`, recognised event names and non-negative purchase value.

## Likely Interview Questions

| Topic | Question | Strong Answer Direction |
|---|---|---|
| GA4 | Why use events rather than pageviews only? | GA4 is event-based, so ecommerce behaviour can be modelled as funnel steps and item interactions. |
| GTM | What does GTM add? | It manages tags and event mapping without changing application code for every analytics change. |
| Event tracking | Why use standard ecommerce events? | They align with GA4 reporting and reduce unnecessary custom taxonomy. |
| Funnels | How do you calculate drop-off? | Count sessions reaching each step, then calculate step-to-step and overall conversion with null-safe denominators. |
| Conversion | Why did you not fire purchase? | The repo has no real checkout/payment workflow, so firing purchase would be misleading. |
| Sessions vs users | What is the difference? | Users identify browsers/devices; sessions group activity windows. Both matter for frequency and conversion. |
| Customer journeys | How do behavioural and transaction data join? | Via `item_id`/`product_id`, allowing engagement-to-revenue analysis. |
| Attribution | What are the limits of source/medium? | Attribution depends on tagging quality, consent, cross-device limits and GA4's attribution model. |
| BigQuery export | Why model GA4 in SQL? | Raw event exports are nested and granular; dbt creates reusable funnel, product and channel marts. |
| Data quality | What can go wrong? | Missing item IDs, invalid event names, duplicate transactions, bad timestamps and inconsistent ecommerce parameters. |
| Privacy/consent | What should be considered? | Consent mode, cookie banners, PII exclusion, data retention and regional compliance. |

## CV Bullet Options

**SAFE NOW:** Added an environment-driven GA4/GTM digital analytics demo to a retail analytics platform, documenting ecommerce event tracking and lightweight funnel modelling without committing tracking IDs or claiming production traffic.

**SAFE AFTER LIVE GA4 TESTING:** Integrated Google Tag Manager with GA4 event forwarding for a retail product demo, validating product list, search, item view, add-to-cart and checkout-intent events in GTM Preview and GA4 DebugView.

**SAFE ONLY AFTER BIGQUERY EXPORT IS CONNECTED:** Modelled GA4 BigQuery export data into session, product conversion and channel performance marts, joining behavioural engagement with transactional retail revenue for conversion analysis.
