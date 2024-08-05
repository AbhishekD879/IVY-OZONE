import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C59918234_Verify_the_availability_of_My_Bets_Footer_and_Live_Stats_Tracking_pop_up_content(Common):
    """
    TR_ID: C59918234
    NAME: Verify the availability of My Bets Footer and Live Stats Tracking pop-up content
    DESCRIPTION: This test case verifies the availability of My Bets Footer and Live Stats Tracking pop-up content which is CMS configurable
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: Create a Football event in OpenBet (TI)
    PRECONDITIONS: Request Banach side to map data including Player Bets markets
    PRECONDITIONS: Check that Banach data is retrieved (‘events’ request to Banach should return event under test on Football EDP)
    PRECONDITIONS: Set up Opta Statistic to the created event according to instruction https://confluence.egalacoral.com/display/SDM/Common+match+runner
    PRECONDITIONS: Place at least 1 bet with few markets (from BYB tab) on created Football event
    PRECONDITIONS: In OpenBet (TI) start the event (Is OFF = yes)
    PRECONDITIONS: Load app and log in
    """
    keep_browser_open = True

    def test_001_go_to_my_betsopen_bets_tab(self):
        """
        DESCRIPTION: Go to My Bets/Open Bets tab
        EXPECTED: 'Open bets' tab is opened and Banach bet(s) details are displayed with Opta score
        EXPECTED: ![](index.php?/attachments/get/119425568)
        """
        pass

    def test_002_observe_my_bets_footer(self):
        """
        DESCRIPTION: Observe My Bets Footer
        EXPECTED: My Bets Footer contains of:
        EXPECTED: * Opta Logo svg icon upload
        EXPECTED: * Description text : Statistical totals are always subject to change.
        EXPECTED: * Clickable text: See More
        EXPECTED: ![](index.php?/attachments/get/119425582)
        """
        pass

    def test_003_tap_on_the_see_more_text(self):
        """
        DESCRIPTION: Tap on the 'See More' text
        EXPECTED: Live Stats Tracking pop-up appears with next content:
        EXPECTED: * Pop-up title : Live Stats Tracking
        EXPECTED: * Pop-up description: "Live Statistics are sourced from our data provider Opta and are to be used as a guide only. Statistical totals are always subject to change, and in some scenarios may be altered after the event has finished."
        EXPECTED: * Pop-up CTA : 'OK'
        EXPECTED: ![](index.php?/attachments/get/119597668)
        """
        pass

    def test_004_tap_on_the_ok_cta(self):
        """
        DESCRIPTION: Tap on the 'OK' CTA
        EXPECTED: Live Stats Tracking pop-up is closed, Open Bets tab remains opened
        """
        pass

    def test_005_navigate_to_event_details_page__my_bets_tab_event_from_precondition(self):
        """
        DESCRIPTION: Navigate to event details page > My Bets tab (event from precondition)
        EXPECTED: 'My Bets' tab is opened and Banach bet(s) details are displayed with Opta score
        EXPECTED: ![](index.php?/attachments/get/120239802)
        """
        pass

    def test_006_observe_my_bets_footer(self):
        """
        DESCRIPTION: Observe My Bets Footer
        EXPECTED: My Bets Footer contains of:
        EXPECTED: * Opta Logo svg icon upload
        EXPECTED: * Description text : Statistical totals are always subject to change.
        EXPECTED: * Clickable text: See More
        """
        pass

    def test_007_tap_on_the_see_more_text(self):
        """
        DESCRIPTION: Tap on the 'See More' text
        EXPECTED: Live Stats Tracking pop-up appears with next content:
        EXPECTED: * Pop-up title : Live Stats Tracking
        EXPECTED: * Pop-up description: "Live Statistics are sourced from our data provider Opta and are to be used as a guide only. Statistical totals are always subject to change, and in some scenarios may be altered after the event has finished."
        EXPECTED: * Pop-up CTA : 'OK'
        """
        pass

    def test_008_tap_on_the_ok_cta(self):
        """
        DESCRIPTION: Tap on the 'OK' CTA
        EXPECTED: Live Stats Tracking pop-up is closed, My Bets tab remains opened
        """
        pass

    def test_009_navigate_to_event_details_page__build_your_bet_tab_any_event_without_mapped_stats_tracking(self):
        """
        DESCRIPTION: Navigate to event details page > Build your bet tab (any event without mapped stats tracking)
        EXPECTED: 
        """
        pass

    def test_010_add_4_selections_to_the_betslip_from_below_build_your_bet_tab_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Add 4 selections to the Betslip from below Build your bet tab and tap 'Place Bet' button
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_011_go_to_my_betsopen_bets_tabobserve_my_bets_footer(self):
        """
        DESCRIPTION: Go to My Bets/Open Bets tab
        DESCRIPTION: Observe My Bets Footer
        EXPECTED: The short description text in the footer is not displayed
        """
        pass
