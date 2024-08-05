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
class Test_C59551074_Verify_Fallback_Betradar_Scores_Comparison(Common):
    """
    TR_ID: C59551074
    NAME: Verify Fallback & Betradar Scores Comparison
    DESCRIPTION: Verify that when the event is In Play fallback scores are displayed against the team names before the odds in Volleyball Landing page and both fallback & betradar scores are same
    PRECONDITIONS: 1: Volleyball Event should be In-Play.
    PRECONDITIONS: 2: Betradar component is not available
    PRECONDITIONS: 3: Fallback scoreboard should be enabled by default in CMS
    PRECONDITIONS: How to Configure CMS?
    PRECONDITIONS: CMS > System Configuration > Structure > Fallback Scoreboard
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes__coral_urlfor_mobile_app_validation_open_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral URL.
        DESCRIPTION: (For mobile app validation Open the App)
        EXPECTED: URL should be launched.
        """
        pass

    def test_002_click_on_login_and_enter_the_user_credentials_and_click_on_the_login_button(self):
        """
        DESCRIPTION: Click on Login and enter the User credentials and click on the Login button.
        EXPECTED: User should be successfully logged in.
        """
        pass

    def test_003_click_on_volleyball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Volleyball sport from A-Z menu
        EXPECTED: User should be able to view the Volleyball Event Landing Page.
        """
        pass

    def test_004_click_on_the_event_betradar_scoreboard_not_available_to_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event (Betradar scoreboard NOT available to the event) from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_fallback_scores(self):
        """
        DESCRIPTION: Validate Fallback scores
        EXPECTED: Fallback scores should be displayed against the team names before the odds in Volleyball Landing page.
        """
        pass

    def test_006_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Event details page
        EXPECTED: User should be able to view the Event Details page.
        EXPECTED: Betradar scores should be same
        """
        pass

    def test_007_open_application_in_two_tabs___one_tab_for_fallback_scoreboard_inplay_event_landing_page_other_is_for_betradar_scoreboard_edp_and_compare_results(self):
        """
        DESCRIPTION: Open application in two tabs - one tab for fallback scoreboard inplay event landing page other is for betradar scoreboard EDP and compare results
        EXPECTED: Fallback scores & Betradar scores should be same
        """
        pass
