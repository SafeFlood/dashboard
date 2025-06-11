import os
import json
import ee
from dotenv import load_dotenv

load_dotenv()


class GEEDataRetriever:
    def __init__(self, service_account_path: str):
        self.service_account_path = service_account_path
        self.ee_initialized = False
        self._initialize_ee()

    def _initialize_ee(self):
        """Initialize Earth Engine with service account authentication"""
        try:
            if self.service_account_path and os.path.exists(self.service_account_path):
                with open(self.service_account_path, "r") as f:
                    service_account_info = json.load(f)

                credentials = ee.ServiceAccountCredentials(
                    service_account_info["client_email"], self.service_account_path
                )
        
                ee.Initialize(credentials, project=service_account_info["project_id"])

            self.ee_initialized = True

        except Exception as e:
            self.ee_initialized = False
            raise RuntimeError(f"Failed to initialize Earth Engine: {e}")


gee_data_retriever = GEEDataRetriever(
    service_account_path=os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
)
