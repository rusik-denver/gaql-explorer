"""Google Ads API client wrapper with credential management."""

import os
from pathlib import Path

from dotenv import load_dotenv


def _find_env() -> Path | None:
    for candidate in [Path.cwd() / ".env", Path.home() / ".gaql-explorer" / ".env"]:
        if candidate.exists():
            return candidate
    return None


class GoogleAdsClient:
    """Thin wrapper around google-ads that handles credential loading."""

    def __init__(self):
        env_path = _find_env()
        if env_path:
            load_dotenv(env_path)

        self.developer_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
        self.client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
        self.refresh_token = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
        self.login_customer_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
        self._client = None

    @property
    def is_configured(self) -> bool:
        return all([self.developer_token, self.client_id, self.client_secret, self.refresh_token])

    def _get_client(self):
        if self._client is None:
            try:
                from google.ads.googleads.client import GoogleAdsClient as GAC
            except ImportError:
                raise RuntimeError(
                    "google-ads package not installed. "
                    "Install with: pip install 'gaql-explorer[api]' or pip install google-ads"
                )
            self._client = GAC.load_from_dict({
                "developer_token": self.developer_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "login_customer_id": self.login_customer_id,
                "use_proto_plus": True,
            })
        return self._client

    def query(self, customer_id: str, query: str) -> tuple[list[str], list[dict]]:
        """Execute a GAQL query and return (headers, rows)."""
        client = self._get_client()
        service = client.get_service("GoogleAdsService")
        stream = service.search_stream(customer_id=customer_id.replace("-", ""), query=query)

        rows = []
        headers = []
        for batch in stream:
            for row in batch.results:
                row_dict = {}
                select_part = query.lower().split("from")[0].replace("select", "").strip()
                fields = [f.strip() for f in select_part.split(",")]
                for field in fields:
                    parts = field.split(".")
                    obj = row
                    for part in parts:
                        obj = getattr(obj, part, None)
                        if obj is None:
                            break
                    row_dict[field] = obj
                if not headers:
                    headers = list(row_dict.keys())
                rows.append(row_dict)

        return headers, rows

    def list_accounts(self) -> list[dict]:
        """List accessible customer accounts."""
        client = self._get_client()
        service = client.get_service("CustomerService")
        accessible = service.list_accessible_customers()
        accounts = []
        for resource_name in accessible.resource_names:
            cid = resource_name.split("/")[-1]
            try:
                ga_service = client.get_service("GoogleAdsService")
                result = ga_service.search(
                    customer_id=cid,
                    query="SELECT customer.id, customer.descriptive_name FROM customer LIMIT 1",
                )
                for row in result:
                    accounts.append({
                        "id": f"{cid[:3]}-{cid[3:6]}-{cid[6:]}",
                        "name": row.customer.descriptive_name,
                    })
            except Exception:
                accounts.append({"id": cid, "name": "(access denied)"})
        return accounts
