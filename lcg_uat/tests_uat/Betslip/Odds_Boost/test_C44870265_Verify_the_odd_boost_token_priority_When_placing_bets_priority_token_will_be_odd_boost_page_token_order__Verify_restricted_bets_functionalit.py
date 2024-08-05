import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


# @pytest.mark.prod - Can't executed on prod, Can't add odds boost token on prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.medium
@vtest
class Test_C44870265_Verify_the_odd_boost_token_priority_When_placing_bets_priority_token_will_be_odd_boost_page_token_order__Verify_restricted_bets_functionality(BaseBetSlipTest):
    """
    TR_ID: C44870265
    NAME: "Verify the odd boost token priority, (When placing bets priority token will be odd boost page token order ) - Verify restricted bets functionality"
    DESCRIPTION: "Verify the odd boost token priority,
    """
    keep_browser_open = True

    def test_001_verify_the_odd_boost_token_priority(self):
        """
        DESCRIPTION: "Verify the odd boost token priority,
        EXPECTED: Odds boost is displayed in the betslip and the odds can be boosted.
        """
        selection_ids = self.ob_config.add_tennis_event_to_autotest_trophy().selection_ids
        self.assertTrue(selection_ids, msg='"Selections" are not found')
        home_team, home_team_selection_id = list(selection_ids.items())[0]
        username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=home_team_selection_id)
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=home_team_selection_id)
        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        odds_boost_header.boost_button.click()
        sleep(5)
        boosted = odds_boost_header.boost_button.name
        self.assertEqual(boosted, vec.odds_boost.BOOST_BUTTON.enabled, msg=f'Actual button"{boosted}" not changed to Expected button "{vec.odds_boost.BOOST_BUTTON.enabled}"')
        self.__class__.singles_section = self.get_betslip_sections().Singles
        stake = self.singles_section[home_team]
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

    def test_002_verify_restricted_bets_functionality(self):
        """
        DESCRIPTION: Verify restricted bets functionality"
        EXPECTED: Odds boost tokens which are not allowed for the restricted bets shows the error message
        EXPECTED: eg: using a free bet while boosting the odds > restricts the odds boost
        """
        stake_name, stake = list(self.singles_section.items())[0]
        self.assertTrue(stake.has_use_free_bet_link(), msg='"Has Use Free Bet" link was not found')
        stake.use_free_bet_link.click()
        self.select_free_bet()
        if self.brand == 'ladbrokes':
            free_bet_error_dialog = self.site.wait_for_dialog(vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet, timeout=5, verify_name=True)
        else:
            free_bet_error_dialog = self.site.wait_for_dialog(vec.odds_boost.BETSLIP_DIALOG.continue_with_freebet.upper(), timeout=5, verify_name=True)
        self.assertEqual(free_bet_error_dialog.description, vec.odds_boost.BETSLIP_DIALOG.cancel_boost_price_message,
                         msg=f'"{vec.odds_boost.BETSLIP_DIALOG.cancel_boost_price_message}"'
                             f' button is not shown on pop up')
        self.assertTrue(free_bet_error_dialog.no_thanks_button,
                        msg=f'"{vec.odds_boost.BETSLIP_DIALOG.no_thanks}" button is not on pop up')
        self.assertTrue(free_bet_error_dialog.yes_please_button,
                        msg=f'"{vec.odds_boost.BETSLIP_DIALOG.yes_please}" button is not on popup')
