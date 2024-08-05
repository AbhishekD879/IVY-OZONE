import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C69616_Tracking_of_Bet_Receipt_page_views(Common):
    """
    TR_ID: C69616
    NAME: Tracking of Bet Receipt page views
    DESCRIPTION: This test case verifies tracking of Bet Receipt page views
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Test case should be run on Mobile, Tablet and Desktop devices
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_in_new_browser_tab(self):
        """
        DESCRIPTION: Load Oxygen app in new browser tab
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_or_race_selection_and_open_betslip_singles_section(self):
        """
        DESCRIPTION: Add <Sport> or <Race> selection and open Betslip, **'Singles' section'**
        EXPECTED: 
        """
        pass

    def test_003_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Enter stake and place a bet
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/betslip-receipt'
        EXPECTED: });
        """
        pass

    def test_005_clicktap_done_button(self):
        """
        DESCRIPTION: Click/tap 'Done' button
        EXPECTED: Bet Receipt is closed
        """
        pass

    def test_006_open_new_browser_tab(self):
        """
        DESCRIPTION: Open new browser tab
        EXPECTED: 
        """
        pass

    def test_007_add_a_few_selections_and_open_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and open Betslip, **'Multiples' section**
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_6_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-6 for Multiple bet
        EXPECTED: 
        """
        pass

    def test_009_add_a_few_selections_from_the_same_race_event_and_open_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and open Betslip, **'Forecasts/Tricasts' section**
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__3_6_for_forecaststricasts_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-6 for Forecasts/Tricasts bet
        EXPECTED: 
        """
        pass

    def test_011_add_sport_or_race_selection_from_inspired_virtual_sports_and_open_betslip(self):
        """
        DESCRIPTION: Add <Sport> or <Race> selection from **Inspired Virtual Sports** and open Betslip
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_3_6_for_inspired_virtual_sports_bet(self):
        """
        DESCRIPTION: Repeat steps #3-6 for Inspired Virtual Sports bet
        EXPECTED: 
        """
        pass
