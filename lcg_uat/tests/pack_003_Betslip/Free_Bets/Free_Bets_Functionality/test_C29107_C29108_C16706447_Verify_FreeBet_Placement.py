import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed now, can't create OB event on prod/hl, can't grant freebets
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.login
@pytest.mark.safari
@vtest
class Test_C29107_C29108_C16706447_Verify_FreeBet_Placement(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29107
    TR_ID: C29108
    TR_ID: C16706447
    NAME: Verify Free Bet Placement
    """
    keep_browser_open = True
    freebet_value = 1.03

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        """
        self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that have Freebets available
        """
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value)
        self.site.login(username=username)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')

    def test_002_add_selection_to_the_bet_slip_via_deeplink(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Selection is added
        EXPECTED: Bet Slip page is open
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])

    def test_003_make_freebet_bet(self):
        """
        DESCRIPTION: Make a bet using Freebet option
        EXPECTED: Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section.items()) == 1, msg='One stake should be found in betslip Singles section')

        stake_name, stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        stake.amount_form.input.value = self.bet_amount
        stake.freebet_tooltip.click()
        stake.use_free_bet_link.click()

        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value))

        total_stake = self.get_betslip_content().total_stake.replace('\n', '')
        stake_and_freebet_stake = str(self.freebet_value) + ' + ' + str(self.bet_amount)
        self.assertEqual(stake_and_freebet_stake, total_stake,
                         msg=f'Freebet stake + stake: "{stake_and_freebet_stake}" != total stake: "{total_stake}"')
        self.get_betslip_content().bet_now_button.click()

        self.check_bet_receipt_is_displayed()
