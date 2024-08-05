import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant free bet on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C14824152_Verify_Bet_Receipt_after_bet_placement_using_FreeBet_bonuses(BaseBetSlipTest):
    """
    TR_ID: C14824152
    NAME: Verify Bet Receipt after bet placement using FreeBet bonuses
    DESCRIPTION: This test case verifies Bet Receipt after bet placement using FreeBet bonuses
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. User should have Free Bets available on their account
    PRECONDITIONS: 4. Make bet placement for selection using only free bet bonuses
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: ----
      """
    keep_browser_open = True

    def verify_bet_receipt(self, stake):
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        single_section = bet_receipt_sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        _, selection = list(single_section.items_as_ordered_dict.items())[0]

        self.assertTrue(selection.free_bet_stake, msg="Free bet amount is not displayed in the betreceipt")
        self.assertTrue(selection.estimate_returns, msg="Potential returns is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.has_free_bet_icon(), msg="Free bet icon is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.footer.free_bet_stake, msg="Free bet amount is not displayed in the betreceipt")
        self.assertTrue(self.site.bet_receipt.footer.total_estimate_returns, msg="Total potential returns is not displayed in the betreceipt")
        if stake:
            self.assertTrue(selection.total_stake, msg="Free bet amount + stake amount is not displayed in the betreceipt")
            self.assertTrue(self.site.bet_receipt.footer.total_stake, msg="Free bet amount + total stake amount is not displayed in the betreceipt")

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Make sure the user is logged into their account
        PRECONDITIONS: 3. User should have Free Bets available on their account
        PRECONDITIONS: 4. Make bet placement for selection using only free bet bonuses
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team2 = event.team2
        self.__class__.selection_id1 = list(event.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event.selection_ids.values())[1]

        username = tests.settings.betplacement_user
        for i in range(2):
            self.ob_config.grant_freebet(username, freebet_value=5)
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.place_single_bet(freebet=True)

    def test_001_verify_bet_receipt_after_bet_placement_using_only_for_example_500_freebet_bonuses(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using only, for example, £5.00 FreeBet bonuses
        EXPECTED: *[Before OX100]*
        EXPECTED: Stake for this bet: £5.00  ('Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx  ('Est. Returns' for Coral)
        EXPECTED: Total Stake £5.00
        EXPECTED: Potential Returns: £xx.xx ('Estimated Returns' for Coral)
        EXPECTED: *[From OX100.1]*
        EXPECTED: **Coral:**
        EXPECTED: - "Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Est. Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Estimated Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: ![](index.php?/attachments/get/36581)
        EXPECTED: **Ladbrokes:**
        EXPECTED: - "Stake for this bet: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: ![](index.php?/attachments/get/36582)
        """
        self.verify_bet_receipt(stake=False)

    def test_002_verify_bet_receipt_after_bet_placement_using_for_example_500_freebet_bonuses_plus_1000_cash_stake(self):
        """
        DESCRIPTION: Verify bet receipt after bet placement using, for example, £5.00 FreeBet bonuses + £10.00 Cash stake
        EXPECTED: *[Before OX100]*
        EXPECTED: Stake for this bet: £15.00  ('Stake' for Coral)
        EXPECTED: Free Bet Amount: -£5.00
        EXPECTED: Potential Returns: £xx.xx   ('Est. Returns' for Coral)
        EXPECTED: Total Stake £15.00
        EXPECTED: Potential Returns: £xx.xx    ('Estimated Returns' for Coral)
        EXPECTED: *[From OX100.1]*
        EXPECTED: **Coral:**
        EXPECTED: - "Stake: [Free Bet signposting icon][Free Bet value (e.g.£5.00)] [+] [Stake value, (e.g.£10.00)]"
        EXPECTED: - "Est. Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet(s) value (e.g.£5.00)] [+] [Stake(s) value (e.g.£10.00)]"
        EXPECTED: - "Estimated Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: ![](index.php?/attachments/get/36583)
        EXPECTED: **Ladbrokes:**
        EXPECTED: - "Stake for this bet: [Free Bet signposting icon][Free Bet value (e.g.£5.00)] [+] [Stake value, (e.g.£10.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: - "Total Stake: [Free Bet signposting icon][Free Bet(s) value (e.g.£5.00)] [+] [Stake(s) value (e.g.£10.00)]"
        EXPECTED: - "Potential Returns: [Value, (e.g.£xx.xx or N/A)]"
        EXPECTED: ![](index.php?/attachments/get/36587)
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id2)
        selections = self.get_betslip_sections().Singles
        selection = selections.get(self.team2, None)
        selection.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()
        self.place_single_bet(number_of_stakes=1)
        self.verify_bet_receipt(stake=True)
