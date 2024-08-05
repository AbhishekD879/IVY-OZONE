import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C49050595_Build_Your_Bet_Bet_Builder_tab_availability_based_on_CMS_configs(Common):
    """
    TR_ID: C49050595
    NAME: 'Build Your Bet/Bet Builder' tab availability based on CMS configs
    DESCRIPTION: This test case verifies 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab availability based on CMS configs (feature toggle and league being enabled for BYB)
    PRECONDITIONS: **Build Your Bet/Bet Builder config:**
    PRECONDITIONS: 1. Feature is enabled in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> enable tab
    PRECONDITIONS: 2. Banach leagues are added and enabled in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for BYB’ is ticked
    PRECONDITIONS: 3. Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: 4. Event is prematch (not live)
    PRECONDITIONS: Load the app
    PRECONDITIONS: Navigate to Football event details page that has all BYB configs
    """
    keep_browser_open = True

    def test_001_verify_build_your_bet_coral__bet_builder_ladbrokes_tab_availability(self):
        """
        DESCRIPTION: Verify 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab availability
        EXPECTED: 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is displayed on event details page
        """
        pass

    def test_002_disable_byb_in_cms__system_configuration___structure___yourcalliconsandtabs___disable_tab_and_save_changes(self):
        """
        DESCRIPTION: Disable BYB in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> disable tab and save changes
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_003_refresh_event_details_page_on_frontend_and_verify_build_your_betbet_builder_tab_availability(self):
        """
        DESCRIPTION: Refresh event details page on frontend and verify 'Build Your Bet/Bet Builder' tab availability
        EXPECTED: 'Build Your Bet/Bet Builder' tab is NOT displayed on event details page
        """
        pass

    def test_004__enable_byb_in_cms__system_configuration___structure___yourcalliconsandtabs___enable_tab_and_save_changes_untick_active_for_byb_in_cms___byb___banach_leagues___select_league_under_test(self):
        """
        DESCRIPTION: * Enable BYB in CMS > System Configuration -> Structure -> YourCallIconsAndTabs -> enable tab and save changes
        DESCRIPTION: * Untick 'Active for BYB' in CMS -> BYB -> Banach Leagues -> select league under test
        EXPECTED: Changes are successfully saved
        """
        pass

    def test_005_refresh_event_details_page_on_frontend_and_verify_build_your_betbet_builder_tab_availability(self):
        """
        DESCRIPTION: Refresh event details page on frontend and verify 'Build Your Bet/Bet Builder' tab availability
        EXPECTED: 'Build Your Bet/Bet Builder' tab is NOT displayed on event details page
        """
        pass
