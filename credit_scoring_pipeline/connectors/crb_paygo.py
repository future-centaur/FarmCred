"""Credit-bureau / PAYGo tradeline connector.

Feeds the active-insolvency eligibility gate, the Repayment History band, and
-- via ``sunculture_owner`` -- an irrigation-mitigation input to Climate
Exposure. PAYGo tradelines (M-KOPA and similar) arrive inside this payload
rather than through a separate bilateral integration (PRD s8).
"""

from __future__ import annotations

from typing import Any, Dict

from data.mock_farmers import get_source_payload

from .base import BaseConnector
from . import register


@register
class MockCRBPaygoConnector(BaseConnector):
    source = "crb_paygo"
    mode = "mock"
    provenance = "Synthetic Metropol-shaped bureau file, including PAYGo tradelines."

    def fetch(self, farmer_id: str) -> Dict[str, Any]:
        self._simulate_latency()
        return get_source_payload(farmer_id, self.source)
