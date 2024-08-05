import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C53625934_Ladbrokes_Verify_event_time_presence_within_event_name_of_the_Virtual_event_for_bet_placement_and_history(Common):
    """
    TR_ID: C53625934
    NAME: [Ladbrokes] Verify event time presence within event name of the Virtual event for bet placement and history
    DESCRIPTION: Test case verifies event start time presence within event name of Greyhound and Horse Racing virtual events on all bet placement related places(pages), such as QuickBet, Betslip, Bet Receipt and Bet History/Open Bets.
    PRECONDITIONS: Upcoming virtual Greyhounds and Horse Racing events should be configured
    PRECONDITIONS: User should be logged in and have positive balance without any restrictions on betting
    PRECONDITIONS: 'Virtual' page (/virtual-sports) should be opened
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_switch_to_a_tab_of_the_upcoming_horse_racing_events_with_activenot_suspended_selections(self):
        """
        DESCRIPTION: Switch to a tab of the upcoming Horse Racing events with active(not suspended) selections
        EXPECTED: Event Name(Title) is shown above the video player
        EXPECTED: ![](index.php?/attachments/get/88860162)
        EXPECTED: Tab is selected with a red underlining shown below the event start time
        EXPECTED: ![](index.php?/attachments/get/88860163)
        EXPECTED: Event start time is shown in the following format: HH:MM
        """
        pass

    def test_002_add_1_selection_from_the_opened_tab_into_the_quick_bet(self):
        """
        DESCRIPTION: Add 1 selection from the opened tab into the Quick Bet
        EXPECTED: Quick Bet modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: ![](index.php?/attachments/get/88860165)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860166)
        """
        pass

    def test_003_place_a_bet_on_the_added_selection(self):
        """
        DESCRIPTION: Place a bet on the added selection
        EXPECTED: Bet Receipt modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name next to the market name (on its right side)
        EXPECTED: ![](index.php?/attachments/get/88860168)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860167)
        """
        pass

    def test_004_close_the_bet_receipt_and_switch_to_a_tab_of_the_upcoming_greyhounds_events_with_activenot_suspended_selections(self):
        """
        DESCRIPTION: Close the Bet Receipt and switch to a tab of the upcoming Greyhounds events with active(not suspended) selections
        EXPECTED: Event Name(Title) is shown above the video player
        EXPECTED: ![](index.php?/attachments/get/88860169)
        EXPECTED: Tab is selected with a red underlining shown below the event start time
        EXPECTED: ![](index.php?/attachments/get/88860170)
        EXPECTED: Event start time is shown in the following format: HH:MM
        """
        pass

    def test_005_add_1_selection_from_the_opened_tab_into_the_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add 1 selection from the opened tab into the the Betslip and Open Betslip
        EXPECTED: Betslip modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: ![](index.php?/attachments/get/88860171)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860173)
        """
        pass

    def test_006_place_a_bet_on_the_added_selection(self):
        """
        DESCRIPTION: Place a bet on the added selection
        EXPECTED: Bet Receipt modal is shown
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name next to the market name (on its right side)
        EXPECTED: ![](index.php?/attachments/get/88860172)
        EXPECTED: Start time within the event name matches the start time that was shown in the selected tab
        EXPECTED: ![](index.php?/attachments/get/88860174)
        """
        pass

    def test_007_close_the_bet_receipt_and_navigate_to_open_bets_page_open_bets(self):
        """
        DESCRIPTION: Close the Bet Receipt and navigate to Open Bets page (/open-bets)
        EXPECTED: Open Bets page is opened
        EXPECTED: Bets from both Quick Bet and Betslip bet placements are shown one under another
        EXPECTED: ![](index.php?/attachments/get/88860178)
        """
        pass

    def test_008_verify_start_time_presence_within_event_names_of_placed_bets(self):
        """
        DESCRIPTION: Verify start time presence within event names of placed Bets
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name
        EXPECTED: (!) **Start time in the event name may differ from the 'factual start time', shown next to the event name (on its right side) in 'HH:MM, Today' format** - this is due to a fact that factual start time doesn't account time zone differences
        """
        pass

    def test_009_wait_for_both_eventsfrom_steps_2_and_5_to_settle_and_switch_to_settled_bets_page_bet_history(self):
        """
        DESCRIPTION: Wait for both events(from steps 2 and 5) to settle and switch to Settled Bets page (/bet-history)
        EXPECTED: Settled Bets page is opened
        EXPECTED: Bets from step 8 are shown one under another
        EXPECTED: ![](index.php?/attachments/get/88860179)
        """
        pass

    def test_010_verify_start_time_presence_within_event_names_of_settled_bets(self):
        """
        DESCRIPTION: Verify start time presence within event names of settled Bets
        EXPECTED: Start time in 'HH:MM' format is shown on the start of the event name below the market name for each cell that represents the previously placed(settled) bet.
        """
        pass
