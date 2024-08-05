import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.medium
@vtest
class Test_C59898487_Accept_bet_made_with_an_Odds_boost_token(BaseBetSlipTest):
    """
    TR_ID: C59898487
    NAME: Accept bet made with an Odds boost token
    """
    keep_browser_open = True
    max_bet = 0.2
    prices = {'odds_home': '1/2', 'odds_away': '1/10', 'odds_draw': '1/9'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name = event_params.team1
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username, async_close_dialogs=False)
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id)

    def test_001_add_a_selection_to_quick_bet_or_bet_slip_click_on_odds_boost_and_trigger_overask(self):
        """
        DESCRIPTION: Add a selection to Quick Bet or bet slip, click on Odds Boost and trigger Overask.
        EXPECTED: Your bet should have gone through to Overask
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections, msg=f'"{selections}" is not added to the betslip')

        odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        stake = list(selections.values())[0]
        self.__class__.new_price = stake.boosted_odds_container.price_value
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_ti_accept_the_bet(self):
        """
        DESCRIPTION: In the TI, accept the bet.
        EXPECTED: You should see the bet receipt and it should have the Odds Boost signposting.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_odds_boost_signpost(), msg='"odds boost" signpost is not displayed')

    def test_003_check_my_bets_open_bets_and_verify_that_you_see_your_bet_there_and_that_it_has_the_odds_boost_signposting(self):
        """
        DESCRIPTION: Check My Bets->Open Bets and verify that you see your bet there and that it has the Odds Boost signposting.
        EXPECTED: Your bet should be in My Bets->Open Bets and it should have the Odds Boost signposting.
        """
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name)
        self.assertTrue(self.event_name in bet_name,
                        msg=f'*** "{self.event_name}" bet not found in the openbets')
        self.assertTrue(bet.has_odds_boost_signpost(), msg=f'"odds boost" signpost is not displayed for "{bet_name}"')
