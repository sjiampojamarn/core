"""Test the Aranet sensors."""

import pytest

from homeassistant.components.aranet.const import DOMAIN
from homeassistant.components.sensor import ATTR_OPTIONS, ATTR_STATE_CLASS
from homeassistant.const import ATTR_FRIENDLY_NAME, ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from . import (
    DISABLED_INTEGRATIONS_SERVICE_INFO,
    VALID_ARANET2_DATA_SERVICE_INFO,
    VALID_ARANET_RADIATION_DATA_SERVICE_INFO,
    VALID_ARANET_RADON_DATA_SERVICE_INFO,
    VALID_DATA_SERVICE_INFO,
)

from tests.common import MockConfigEntry
from tests.components.bluetooth import inject_bluetooth_service_info


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_aranet_radiation(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test setting up creates the sensors for Aranet Radiation device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, VALID_ARANET_RADIATION_DATA_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 4

    batt_sensor = hass.states.get("sensor.aranet_12345_battery")
    batt_sensor_attrs = batt_sensor.attributes
    assert batt_sensor.state == "100"
    assert batt_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet\u2622 12345 Battery"
    assert batt_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert batt_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    humid_sensor = hass.states.get("sensor.aranet_12345_radiation_total_dose")
    humid_sensor_attrs = humid_sensor.attributes
    assert humid_sensor.state == "0.011616"
    assert (
        humid_sensor_attrs[ATTR_FRIENDLY_NAME]
        == "Aranet\u2622 12345 Radiation Total Dose"
    )
    assert humid_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "mSv"
    assert humid_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    temp_sensor = hass.states.get("sensor.aranet_12345_radiation_dose_rate")
    temp_sensor_attrs = temp_sensor.attributes
    assert temp_sensor.state == "0.11"
    assert (
        temp_sensor_attrs[ATTR_FRIENDLY_NAME]
        == "Aranet\u2622 12345 Radiation Dose Rate"
    )
    assert temp_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "μSv/h"
    assert temp_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    interval_sensor = hass.states.get("sensor.aranet_12345_update_interval")
    interval_sensor_attrs = interval_sensor.attributes
    assert interval_sensor.state == "300"
    assert (
        interval_sensor_attrs[ATTR_FRIENDLY_NAME]
        == "Aranet\u2622 12345 Update Interval"
    )
    assert interval_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "s"
    assert interval_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    # Check device context for the battery sensor
    entity = entity_registry.async_get("sensor.aranet_12345_battery")
    device = device_registry.async_get(entity.device_id)
    assert device.name == "Aranet☢ 12345"
    assert device.model == "Aranet Radiation"
    assert device.sw_version == "v1.4.38"
    assert device.manufacturer == "SAF Tehnika"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_aranet2(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test setting up creates the sensors for Aranet2 device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, VALID_ARANET2_DATA_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 4

    batt_sensor = hass.states.get("sensor.aranet2_12345_battery")
    batt_sensor_attrs = batt_sensor.attributes
    assert batt_sensor.state == "79"
    assert batt_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet2 12345 Battery"
    assert batt_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert batt_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    humid_sensor = hass.states.get("sensor.aranet2_12345_humidity")
    humid_sensor_attrs = humid_sensor.attributes
    assert humid_sensor.state == "52.4"
    assert humid_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet2 12345 Humidity"
    assert humid_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert humid_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    temp_sensor = hass.states.get("sensor.aranet2_12345_temperature")
    temp_sensor_attrs = temp_sensor.attributes
    assert temp_sensor.state == "24.8"
    assert temp_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet2 12345 Temperature"
    assert temp_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "°C"
    assert temp_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    interval_sensor = hass.states.get("sensor.aranet2_12345_update_interval")
    interval_sensor_attrs = interval_sensor.attributes
    assert interval_sensor.state == "60"
    assert interval_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet2 12345 Update Interval"
    assert interval_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "s"
    assert interval_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    # Check device context for the battery sensor
    entity = entity_registry.async_get("sensor.aranet2_12345_battery")
    device = device_registry.async_get(entity.device_id)
    assert device.name == "Aranet2 12345"
    assert device.model == "Aranet2"
    assert device.sw_version == "v1.4.4"
    assert device.manufacturer == "SAF Tehnika"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_aranet4(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test setting up creates the sensors for Aranet4 device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, VALID_DATA_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 7

    batt_sensor = hass.states.get("sensor.aranet4_12345_battery")
    batt_sensor_attrs = batt_sensor.attributes
    assert batt_sensor.state == "89"
    assert batt_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Battery"
    assert batt_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert batt_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    co2_sensor = hass.states.get("sensor.aranet4_12345_carbon_dioxide")
    co2_sensor_attrs = co2_sensor.attributes
    assert co2_sensor.state == "650"
    assert co2_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Carbon Dioxide"
    assert co2_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "ppm"
    assert co2_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    humid_sensor = hass.states.get("sensor.aranet4_12345_humidity")
    humid_sensor_attrs = humid_sensor.attributes
    assert humid_sensor.state == "34"
    assert humid_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Humidity"
    assert humid_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert humid_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    temp_sensor = hass.states.get("sensor.aranet4_12345_temperature")
    temp_sensor_attrs = temp_sensor.attributes
    assert temp_sensor.state == "21.1"
    assert temp_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Temperature"
    assert temp_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "°C"
    assert temp_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    press_sensor = hass.states.get("sensor.aranet4_12345_pressure")
    press_sensor_attrs = press_sensor.attributes
    assert press_sensor.state == "990.5"
    assert press_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Pressure"
    assert press_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "hPa"
    assert press_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    interval_sensor = hass.states.get("sensor.aranet4_12345_update_interval")
    interval_sensor_attrs = interval_sensor.attributes
    assert interval_sensor.state == "300"
    assert interval_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Update Interval"
    assert interval_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "s"
    assert interval_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    status_sensor = hass.states.get("sensor.aranet4_12345_threshold")
    status_sensor_attrs = status_sensor.attributes
    assert status_sensor.state == "green"
    assert status_sensor_attrs[ATTR_FRIENDLY_NAME] == "Aranet4 12345 Threshold"
    assert status_sensor_attrs[ATTR_OPTIONS] == ["error", "green", "yellow", "red"]

    # Check device context for the battery sensor
    entity = entity_registry.async_get("sensor.aranet4_12345_battery")
    device = device_registry.async_get(entity.device_id)
    assert device.name == "Aranet4 12345"
    assert device.model == "Aranet4"
    assert device.sw_version == "v1.2.0"
    assert device.manufacturer == "SAF Tehnika"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_aranetrn(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test setting up creates the sensors for Aranet Radon device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, VALID_ARANET_RADON_DATA_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 7

    batt_sensor = hass.states.get("sensor.aranetrn_12345_battery")
    batt_sensor_attrs = batt_sensor.attributes
    assert batt_sensor.state == "100"
    assert batt_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Battery"
    assert batt_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert batt_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    co2_sensor = hass.states.get("sensor.aranetrn_12345_radon_concentration")
    co2_sensor_attrs = co2_sensor.attributes
    assert co2_sensor.state == "7"
    assert co2_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Radon Concentration"
    assert co2_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "Bq/m³"
    assert co2_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    humid_sensor = hass.states.get("sensor.aranetrn_12345_humidity")
    humid_sensor_attrs = humid_sensor.attributes
    assert humid_sensor.state == "46.2"
    assert humid_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Humidity"
    assert humid_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "%"
    assert humid_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    temp_sensor = hass.states.get("sensor.aranetrn_12345_temperature")
    temp_sensor_attrs = temp_sensor.attributes
    assert temp_sensor.state == "25.5"
    assert temp_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Temperature"
    assert temp_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "°C"
    assert temp_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    press_sensor = hass.states.get("sensor.aranetrn_12345_pressure")
    press_sensor_attrs = press_sensor.attributes
    assert press_sensor.state == "1018.5"
    assert press_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Pressure"
    assert press_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "hPa"
    assert press_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    interval_sensor = hass.states.get("sensor.aranetrn_12345_update_interval")
    interval_sensor_attrs = interval_sensor.attributes
    assert interval_sensor.state == "600"
    assert (
        interval_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Update Interval"
    )
    assert interval_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == "s"
    assert interval_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    status_sensor = hass.states.get("sensor.aranetrn_12345_threshold")
    status_sensor_attrs = status_sensor.attributes
    assert status_sensor.state == "green"
    assert status_sensor_attrs[ATTR_FRIENDLY_NAME] == "AranetRn+ 12345 Threshold"
    assert status_sensor_attrs[ATTR_OPTIONS] == ["error", "green", "yellow", "red"]

    # Check device context for the battery sensor
    entity = entity_registry.async_get("sensor.aranetrn_12345_battery")
    device = device_registry.async_get(entity.device_id)
    assert device.name == "AranetRn+ 12345"
    assert device.model == "Aranet Radon Plus"
    assert device.sw_version == "v1.6.4"
    assert device.manufacturer == "SAF Tehnika"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_smart_home_integration_disabled(hass: HomeAssistant) -> None:
    """Test disabling smart home integration marks entities as unavailable."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="aa:bb:cc:dd:ee:ff",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, DISABLED_INTEGRATIONS_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 0

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
