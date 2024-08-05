import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C64378803_Verify_in_Post_Leaderboard_phase_the_Mybets_widget_is_undisplayed_on_mybets_open_bets_settle_bets_section_when_Contest_is_undisplayed_from_CMS(Common):
    """
    TR_ID: C64378803
    NAME: Verify in Post-Leaderboard phase the Mybets widget is undisplayed on mybets (open bets & settle bets) section, when Contest is undisplayed from CMS
    DESCRIPTION: Verify in Post-Leaderboard phase the Mybets widget is undisplayed on mybets (open bets & settle bets) section, when Contest is undisplayed from CMS
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create a contests for an events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: Important: While creating contest give multiple prize combinations including Cash, freebet, ticket, voucher.
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
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
        EXPECTED: User should able to navigate context detail view
        """
        pass

    def test_004_undisplay_the_contest_in_detail_page_from_cms(self):
        """
        DESCRIPTION: Undisplay the contest in detail page from CMS
        EXPECTED: User should able to Undisplay the context
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

    def test_007_navigate_to_open_bets_section_or_settle_bets_if_event_is_settled_and_verify_the_my_betsleaderboard_widget_is_undisplayed_for_undisplayed_contest_bets_in_post_leaderboard_phase(self):
        """
        DESCRIPTION: Navigate to open bets section or settle bets (if event is settled) and verify the my bets
        DESCRIPTION: leaderboard widget is undisplayed for undisplayed contest bets in Post-leaderboard phase.
        EXPECTED: Mybets widget is un displayed in open bets section or  settle bets (if event is settled)
        EXPECTED: for un displayed contest bets in Post-leaderboard phase
        """
        pass

    def test_008_in_cms_enable_the_display_check_box_for_contest_which_is_undisplayed_in_post__leaderboard_phase_for_mybets_widget_in_settle_bets_section(self):
        """
        DESCRIPTION: In CMS, enable the display check box for contest which is undisplayed in Post- leaderboard phase for Mybets widget in settle bets section
        EXPECTED: Mybets widget should be display in settle bets for Contest
        """
        pass
