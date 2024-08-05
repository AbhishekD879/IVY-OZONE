import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C10474867_Verify_Forecast__Tricast_tabs_displaying_on_Greyhound_EDP_depending_on_checkboxes_in_Openbet_TI(Common):
    """
    TR_ID: C10474867
    NAME: Verify Forecast / Tricast tabs displaying on Greyhound EDP depending on checkboxes in Openbet TI
    DESCRIPTION: This test case verifies  Forecast / Tricast tabs displaying depending on checkboxes in Openbet TI
    PRECONDITIONS: 1. GH event with Win or Each Way market exists.
    PRECONDITIONS: 2. Forecast and Tricast checkboxes are active on market level for Win or Each Way market for event from precondition 1
    PRECONDITIONS: 3. OB TI:
    PRECONDITIONS: - Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments#LadbrokesEnvironments-LadbrokesOB/IMSendpoints
    PRECONDITIONS: 4. User is on Event details page for event from precondition 1
    PRECONDITIONS: 5. To verify SS response check EventToOutcomeForEvent
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 5 flags from SS respone responsible for Forecast/Tricast:
    PRECONDITIONS: ncastTypeCodes="CT,SF,CF,RF,TC,"
    PRECONDITIONS: CT - Combinational Tricast
    PRECONDITIONS: SF - Straight Forecast
    PRECONDITIONS: CF - Combinational Forecast
    PRECONDITIONS: RF - Reverse Forecast
    PRECONDITIONS: TC - Straight Tricast
    """
    keep_browser_open = True

    def test_001_verify_forecasttricast_tabs_on_edp(self):
        """
        DESCRIPTION: Verify Forecast/Tricast tabs on EDP
        EXPECTED: * Forecast and Tricast tabs are present on
        EXPECTED: * All 5 flags present in  SS response:
        EXPECTED: ncastTypeCodes="CT,SF,CF,RF,TC,"
        """
        pass

    def test_002_in_ti_uncheck_forecast_tabrefresh_app(self):
        """
        DESCRIPTION: In TI uncheck Forecast tab.
        DESCRIPTION: Refresh app
        EXPECTED: * Forecast tab in not present on EDP
        EXPECTED: * flags present in  SS response:
        EXPECTED: ncastTypeCodes="CT,TC,"
        """
        pass

    def test_003_in_ti_uncheck_tricast_checkboxrefresh_app(self):
        """
        DESCRIPTION: In TI uncheck Tricast checkbox.
        DESCRIPTION: Refresh app
        EXPECTED: * Tricast tab is not present on EDP
        EXPECTED: *  'ncastTypeCodes' parameter is not present in SS response
        """
        pass

    def test_004_in_ti_check_only_forecast_checkboxrefresh_app(self):
        """
        DESCRIPTION: In TI check only Forecast checkbox.
        DESCRIPTION: Refresh app
        EXPECTED: *Forecast tab is present on EDP
        EXPECTED: * flags present in  SS response:
        EXPECTED: ncastTypeCodes="SF,CF,RF,"
        """
        pass
