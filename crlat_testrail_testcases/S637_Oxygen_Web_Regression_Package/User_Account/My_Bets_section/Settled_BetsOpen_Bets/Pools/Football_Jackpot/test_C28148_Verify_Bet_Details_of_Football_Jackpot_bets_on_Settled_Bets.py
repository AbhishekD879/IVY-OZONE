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
class Test_C28148_Verify_Bet_Details_of_Football_Jackpot_bets_on_Settled_Bets(Common):
    """
    TR_ID: C28148
    NAME: Verify Bet Details of Football Jackpot bets on Settled Bets
    DESCRIPTION: This test case verifies 'Pools' sort filter and bet details for Football Jackpot bet lines within
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: * [BMA-3145] [1]
    DESCRIPTION: * [BMA-6231] [2]
    DESCRIPTION: * [BMA-9153] [3]
    DESCRIPTION: * [BMA-13748 Add Digital Sports Bet History in Oxygen platform] [4]
    DESCRIPTION: * [BMA-12422: Digital Sports - Change name Pick & Mix to Player Bets] [5]
    DESCRIPTION: * [BMA-15524: Removing Bet History Download Links from Bet History Pages] [6]
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [7]
    DESCRIPTION: * [BMA-27576 MyBets Improvement: Football Jackpot Redesign - Bet History] [8]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-3145
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-6231
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-9153
    DESCRIPTION: [4]: https://jira.egalacoral.com/browse/BMA-13748
    DESCRIPTION: [5]: https://jira.egalacoral.com/browse/BMA-12422
    DESCRIPTION: [6]: https://jira.egalacoral.com/browse/BMA-15524
    DESCRIPTION: [7]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [8]: https://jira.egalacoral.com/browse/BMA-27576
    PRECONDITIONS: 1. User should be logged in to view their bet history.
    PRECONDITIONS: 2. User should have few **Settled Bets: Open/Won/Lost/Void** Football Jackpot bets
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' page/tab is opened
        EXPECTED: * 'Regular' filter is selected by default
        EXPECTED: * Today's date is selected in both 'From' and 'To' date pickers
        """
        pass

    def test_002_select_pools_filter(self):
        """
        DESCRIPTION: Select 'Pools' filter
        EXPECTED: * 'Pools' filter is selected
        EXPECTED: * Today's date is still shown in both date pickers
        EXPECTED: * User's football jackpot bets are shown if user has settled FJ bets today
        EXPECTED: * If there is no FJ settled bets for today, "You have no settled bets" message is shown
        """
        pass

    def test_003_select_dates_when_user_has_settled_fj_bets_in_the_date_pickers(self):
        """
        DESCRIPTION: Select dates, when user has settled FJ bets, in the date pickers
        EXPECTED: * Dates are selected
        EXPECTED: * User's FJ bets are shown
        """
        pass

    def test_004_verify_ft_label_for_finished_events(self):
        """
        DESCRIPTION: Verify "FT" label for finished events
        EXPECTED: If the event is finished, there is "FT" label next to the event name instead of the event start time in the format:
        EXPECTED: **<Selection name>**
        EXPECTED: <Event name> FT
        EXPECTED: Example:
        EXPECTED: **Draw**
        EXPECTED: Barcelona v Levante FT
        """
        pass

    def test_005_verify_bet_details_of_a_lost_fj_bet(self):
        """
        DESCRIPTION: Verify bet details of a **Lost** FJ bet
        EXPECTED: * Bet details are shown in the same format as described in step #4
        EXPECTED: * There is a "LOST" label on the right side of the section header
        """
        pass

    def test_006_verify_bet_details_of_a_won_fj_bet(self):
        """
        DESCRIPTION: Verify bet details of a **Won** FJ bet
        EXPECTED: * Bet details are shown in the same format as described in step #4
        EXPECTED: * There is a "WON" label on the right side of the section header
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        """
        pass

    def test_007_verify_bet_details_of_a_void_fj_bet(self):
        """
        DESCRIPTION: Verify bet details of a **Void** FJ bet
        EXPECTED: * Bet details are shown in the same format as described in step #4
        EXPECTED: * There is a "VOID" label on the right side of the section header
        """
        pass

    def test_008_repeat_steps_2_9_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop_settled_bets_page_for_tabletdesktop___can_be_accessed_via_direct_link(self):
        """
        DESCRIPTION: Repeat steps 2-9 for:
        DESCRIPTION: * 'Settled Bets' tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        DESCRIPTION: * Settled Bets page (for Tablet/Desktop) - can be accessed via direct link
        EXPECTED: 
        """
        pass
