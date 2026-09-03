import json
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

from src.digital_analytics.product_catalog import load_demo_products, project_root


DEMO_DIR = project_root() / "digital_demo"


class RetailDemoHandler(SimpleHTTPRequestHandler):
    """Serve the tracked demo with env-driven GA4/GTM configuration."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DEMO_DIR), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._serve_index()
            return
        if path == "/products.json":
            self._serve_products()
            return
        super().do_GET()

    def _serve_index(self):
        html = (DEMO_DIR / "index.html").read_text(encoding="utf-8")
        config = {
            "gtmContainerId": os.getenv("GTM_CONTAINER_ID", ""),
        }
        html = html.replace("__RETAIL_ANALYTICS_CONFIG__", json.dumps(config))
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _serve_products(self):
        body = json.dumps(load_demo_products())
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


def run(host: str = "127.0.0.1", port: int = 8502) -> None:
    gtm_container_id = os.getenv("GTM_CONTAINER_ID", "")
    server = ThreadingHTTPServer((host, port), RetailDemoHandler)
    print(f"Retail GA4/GTM demo running at http://{host}:{port}")
    if gtm_container_id:
        print(f"GTM enabled: {gtm_container_id}")
    else:
        print("Set GTM_CONTAINER_ID before launch to enable GTM injection.")
    server.serve_forever()


if __name__ == "__main__":
    run()
