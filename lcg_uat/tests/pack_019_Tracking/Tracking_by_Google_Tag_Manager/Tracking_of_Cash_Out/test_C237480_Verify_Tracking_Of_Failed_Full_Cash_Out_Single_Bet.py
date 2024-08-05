import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException


# @pytest.mark.prod  # Uncomment after VOL-4305
# @pytest.mark.hl    # and change in test rail: Automated? - Automated
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.google_analytics
@pytest.mark.cash_out
@pytest.mark.bet_placement
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-4305')
@pytest.mark.login
@vtest
class Test_C237480_Verify_Tracking_Of_Failed_Full_Cash_Out_Single_Bet(BaseDataLayerTest, BaseCashOutTest):
    """
    TR_ID: C237479
    VOL_ID: C9698038
    NAME: Tracking of Failed Cash Out
    """
    bet_amount = 1.0
    expected_response = {
        'event': 'trackEvent',
        'eventCategory': 'cash out',
        'eventAction': 'attempt',
        'eventLabel': 'failure',
        'cashOutType': 'full',
        'cashOutOffer': '',
        'errorCode': 'cashout seln suspended',
        'errorMessage': '',
        'location': 'event page',
        'oddsBoost': 'no'
    }
    draw_selection = 'Draw'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Log in
        DESCRIPTION: Place bet
        """
        self.__class__.event_info = self.ob_config.add_autotest_premier_league_football_event()
        self.site.login()
        self.open_betslip_with_selections(self.event_info.selection_ids[self.event_info.team1])
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets_on_event_details(self):
        """
        DESCRIPTION: Navigate to MY BETS tab on Event Details page
        """
        if self.brand == "ladbrokes":
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_edp(event_id=self.event_info.event_id)
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_do_full_cash_out(self):
        """
        DESCRIPTION: Trigger the situation when market is suspended and try to do Full Cash Out
        EXPECTED: Error message is shown about Cashout unsuccessful
        """
        self.__class__.unsuccess_message = vec.bet_history.CASHOUT_BET.cashout_attempt_errors.cashout_seln_suspended
        wait_for_result(lambda: self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict,
                        name='Cashout bets to appear',
                        timeout=2,
                        bypass_exceptions=(VoltronException, StaleElementReferenceException))
        if self.brand == "ladbrokes":
            bet_name, bet = self.site.open_bets.tab_content.accordions_list. \
                get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_info.team1, number_of_bets=1)
        else:
            bet_name, bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_info.team1, number_of_bets=1)
        self.__class__.cashout_amount = bet.buttons_panel.full_cashout_button.amount.value
        bet.buttons_panel.full_cashout_button.click()
        event_id = self.event_info.event_id
        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_market_state(event_id=event_id,
                                           market_id=self.ob_config.market_ids[event_id][market_short_name],
                                           displayed=True,
                                           active=False)
        bet.buttons_panel.cashout_button.click()

        def get_message():
            bet_name_, bet_ = self.site.sport_event_details.my_bets.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_info.team1, number_of_bets=1)
            return bet_.buttons_panel.cashout_message.text

        # there is no possibility to verify error message on ladbrokes - it disappears in 1-2 sec
        if self.brand != 'ladbrokes':
            result = wait_for_result(lambda: get_message() == self.unsuccess_message,
                                     name=f'Error message "{self.unsuccess_message}" to appear',
                                     bypass_exceptions=(VoltronException, StaleElementReferenceException),
                                     timeout=3)
            self.assertTrue(result,
                            msg=f'Error message "{self.unsuccess_message}" has not appeared')

    def test_003_verify_data_layer_response(self):
        """
        DESCRIPTION: Get dataLayer response and verify it contains required Tracking of Failed Cash Out push
        EXPECTED: cashOutOffer and errorMessage field are correct
        """
        actual_response = self.get_data_layer_specific_object('eventCategory', 'cash out', timeout=3)
        self.__class__.expected_response['cashOutOffer'] = float(self.cashout_amount)
        self.__class__.expected_response['errorMessage'] = 'unsuccessful cash out, %s' % self.unsuccess_message.lower()
        self.compare_json_response(actual_response, self.expected_response)
