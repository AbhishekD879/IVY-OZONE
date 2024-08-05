import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C874388_Navigation_Football_Jackpot(Common):
    """
    TR_ID: C874388
    NAME: Navigation Football Jackpot
    DESCRIPTION: This test case verifies content of Football 'Jackpot' page
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To view all events being used within the Football Jackpot please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/YYY?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYY - comma separated list of 15 market id's of Football Jackpot pool
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Make sure there is at least one active pool available to be displayed on front-end
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: *   Football Landing Page is opened
        EXPECTED: *   'Today' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_004_verify_page_header(self):
        """
        DESCRIPTION: Verify page header
        EXPECTED: Page header contain the following message:
        EXPECTED: "You're just <number of active events from 15 available> selections away from the jackpot!"
        """
        pass

    def test_005_verify_how_to_play_section(self):
        """
        DESCRIPTION: Verify 'How to Play?' section
        EXPECTED: There is an 'i' icon with label 'How to Play?'
        """
        pass

    def test_006_tap_the_how_to_play_text(self):
        """
        DESCRIPTION: Tap the 'How to Play?' text
        EXPECTED: * ‘Football Jackpot Betting Rules’ appear as a full screen overlay
        EXPECTED: * There is 'X' ('close') button in the top left corner
        EXPECTED: * There is a green 'OK' button at the bottom of the overlay
        EXPECTED: * 'OK' button is in the sticky footer
        """
        pass

    def test_007_check_the_corresponding_static_block_in_cms(self):
        """
        DESCRIPTION: Check the corresponding static block in CMS
        EXPECTED: * The data in the static block is exactly the same as on the overlay
        EXPECTED: * Data for the overlay is always pulled from the CMS static block
        """
        pass

    def test_008_tap_the_x_button_in_the_top_left_corner_of_the_overlay(self):
        """
        DESCRIPTION: Tap the 'X' button in the top left corner of the overlay
        EXPECTED: * The overlay is closed
        EXPECTED: * User is redirected to the main Football Jackpot page
        """
        pass

    def test_009_tap_the_how_to_play_text(self):
        """
        DESCRIPTION: Tap the 'How to Play?' text
        EXPECTED: ‘Football Jackpot Betting Rules’ appear as a full screen overlay
        """
        pass

    def test_010_tap_ok_button(self):
        """
        DESCRIPTION: Tap 'OK' button
        EXPECTED: * The overlay is closed
        EXPECTED: * User is redirected to the main Football Jackpot page
        EXPECTED: **Note for tablet:
        EXPECTED: - There is no sticky footer on tablet
        EXPECTED: - 'OK' button is located at the bottom of the page and user is able to scroll the page down to this button
        """
        pass

    def test_011_verify_luck_dip_option(self):
        """
        DESCRIPTION: Verify 'Luck Dip' option
        EXPECTED: 'Lucky Dip' button is present and shown correctly
        """
        pass

    def test_012_verify_the_main_body_of_the_page_ie_football_jackpot_coupon(self):
        """
        DESCRIPTION: Verify the main body of the page (i.e. Football Jackpot coupon)
        EXPECTED: The main body of the page contains 15 events
        """
        pass

    def test_013_verify_bet_placement_section(self):
        """
        DESCRIPTION: Verify Bet Placement section
        EXPECTED: This section includes the following elements below the main section:
        EXPECTED: *   'Stake Per Line:' label and dropdown
        EXPECTED: *   'Total Lines:' label and field
        EXPECTED: *   'Total Stake:' label and field
        EXPECTED: *   'Clear All Selections' button
        EXPECTED: *   'Bet Now' button
        """
        pass
