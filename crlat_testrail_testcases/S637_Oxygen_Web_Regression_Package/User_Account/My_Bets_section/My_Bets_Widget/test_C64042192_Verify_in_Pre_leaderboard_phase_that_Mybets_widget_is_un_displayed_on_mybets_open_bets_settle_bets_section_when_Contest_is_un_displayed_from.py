import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C64042192_Verify_in_Pre_leaderboard_phase_that_Mybets_widget_is_un_displayed_on_mybets_open_bets_settle_bets_section_when_Contest_is_un_displayed_from_CMS(Common):
    """
    TR_ID: C64042192
    NAME: Verify in Pre-leaderboard phase that Mybets widget is un displayed on mybets (open bets & settle bets) section, when Contest is un displayed from CMS
    DESCRIPTION: Verify in Pre-leaderboard phase that Mybets widget is un displayed on mybets (open bets & settle bets) section, when Contest is un displayed from CMS
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User should disable mybets toggle on in system-configuration/structure
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    PRECONDITIONS: Un displaying contest
    PRECONDITIONS: 1: User should able un display the created contest from CMS in contest detail view
    """
    keep_browser_open = True

    def test_001_login_as_cms_admin(self):
        """
        DESCRIPTION: Login as CMS admin
        EXPECTED: User should successful login to CMS
        """
        pass

    def test_002_navigate_to_system_configuration_and_enable_mybets_widget(self):
        """
        DESCRIPTION: Navigate to system configuration and enable mybets widget
        EXPECTED: user should able to navigate and enable mybets section
        """
        pass

    def test_003_navigate_5a_side_showdown_section_and_click_the_contest_id(self):
        """
        DESCRIPTION: Navigate 5a side showdown section and click the contest id
        EXPECTED: User should able to navigate contest detail view
        """
        pass

    def test_004_un_display_the_contest_in_detail_page(self):
        """
        DESCRIPTION: Un display the contest in detail page
        EXPECTED: User should able to un display the context
        """
        pass

    def test_005_load_the_app_or_url(self):
        """
        DESCRIPTION: Load the app or URL
        EXPECTED: "User should be able to launch the URL
        EXPECTED: Mobile App: User should able to launch the app"
        """
        pass

    def test_006_navigate_to_football_section_and_place_5a_side_bets(self):
        """
        DESCRIPTION: Navigate to football section and place 5a side bets
        EXPECTED: User should able to place 5a side bets
        """
        pass

    def test_007_navigate_to_open_bets_section_or_settle_bets_if_event_is_settled_and_verify_the_my_betsleaderboard_widget_is_undisplayed_for_undisplayed_contest_bets_in_pre_leaderboard_phase(self):
        """
        DESCRIPTION: Navigate to open bets section or settle bets (if event is settled) and verify the my bets
        DESCRIPTION: leaderboard widget is undisplayed for undisplayed contest bets in pre-leaderboard phase.
        EXPECTED: Mybets widget is un displayed in open bets section or  settle bets (if event is settled)
        EXPECTED: for un displayed contest bets in pre-leaderboard phase
        """
        pass

    def test_008_in_cms_enable_the_display_check_box_for_contest_which_is_undisplayed_inpre__leaderboard_phase_for_mybets_widget_in_open_bets_section(self):
        """
        DESCRIPTION: In CMS, enable the display check box for contest which is undisplayed in
        DESCRIPTION: pre- leaderboard phase for Mybets widget in open bets section
        EXPECTED: Mybets widget should be display in open bets for Contest
        """
        pass
