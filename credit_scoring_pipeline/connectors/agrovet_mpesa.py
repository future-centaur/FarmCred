"""M-Pesa / agrovet till connector.

Feeds Cash-Flow Stability only. Derived from Till/Paybill classification of
mobile-money statements, not a general-purpose agrovet supplier API (PRD s8 --
iProcure is defunct and the sector is paper/cash-based).
"""

from __future__ import annotations

from typing import Any, Dict

from data.mock_farmers import get_source_payload

from .base import BaseConnector
from . import register


@register
class MockAgrovetMpesaConnector(BaseConnector):
    source = "agrovet_mpesa"
    mode = "mock"
    provenance = "Synthetic M-Pesa statement pulls, Till/Paybill-classified."

    def fetch(self, farmer_id: str) -> Dict[str, Any]:
        self._simulate_latency()
        return get_source_payload(farmer_id, self.source)
