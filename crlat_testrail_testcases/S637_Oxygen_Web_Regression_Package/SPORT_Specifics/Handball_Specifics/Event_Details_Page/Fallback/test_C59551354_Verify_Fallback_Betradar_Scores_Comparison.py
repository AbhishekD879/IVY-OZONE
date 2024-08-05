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
class Test_C59551354_Verify_Fallback_Betradar_Scores_Comparison(Common):
    """
    TR_ID: C59551354
    NAME: Verify Fallback & Betradar Scores Comparison
    DESCRIPTION: Verify that when the event is In Play fallback scores are displayed against the team names before the odds in Handball Landing page and both fallback & betradar scores are same
    PRECONDITIONS: 1: Handball Event should be In-Play.
    PRECONDITIONS: 2: Only Betradar scoreboard to be available for the event.
    PRECONDITIONS: 3: Betradar scoreboard configuration in CMS is enabled.
    PRECONDITIONS: How to configure ?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_urlfor_mobile_app_validation_open_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes URL.
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

    def test_003_navigate_to_handball_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Navigate to Handball sport from A-Z menu.
        EXPECTED: User should be able to view the Handball Landing page.
        """
        pass

    def test_004_validate_fallback_scores(self):
        """
        DESCRIPTION: Validate Fallback scores
        EXPECTED: Fallback scores should be displayed against the team names before the odds in Handball Landing page.
        """
        pass

    def test_005_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Event details page
        EXPECTED: User should be able to view the Event Details page.
        EXPECTED: Fallback scores & Betradar scores should be same
        """
        pass

    def test_006_compare_fallback__betradar_scores(self):
        """
        DESCRIPTION: Compare Fallback & Betradar scores
        EXPECTED: Fallback scores & Betradar scores should be same
        """
        pass
