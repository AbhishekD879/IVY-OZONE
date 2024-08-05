import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C65865538_Verify_surface_bet_is_displayed_for_different_event_hubs(Common):
    """
    TR_ID: C65865538
    NAME: Verify surface bet is displayed for different event hubs
    DESCRIPTION: 
    PRECONDITIONS: Create a event in OB
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
    PRECONDITIONS: 3.Click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title as 'Featured - Ladies Matches '
    PRECONDITIONS: EventIds (Create with EventId)
    PRECONDITIONS: Show on Sports select 'All Sports'
    PRECONDITIONS: Show on EventHub select multiple eventhubs:US Sports,Football,5 A Side
    PRECONDITIONS: Content Header
    PRECONDITIONS: Content
    PRECONDITIONS: Was Price
    PRECONDITIONS: Selection ID
    PRECONDITIONS: Display From
    PRECONDITIONS: Display To
    PRECONDITIONS: SVG Icon
    PRECONDITIONS: SVG Background
    PRECONDITIONS: 6.Check segment as 'Universal' or 'Segment'
    PRECONDITIONS: 7.Click Save Changes
    PRECONDITIONS: Check the Sort Order of Surface bet Module
    PRECONDITIONS: Navigate to Home Page-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
    """
    keep_browser_open = True

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        pass

    def test_002_observe_the_surface_bet_created_on_eventhub(self):
        """
        DESCRIPTION: Observe the surface bet created on eventhub
        EXPECTED: Surface bet created in CMS should be reflected on eventhub
        """
        pass

    def test_003_validate_the_order_of_surface_bet_created_on_eventhub(self):
        """
        DESCRIPTION: Validate the Order of surface bet created on eventhub
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        pass

    def test_004_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        pass

    def test_005_validate_the_surface_bet_title_content_header_content_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the surface bet Title, 'Content header', 'Content', SVG icon and SVG background
        EXPECTED: Title, 'Content header', 'Content', SVG icon and SVG background
        EXPECTED: should be displayed as per CMS config
        """
        pass

    def test_006_validate_the_surface_bet_is_displayed_in_the_event_hubs_for_example_us_sportsfootball5_a_side(self):
        """
        DESCRIPTION: Validate the surface bet is displayed in the event hubs: for example: US sports,Football,5 A Side
        EXPECTED: Surface bet created should reflect in the 'eventhub' selected as per CMS config
        """
        pass

    def test_007_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_eventhubs(self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in eventhubs
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        pass

    def test_008_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        pass

    def test_009_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        pass

    def test_010_activatedeactivate_the_whole_surface_bet_module_on_eventhub(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on eventhub
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """
        pass

    def test_011_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        pass

    def test_012_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        pass
