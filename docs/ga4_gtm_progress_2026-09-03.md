# GA4 + GTM Progress — 2026-09-03

Session log for the GA4/GTM implementation work on the retail behaviour demo. This is a progress snapshot, not a claim that GA4 reporting is live end-to-end.

## Setup

- Local demo: `http://127.0.0.1:8502`
- GTM container: `GTM-N4N67DV6`
- GA4 Measurement ID: `G-B3JSWF5WRX`
- The demo uses environment-driven GTM injection: `GTM_CONTAINER_ID` is read server-side (`src/digital_analytics/demo_site.py`) and written into the page as `window.RETAIL_ANALYTICS_CONFIG`, which the page's inline loader script uses to inject the GTM container script. No container ID is hardcoded or committed.

## A. Confirmed working

- The demo server correctly injects the GTM container ID into the served HTML and loads `googletagmanager.com/gtm.js` for `GTM-N4N67DV6` only when `GTM_CONTAINER_ID` is set.
- GTM Tag Assistant successfully connects to the local demo at `http://127.0.0.1:8502`.
- Base tag `Google Tag - GA4` is configured with Measurement ID `G-B3JSWF5WRX`, firing on `Initialization - All Pages`.
- GA4 event tag `GA4 Event - view_item_list` is configured with Measurement ID `G-B3JSWF5WRX`, triggered by custom trigger `CE - view_item_list` listening for the custom `dataLayer` event `view_item_list`.
- Tag Assistant shows `GA4 Event - view_item_list` as **Succeeded**.
- Chrome DevTools Network tab, captured while using the Tag Assistant-connected Preview tab, shows GA4 `collect` requests containing `G-B3JSWF5WRX` returning HTTP **204**.
- `tests/test_digital_analytics.py` passed **5/5**.
- `purchase` remains unfired by the demo — there is no genuine checkout/payment workflow, so no purchase event is sent to GA4.

## B. Still unverified

- **GA4 DebugView shows 0 debug devices / 0 events**, despite the `collect` requests above returning 204. This is the key open issue.
- `debug_mode=true` was attempted during this session but DebugView was still empty by the end of the session.
- GA4 Realtime has not been separately confirmed to show demo traffic.
- The GA4 BigQuery export → dbt layer (`stg_ga4_events`, `fct_digital_funnel`) is still proposed/future work — it is not wired to any live GA4 BigQuery export and has not run against real behavioural data.

## C. Next-session troubleshooting steps

1. Re-check that the GA4 Event tag is actually attached to the same GA4 property/stream as the one being viewed in DebugView (property/stream mismatch is the most common cause of "204 but no DebugView events").
2. Confirm `debug_mode=true` is being sent as an event parameter on the GA4 event tag itself (not just appended to the page URL), and that it's present in the request payload, not only the config tag.
3. Check whether an ad blocker, Consent Mode default, or `SameSite`/cookie setting in the browser session is suppressing GA4 from associating the hit with a debug device.
4. Try the GA4 DebugView "debug device" via the GA4/GTM Chrome extension explicitly, rather than relying solely on the `debug_mode` parameter.
5. Inspect the raw `collect` request payload (query string) in Network tab for the `_dbg` / `dbg` parameter to confirm debug mode is actually reaching GA4, not just requested.
6. If DebugView still shows nothing after the above, test firing the same tag from GTM's own Preview "Debug your site" against a minimal blank page to isolate whether the issue is demo-specific or GTM/GA4-configuration-specific.

## Known limitation as of end of session

GA4 `collect` requests for `G-B3JSWF5WRX` return HTTP 204 (accepted) in Chrome Network, and Tag Assistant reports the tag as Succeeded, but GA4 DebugView still shows 0 debug devices and 0 events. GA4 is not yet confirmed to be receiving/processing these events end-to-end — only that the browser successfully sent them.
