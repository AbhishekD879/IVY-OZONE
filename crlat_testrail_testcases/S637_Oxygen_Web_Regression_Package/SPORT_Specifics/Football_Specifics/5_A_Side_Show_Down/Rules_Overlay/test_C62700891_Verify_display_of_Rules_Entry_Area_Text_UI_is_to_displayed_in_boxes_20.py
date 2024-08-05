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
class Test_C62700891_Verify_display_of_Rules_Entry_Area_Text_UI_is_to_displayed_in_boxes_20(Common):
    """
    TR_ID: C62700891
    NAME: Verify display of Rules Entry Area/Text UI is to displayed in boxes (2.0)
    DESCRIPTION: Verify display of Rules Entry Area/Text UI is to displayed in boxes (2.0)
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2)  user should not placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: Rules Entry Area
    PRECONDITIONS: Create  Rules Entry Area in CMS Static blocks
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_add_contest(self):
        """
        DESCRIPTION: Add Contest
        EXPECTED: Fill all the Mand* fields and save the contest
        """
        pass

    def test_004_validate_the_display_of_static_blocks_and_create_rule_entry_text_in_static_blocks(self):
        """
        DESCRIPTION: Validate the display of Static blocks and create Rule entry text in static blocks
        EXPECTED: User should be able create and view Rules entry text
        """
        pass

    def test_005_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_006_validate_ui_for_rules_entry_areatext_ui_in_prelivepost_leaderboards(self):
        """
        DESCRIPTION: Validate UI for Rules Entry Area/Text UI in Pre/live/post leaderboards
        EXPECTED: Rules Entry Area/Text UI in Pre/live/post leaderboards should display in boxes
        """
        pass
