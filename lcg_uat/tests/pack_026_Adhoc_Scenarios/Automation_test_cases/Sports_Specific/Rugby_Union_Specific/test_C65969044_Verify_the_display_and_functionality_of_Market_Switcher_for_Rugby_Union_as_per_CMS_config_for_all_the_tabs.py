import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65969044_Verify_the_display_and_functionality_of_Market_Switcher_for_Rugby_Union_as_per_CMS_config_for_all_the_tabs(Common):
    """
    TR_ID: C65969044
    NAME: Verify the display and functionality of Market Switcher for Rugby Union as per CMS config  for all the  tabs
    DESCRIPTION: The test case verifies the functionality of the Market Switcher as per CMS configuration for all the tabs for the Rugby Union sport.
    PRECONDITIONS: In CMS --&gt; Sport Pages--&gt;Sport Category--&gt; General Sport Configuration--&gt; Primary and Top markets and Save Changes with required fields.
    PRECONDITIONS: In CMS --&gt; System Configuration -&gt; Structure -&gt; Enable the Market Switcher for Rugby Union.
    PRECONDITIONS: Add Markets in Matches tab and Competitions with the Market name and Display name and Save changes.
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be loaded successfully.
        """
        pass

    def test_002_navigate_to_rugby_union_sport_by_selecting_it_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Navigate to Rugby Union sport by selecting it from the sports ribbon.
        EXPECTED: The Rugby Union sports landing page should be successfully loaded.
        """
        pass

    def test_003_verify_the_functionality_of_the_market_switcher_in_the_matches_tab(self):
        """
        DESCRIPTION: Verify the functionality of the Market switcher in the Matches tab.
        EXPECTED: 1. The Market switcher should be available in the Matches tab.
        EXPECTED: 2. The list of markets added in the CMS should be displayed in the drop down list of the market switcher if the events are available for the respective markets.
        EXPECTED: 3. The order of display of options in the drop down list should be in the order in CMS.
        EXPECTED: 4. When the order of the markets are changed in the CMS - Markets table it should be updated in the same order in the FE.
        """
        pass

    def test_004_verify_the_market_switcher_in_the_competitions_tab(self):
        """
        DESCRIPTION: Verify the Market Switcher in the Competitions tab
        EXPECTED: 1. The Market switcher should be available in the Competitions tab.
        EXPECTED: 2. The list of markets added in the CMS should be displayed in the drop down list of the market switcher if the events are available for the respective markets.
        EXPECTED: 3. The order of display of options in the drop down list should be in the order in CMS.
        EXPECTED: 4. When the order of the markets are changed in the CMS - Markets table it should be updated in the same order in the FE.
        """
        pass

    def test_005_click_on__add_selection_in_any_of_the_market_from_market_switcher_and_place_a_bet_in_matches_and_competition_tab_events(self):
        """
        DESCRIPTION: Click on  add selection in any of the Market from Market Switcher and place a bet in Matches and Competition tab events.
        EXPECTED: Bets should be placed successfully on selections added from the Matches and Competitions tab events.
        """
        pass
