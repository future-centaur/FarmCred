"""Cooperative / off-taker delivery-history connector.

Feeds Market Linkage, Social Collateral, and (as a repayment proxy) Repayment
History. Many smallholders belong to no cooperative at all -- that resolves to
``{}``, not a negative signal.
"""

from __future__ import annotations

from typing import Any, Dict

from data.mock_farmers import get_source_payload

from .base import BaseConnector
from . import register


@register
class MockCooperativeConnector(BaseConnector):
    source = "cooperative"
    mode = "mock"
    provenance = "Synthetic co-op delivery ledgers (KTDA-shaped) for demo profiles."

    def fetch(self, farmer_id: str) -> Dict[str, Any]:
        self._simulate_latency()
        return get_source_payload(farmer_id, self.source)
