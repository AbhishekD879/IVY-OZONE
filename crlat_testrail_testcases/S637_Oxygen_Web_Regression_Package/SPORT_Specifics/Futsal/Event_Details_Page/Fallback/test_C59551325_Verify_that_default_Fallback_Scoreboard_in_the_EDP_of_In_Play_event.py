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
class Test_C59551325_Verify_that_default_Fallback_Scoreboard_in_the_EDP_of_In_Play_event(Common):
    """
    TR_ID: C59551325
    NAME: Verify that default Fallback Scoreboard in the EDP of In-Play event
    DESCRIPTION: Verify that Fallback scoreboard is displayed by default when the In Play Futsal event does not have Betradar component available.
    PRECONDITIONS: 1: Event should be In-Play.
    PRECONDITIONS: 2: Betradar component is not available
    PRECONDITIONS: 3: Fallback scoreboard should be enabled by default in CMS
    PRECONDITIONS: How to Configure CMS?
    PRECONDITIONS: CMS > System Configuration > Structure > Fallback Scoreboard
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

    def test_003_click_on_futsal_sport_from_a_z_menu(self):
        """
        DESCRIPTION: Click on Futsal sport from A-Z menu
        EXPECTED: 1: User should be able to view the Futsal Event Landing Page.
        EXPECTED: 2: For the In Play event scores should be displayed before the Odds against the Team names
        """
        pass

    def test_004_click_on_the_event_from_in_play_tab(self):
        """
        DESCRIPTION: Click on the Event from In Play tab
        EXPECTED: User should be able to view the Event Details page.
        """
        pass

    def test_005_validate_the_scoreboard_section(self):
        """
        DESCRIPTION: Validate the Scoreboard section
        EXPECTED: Fallback scoreboard should be displayed in a rectangular section above Market Collections
        """
        pass
