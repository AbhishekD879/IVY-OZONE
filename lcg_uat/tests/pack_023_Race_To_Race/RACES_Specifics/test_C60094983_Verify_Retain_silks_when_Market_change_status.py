import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094983_Verify_Retain_silks_when_Market_change_status(Common):
    """
    TR_ID: C60094983
    NAME: Verify Retain silks when Market change status.
    DESCRIPTION: This test case verifies Retain silks when change status.
    PRECONDITIONS: 1. HR event with Win or Each Way market exists (shouldn't be in-play).
    PRECONDITIONS: 2. Some of the other markets should be created for current event ( To Finish Second', 'To Finish Third', 'To Finish Fourth', 'Top 2 Finish', 'Top 3 Finish', 'Top 4 Finish', 'Top 2', 'Top 3', 'Top 4', 'To Finish 2nd', 'To Finish 3rd', 'Insurance 2 Places','Insurance 3 Places', 'Insurance 4 Places', 'Place Insurance 2', 'Place Insurance 3', 'Place Insurance 4'],)
    PRECONDITIONS: 3. Forecast and Tricast checkboxes are active on market level for Win or Each Way market for event from precondition 1
    PRECONDITIONS: 4. OB TI:
    PRECONDITIONS: - Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments#LadbrokesEnvironments-LadbrokesOB/IMSendpoints
    PRECONDITIONS: 5. User should have a Horse Racing event detail page open
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select Win/EW or Forecast/Tricast tab
    """
    keep_browser_open = True

    def test_001_open_racing__edp_and_select_win_or_ew_tab(self):
        """
        DESCRIPTION: Open racing  EDP and select 'Win or E/W' tab
        EXPECTED: 'Win or E/W' tab appears with available silks and prices.
        """
        pass

    def test_002_open_ti_and_open_event_from_preconditionsundisplay_win_or_ew_marketopen_application_and_go_to_racing__edp(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Undisplay 'Win or E/W' market.
        DESCRIPTION: Open application and go to racing  EDP.
        EXPECTED: 'Win or E/W', Forecast, Tricast tabs should be removed.
        EXPECTED: User redirected to 1) Win Only or if not available then 2) To finish or if not available then 3) Top Finish
        EXPECTED: If NONE of these tabs are available user should be redirected to any available tab.
        """
        pass

    def test_003_open_ti_and_open_event_from_preconditionsdisplay_win_or_ew_marketreturn_to_racing__edp_reload_the_page(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Display 'Win or E/W' market.
        DESCRIPTION: Return to racing  EDP (reload the page).
        EXPECTED: 'Win or E/W', Forecast, Tricast tabs appear.
        """
        pass

    def test_004_open_ti_and_open_event_from_preconditionssuspend_win_or_ew_marketreturn_to_racing__edp(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Suspend 'Win or E/W' market.
        DESCRIPTION: Return to racing  EDP.
        EXPECTED: The tab isn't removed.
        EXPECTED: Prices are suspended.
        """
        pass

    def test_005_open_ti_and_open_event_from_preconditionsunsuspend_win_or_ew_marketreturn_to_racing__edp(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Unsuspend 'Win or E/W' market.
        DESCRIPTION: Return to racing  EDP.
        EXPECTED: All prices became active.
        """
        pass

    def test_006_open_ti_and_open_event_from_preconditionssuspend_and_undisplay_all_marketsreturn_to_racing__edp(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Suspend and undisplay ALL markets.
        DESCRIPTION: Return to racing  EDP.
        EXPECTED: All tabs removed from race EDP.
        """
        pass

    def test_007_open_ti_and_open_event_from_preconditionsdisplay_all_marketreturn_to_racing__edp_reload_the_page(self):
        """
        DESCRIPTION: Open TI and open event from preconditions.
        DESCRIPTION: Display All market.
        DESCRIPTION: Return to racing  EDP (reload the page).
        EXPECTED: All tabs appeared.
        """
        pass

    def test_008_open_forecasttricast_and_repeat_2_6_steps(self):
        """
        DESCRIPTION: Open Forecast/Tricast and repeat 2-6 steps.
        EXPECTED: 
        """
        pass
