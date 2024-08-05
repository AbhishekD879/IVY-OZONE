import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C58996616_Verify_Surface_Bet_module_not_displaying_on_5_A_side_and_Build_Your_Bet_Bet_Builder_tabs_on_EDP(Common):
    """
    TR_ID: C58996616
    NAME: Verify Surface Bet module not displaying on 5-A-side and Build Your Bet/Bet Builder tabs on EDP
    DESCRIPTION: Test case verifies that Surface Bets aren't shown on Build Your Bet (Coral)/Bet Builder (Ladbrokes) and 5-A-Side tabs
    PRECONDITIONS: There is a single Surface Bet added to Event Detail page (EDP).
    PRECONDITIONS: Valid Selection Id is set.
    PRECONDITIONS: Event has configured 5-A-Side and BYB markets.
    PRECONDITIONS: 5-A-Side config:
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application.
        EXPECTED: Application is loaded.
        """
        pass

    def test_002_navigate_to_football_event_details_page_that_has_all_5_a_side_and_byb_configs(self):
        """
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side and BYB configs.
        EXPECTED: Configured in CMS Surface Bet is displayed.
        """
        pass

    def test_003_tap_on_5_a_side_tab(self):
        """
        DESCRIPTION: Tap on 5-A-Side tab.
        EXPECTED: Surface bet is not displayed.
        """
        pass

    def test_004_tap_on_build_your_bet_coralbet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Tap on Build Your Bet (Coral)/Bet Builder (Ladbrokes) tab.
        EXPECTED: Surface bet is not displayed.
        """
        pass
