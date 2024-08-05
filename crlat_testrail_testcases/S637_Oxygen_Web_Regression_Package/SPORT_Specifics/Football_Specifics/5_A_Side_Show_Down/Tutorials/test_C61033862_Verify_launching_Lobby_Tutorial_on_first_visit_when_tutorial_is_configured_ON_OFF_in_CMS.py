import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C61033862_Verify_launching_Lobby_Tutorial_on_first_visit_when_tutorial_is_configured_ON_OFF_in_CMS(Common):
    """
    TR_ID: C61033862
    NAME: Verify launching Lobby Tutorial on first visit when tutorial is configured ON/OFF in CMS
    DESCRIPTION: Verifies launching Lobby Tutorial on first visit when tutorial is configured off in CMS and on second visit if it is toggled on
    PRECONDITIONS: Lobby tutorial should be configured off in CMS.
    """
    keep_browser_open = True

    def test_001_login_into_the_application_with_the_user_not_yet_visited_the_showdown_lobby(self):
        """
        DESCRIPTION: Login into the application with the user not yet visited the Showdown Lobby
        EXPECTED: User successfully logged in.
        """
        pass

    def test_002_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-a-side lobby
        EXPECTED: Lobby is loaded with Animation and user shouldn't get tutorial.
        """
        pass

    def test_003_navigate_to_cms_and_toggle_on_the_tutorial_toggle(self):
        """
        DESCRIPTION: Navigate to CMS and Toggle ON the Tutorial Toggle
        EXPECTED: Tutorial Toggle should be Toggled ON in CMS
        """
        pass

    def test_004_go_to_front_end_and_login_with_another_user_not_yet_visited_the_showdown_lobby(self):
        """
        DESCRIPTION: Go to front end and login with another user not yet visited the showdown lobby.
        EXPECTED: user successfully logged in
        """
        pass

    def test_005_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-a-side lobby
        EXPECTED: Lobby loaded with Animation and lobby tutorial should display with welcome overlay with tutorial video and get started button.
        EXPECTED: ![](index.php?/attachments/get/161019232)
        """
        pass

    def test_006_click_on_video_play_button_and_verify_its_ga_tracking_in_console(self):
        """
        DESCRIPTION: Click on video play button and verify it's GA tracking in console.
        EXPECTED: Video should be played if it is available. click action should be GA tracked.
        """
        pass

    def test_007_click_on_get_started_button_and_verify_its_ga_tracking(self):
        """
        DESCRIPTION: Click on Get started button and verify it's GA tracking.
        EXPECTED: Welcome to showdown lobby screen should display and the text( is driven by CMS), close button and Next button are avilable
        EXPECTED: click action should be GA tracked. ![](index.php?/attachments/get/140133871)
        """
        pass

    def test_008_click_on_next_button_on_welcome_to_showdown_lobby_screen_verify_its_ga_tracking(self):
        """
        DESCRIPTION: Click on Next button on Welcome to showdown lobby screen. verify its GA tracking
        EXPECTED: Action should be GA tracked. if there is any upcoming showdown cards available then display prize screen by focusing on first card in the list. prize areas highlighted along with close and next buttons.      ![](index.php?/attachments/get/161000204)
        """
        pass

    def test_009_repeat_steps_4_8_when_there_is_no_upcoming_cards_in_lobby(self):
        """
        DESCRIPTION: Repeat steps 4-8 when there is no upcoming cards in lobby.
        EXPECTED: shuts the tutorial experience automatically.
        """
        pass

    def test_010_click_next_button_in_prize_screen_and_verify_its_ga_tracking(self):
        """
        DESCRIPTION: Click Next button in Prize screen and verify its GA tracking.
        EXPECTED: Click Action should be GA tracked. Entry stake screen should display with Close, Next buttons and highlighting with entry stake.  ![](index.php?/attachments/get/161000211)
        """
        pass

    def test_011_click_next_button_on_entry_stake_screen_and_verify_its_ga_tracking(self):
        """
        DESCRIPTION: Click Next button on Entry stake screen and verify it's GA tracking.
        EXPECTED: Click action should be GA trackable. displays Finish screen along with Close, Next buttons and highlighting the first upcoming showdown card.  ![](index.php?/attachments/get/161000213)
        """
        pass

    def test_012_click_on_finish_button_and_verify_its_ga_tracking(self):
        """
        DESCRIPTION: Click on Finish button and verify it's GA tracking.
        EXPECTED: Tutorial experience should be closed and click action should GA trackable.
        """
        pass

    def test_013_navigate_to_any_other_sports_pages_and_come_back_lobby_page(self):
        """
        DESCRIPTION: Navigate to any other sports pages and come back lobby page.
        EXPECTED: User shouldn't get tutorial experience automatically on second visit.
        """
        pass

    def test_014_click_on_tutorial_button(self):
        """
        DESCRIPTION: Click on Tutorial button
        EXPECTED: Tutorial overlay should display
        """
        pass
