"""Satellite/climate connector.

Feeds Climate Exposure only -- never the eligibility gates, never the weighted
score (PRD s8). ``config.FORCE_NDVI_TIMEOUT`` deliberately forces the
unavailable path so a demo can prove a failed pull resolves to the neutral
band rather than crashing or silently scoring as a zero.
"""

from __future__ import annotations

from typing import Any, Dict

import config
from data.mock_farmers import get_source_payload

from .base import BaseConnector, ConnectorUnavailableError
from . import register


@register
class MockClimateConnector(BaseConnector):
    source = "climate"
    mode = "mock"
    provenance = "Synthetic NDVI/rainfall-deficit series, CHIRPS/Sentinel-2-shaped."

    def fetch(self, farmer_id: str) -> Dict[str, Any]:
        self._simulate_latency()
        if config.FORCE_NDVI_TIMEOUT:
            raise ConnectorUnavailableError(self.source, "forced timeout (debug flag)")
        return get_source_payload(farmer_id, self.source)
