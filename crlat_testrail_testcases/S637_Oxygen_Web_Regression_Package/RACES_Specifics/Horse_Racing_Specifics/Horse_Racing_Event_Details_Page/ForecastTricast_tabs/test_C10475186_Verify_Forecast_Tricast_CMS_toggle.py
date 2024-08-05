import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C10475186_Verify_Forecast_Tricast_CMS_toggle(Common):
    """
    TR_ID: C10475186
    NAME: Verify Forecast/Tricast CMS toggle
    DESCRIPTION: This test case verifies functionality of Forecast/Tricast feature toggle in CMS
    PRECONDITIONS: 1. Forecast/Tricast feature toggle is created and enabled: CMS > System Configuration > Structure > forecastTricastRacing
    PRECONDITIONS: 2. HR event with Forecast/Tricast available exists.
    PRECONDITIONS: 3. User should have a Horse Racing event detail page open ("Forecast/Tricast" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Forecast/Tricast' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Forecast/Tricast" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Forecast/Tricast are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Forecast/Tricast' tab
    """
    keep_browser_open = True

    def test_001_verify_forecasttricast_tabs(self):
        """
        DESCRIPTION: Verify Forecast/Tricast tabs
        EXPECTED: Forecast/Tricast tabs are displayed on EDP
        """
        pass

    def test_002_disable_forecasttricastracing_config_in_cmsreload_page(self):
        """
        DESCRIPTION: Disable forecastTricastRacing config in CMS.
        DESCRIPTION: Reload page
        EXPECTED: Forecast/Tricast tabs are not displayed on EDP
        """
        pass
