import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C44870167_Verify_In_play_and_Featured_modules_on_Highlights_tab(Common):
    """
    TR_ID: C44870167
    NAME: Verify In-play and Featured modules on Highlights tab
    DESCRIPTION: "Verify below functions in the featured page,
    DESCRIPTION: - InPlay module with list of Inplay(Sports/Racing) and sublisted with events.
    DESCRIPTION: - Price updates by live push
    DESCRIPTION: - Check SEE ALL  and chevron on in the tap to  navigate to correct page
    DESCRIPTION: - Verify when there is no Inplay sport, Inplay module should not be displayed
    DESCRIPTION: - Check events arranged into competition types and each type is collapsable
    DESCRIPTION: - Check highlight carousel in the featured tab (check the event navigations,bet placement)
    DESCRIPTION: "
    PRECONDITIONS: Configure Featured tab module in CMS
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default
        EXPECTED: For Logged in User : If user has any Private Markets, 'Your Enhanced Markets' tab will be opened by default.
        """
        pass

    def test_002_verify_in_play_module(self):
        """
        DESCRIPTION: Verify In-Play module
        EXPECTED: User should see the In-Play events grouped on sport type.  If there are No In-Play events, user should not see the In-Play module.
        """
        pass

    def test_003_verify_the_price_updates_for_in_play_events(self):
        """
        DESCRIPTION: Verify the price updates for In-Play events
        EXPECTED: User should see the price updates with live push for all the listed In-Play events
        """
        pass

    def test_004_click_on_see_all_next_to_the_in_play_eventsnote_this_step_is_applicable_for_mobile_onlyna_for_desktop(self):
        """
        DESCRIPTION: Click on 'SEE ALL' next to the In-Play events
        DESCRIPTION: Note: This step is applicable for mobile only
        DESCRIPTION: N/A for Desktop
        EXPECTED: User should navigate to the In-Play page which lists all In-Play events for different sports.
        """
        pass

    def test_005_click_back_on_in_play_pagenote_this_step_is_applicable_for_mobile_onlyna_for_desktop(self):
        """
        DESCRIPTION: Click 'Back' on In-Play page
        DESCRIPTION: Note: This step is applicable for mobile only
        DESCRIPTION: N/A for Desktop
        EXPECTED: User should navigate back to the Home page.
        """
        pass

    def test_006_click_on_any_chevron_of_a_given_event(self):
        """
        DESCRIPTION: Click on any chevron of a given event
        EXPECTED: User should navigate to the corresponding event Landing page
        """
        pass

    def test_007_click_back(self):
        """
        DESCRIPTION: Click 'Back'
        EXPECTED: User should navigate back to the Home page.
        """
        pass

    def test_008_verify_recently_played_games_carousalnote_for_mobile_only(self):
        """
        DESCRIPTION: verify Recently played Games carousal
        DESCRIPTION: Note: For mobile only
        EXPECTED: Recently Played Games carousal is displayed only for Logged in Users, if the user has played any games in the past
        """
        pass

    def test_009_repeat_steps_1_7_for_a_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 1-7 for a logged out user
        EXPECTED: 
        """
        pass
