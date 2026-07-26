import config
from connectors import ConnectorUnavailableError, get_all_connectors, get_connector


def test_every_source_has_a_registered_mock_connector():
    connectors = get_all_connectors()
    assert set(connectors) == set(config.CONNECTOR_SOURCES)


def test_fetch_returns_dict_for_known_and_unknown_farmer():
    kiamis = get_connector("kiamis")
    assert isinstance(kiamis.fetch("F001"), dict)
    assert kiamis.fetch("F001")["national_id"] == "22334455"


def test_absent_source_returns_empty_dict_not_none():
    cooperative = get_connector("cooperative")
    # F002 has no cooperative record at all -- healthy source, no record.
    assert cooperative.fetch("F002") == {}


def test_force_ndvi_timeout_raises_connector_unavailable():
    config.FORCE_NDVI_TIMEOUT = True
    try:
        climate = get_connector("climate")
        try:
            climate.fetch("F001")
            assert False, "expected ConnectorUnavailableError"
        except ConnectorUnavailableError as exc:
            assert exc.source == "climate"
    finally:
        config.FORCE_NDVI_TIMEOUT = False


def test_unknown_source_raises_lookup_error():
    try:
        get_connector("not_a_real_source")
        assert False, "expected LookupError"
    except LookupError:
        pass
