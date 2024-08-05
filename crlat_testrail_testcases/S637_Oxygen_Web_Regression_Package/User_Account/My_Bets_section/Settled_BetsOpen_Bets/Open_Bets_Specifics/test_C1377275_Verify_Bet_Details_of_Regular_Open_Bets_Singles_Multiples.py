import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1377275_Verify_Bet_Details_of_Regular_Open_Bets_Singles_Multiples(Common):
    """
    TR_ID: C1377275
    NAME: Verify Bet Details of Regular Open Bets (Singles & Multiples)
    DESCRIPTION: This test case verifies bet details of Regular Open bets
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-24438 OpenBets : Redesign main areas] [1]
    DESCRIPTION: [BMA-24473 CashOut/OpenBets: Watch Icon (link) to Live Stream] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24438
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-24473
    DESCRIPTION: AUTOTEST [C2011240]
    DESCRIPTION: AUTOTEST [C1952837]
    DESCRIPTION: AUTOTEST [C2011241]
    PRECONDITIONS: 1. User should be logged in to view their open bets.
    PRECONDITIONS: 2. User should have a few open bets
    PRECONDITIONS: 3. User should have "My Bets" page opened
    """
    keep_browser_open = True

    def test_001_navigate_to_the_open_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to the "Open Bets" tab on 'My Bets' page
        EXPECTED: * "Open Bets" tab on 'My Bets' page is opened
        EXPECTED: * User's open bets are shown
        """
        pass

    def test_002_verify_bet_details_of_a_single_open_bet_in_the_bet_overview_pre_match_event(self):
        """
        DESCRIPTION: Verify bet details of a **Single** Open bet in the bet overview **(Pre-match event)**
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: * Bet type
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name and event start date and time in HH:MM, DD MM format using 24-hour clock:
        EXPECTED: Today - HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: Tomorrow/Future - HH:MM, DD MMM (e.g. "14:00 or 05:00, 24 Nov or 02 Nov")
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00) on the left
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00) on the right
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_003_tap_on_the_event_name(self):
        """
        DESCRIPTION: Tap on the event name
        EXPECTED: User is redirected to event details page
        EXPECTED: Note: Event name is NOT hyperlinked if bet was placed on selections from Enhanced Multiples market
        """
        pass

    def test_004_verify_bet_details_of_a_single_open_bet_in_the_bet_overview_live_event(self):
        """
        DESCRIPTION: Verify bet details of a **Single** Open bet in the bet overview **(Live event)**
        EXPECTED: The following information is shown in the bet overview:
        EXPECTED: * Bet type (Single)
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name
        EXPECTED: * Event match clock/"Live" label or "Watch live" icon (if available),live scores
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: * "LIVE" label or "Watch live" icon (if available), live scores  are shown next to the event name and start time
        EXPECTED: * "green arrow"/"red arrow" icons (indicating winning/losing state) are shown for each selection on the left of each selection
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_005_verify_bet_details_of_an_open_live_multiple_bet(self):
        """
        DESCRIPTION: Verify bet details of an **OPEN LIVE** Multiple bet
        EXPECTED: * Bet details are the same as in step #4
        EXPECTED: * "LIVE" label or "Watch live" icon (if available),live scores are shown next to the event name and start time
        EXPECTED: * "green arrow"/"red arrow" icons (indicating winning/losing state) are shown for each selection on the left of each selection
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_006_verify_long_names_on_open_bet_card(self):
        """
        DESCRIPTION: Verify long names on Open bet card
        EXPECTED: * Long name of a selection is wrapped to the next line
        EXPECTED: * Long name of a market is wrapped to the next line
        EXPECTED: * Long name of an event is wrapped to the next line
        """
        pass

    def test_007_verify_bet_details_of_an_multiple_open_bet_in_the_bet_overview_pre_match_event(self):
        """
        DESCRIPTION: Verify bet details of an **Multiple** Open bet in the bet overview **(Pre-Match event)**
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type
        EXPECTED: * Selection name user has bet on
        EXPECTED: * Odds of selection displayed through @ symbol next to selection name (eg. Home@1/4)
        EXPECTED: * Market name user has bet on - e.g., "Match Result & Both Teams to Score"
        EXPECTED: * Event name and event start date and time - 24 hours format:
        EXPECTED: Today - HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: Tomorrow/Future - HH:MM, DD MMM (e.g. "14:00 or 05:00, 24 Nov or 02 Nov")
        EXPECTED: * The above described details are shown for each selection, included in the multiple, one under another (list view)
        EXPECTED: At the bottom of the multiple section the following details are shown:
        EXPECTED: * Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_008_verify_bet_details_of_a_multiple_open_bet_in_the_bet_overview_live_event(self):
        """
        DESCRIPTION: Verify bet details of a **Multiple** Open bet in the bet overview **(LIVE Event)**
        EXPECTED: * Bet details are the same as in step #3
        EXPECTED: * "LIVE" label or "Watch live" icon (if available),live scores are shown next to the event name and start time
        """
        pass

    def test_009_verify_bet_details_of_a_single_horse_racing_bet_each_way(self):
        """
        DESCRIPTION: Verify bet details of a **Single Horse Racing bet (each way)**
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single - Each Way")
        EXPECTED: * Selection name
        EXPECTED: * Market name user has bet on and Each Way terms - e.g., "Win or Each Way, 1/4 odds - places 1,2,3,4")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date when bet was placed
        EXPECTED: * Unit stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: * Total stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Est. returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: If estimated returns are not available, "N/A" is shown
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_010_verify_bet_details_of_a_single_horse_racing_bet_not_each_way(self):
        """
        DESCRIPTION: Verify bet details of a **Single Horse Racing bet (NOT each way)**
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single")
        EXPECTED: * Selection name
        EXPECTED: * Market name user has bet on - e.g., "Win or Each Way")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date when bet was placed
        EXPECTED: * Stake <currency symbol> <value> (e.g., £20.00)
        EXPECTED: * Est. returns <currency symbol> <value> (e.g., £40.00)
        EXPECTED: If estimated returns are not available, "N/A" is shown
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass

    def test_011_verify_bet_details_of_a_forecasttricast_bet(self):
        """
        DESCRIPTION: Verify bet details of a **Forecast/Tricast bet**
        EXPECTED: The following bet details are shown:
        EXPECTED: * Bet type (e.g., "Single to win - Tricast")
        EXPECTED: * Selection names (3 names for Tricast bet, 4 names for Forecast bets)
        EXPECTED: * Market name user has bet on - e.g., "Win or Each Way - Tricast")
        EXPECTED: * Event name and start time (e.g., "1:40 Greyville")
        EXPECTED: * Date when bet was placed
        EXPECTED: * Stake (e.g., £10.00) and Est. Returns ("N/A" if not available)
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass
