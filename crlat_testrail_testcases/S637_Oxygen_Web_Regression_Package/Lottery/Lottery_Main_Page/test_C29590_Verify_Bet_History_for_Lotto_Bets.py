import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@vtest
class Test_C29590_Verify_Bet_History_for_Lotto_Bets(Common):
    """
    TR_ID: C29590
    NAME: Verify Bet History for Lotto Bets
    DESCRIPTION: This test tase verifies data of Bet History for resulted bets on Lotteries
    DESCRIPTION: **Jira Ticket: **
    DESCRIPTION: BMA-8508 'Lottery - Bet History CR'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   to result Lotto bets contact UAT-team
    PRECONDITIONS: *   for now Won/Lost/Cancelled/Pending result are available
    PRECONDITIONS: *   to check data of resulted bets use 'accountHistory' Response
    """
    keep_browser_open = True

    def test_001_tap_on_lotto_icon_from_sportsmenu_ribbonor_a_z_page(self):
        """
        DESCRIPTION: Tap on 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_002_place_lotto_bet_successfully(self):
        """
        DESCRIPTION: Place Lotto bet successfully
        EXPECTED: 
        """
        pass

    def test_003_ask_uat_tean_to_trigger_result_for_appropriate_lotto_bet_ids(self):
        """
        DESCRIPTION: Ask UAT tean to trigger result for appropriate Lotto bet IDs
        EXPECTED: 
        """
        pass

    def test_004_go_to_lotto_tab_ofbet_history(self):
        """
        DESCRIPTION: Go to 'Lotto' tab of 'Bet History'
        EXPECTED: 
        """
        pass

    def test_005_veriify_bet_history_data_received_from_ss_for_lotto_bets(self):
        """
        DESCRIPTION: Veriify Bet History data received from SS for Lotto bets
        EXPECTED: **Lotto Bet History must comprise the following items** :
        EXPECTED: **Bet Receipt #**
        EXPECTED: **Selection Details**
        EXPECTED: *   Result : Pending/Lost/Won
        EXPECTED: *   Lottery : Lotto Name
        EXPECTED: *   Draw Type : e.g. Monday Draw, Teatime Draw. Time= 'drawAtTime' from SSResponse.
        EXPECTED: *   Draw Date : date bet is placed at
        EXPECTED: *   Number picked : displayed in ascending mode
        EXPECTED: **Stake & Return Details**
        EXPECTED: *   Bet placed at : date of placement
        EXPECTED: *   Bet Type : e.g. Double, Treble
        EXPECTED: *   Number of Lines : number of separate bets placed (e.g. number of combo options)
        EXPECTED: *   Stake : stake amount per line
        EXPECTED: *   Total Estimated Returns : (not returned from SS for now)
        EXPECTED: *   Total Wins : actual win amount if bet is won (or nothing if bet is lost)
        """
        pass
