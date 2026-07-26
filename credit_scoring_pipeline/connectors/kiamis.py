"""KIAMIS registry connector.

Feeds the identity/geography eligibility gates and the Production Capacity
structuring band. Every registered farmer has a KIAMIS record by definition
(it is the national land/identity registry) -- an empty dict here would mean
the registry itself has no entry, which the mock data never models.
"""

from __future__ import annotations

from typing import Any, Dict

from data.mock_farmers import get_source_payload

from .base import BaseConnector
from . import register


@register
class MockKIAMISConnector(BaseConnector):
    source = "kiamis"
    mode = "mock"
    provenance = "Synthetic registry records mirroring the KIAMIS response shape."

    def fetch(self, farmer_id: str) -> Dict[str, Any]:
        self._simulate_latency()
        return get_source_payload(farmer_id, self.source)
