import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


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
class Test_AT_237479_Verify_Tracking_Of_Successful_Partial_Cash_Out_Multiple_Bet(BaseDataLayerTest, BaseCashOutTest):
    """
    TR_ID: C237479
    VOL_ID: C9690269
    NAME: Tracking of Successful Partial Cash Out for Multiple Bets
    DESCRIPTION: This test case verifies tracking of successful Cash Out
    """
    bet_amount = 1.0
    number_of_events = 3
    expected_response = {
        'event': 'trackEvent',
        'eventCategory': 'cash out',
        'eventAction': 'attempt',
        'eventLabel': 'success',
        'cashOutType': 'partial',
        'cashOutOffer': '',
        'partialPercentage': 50,
        'successMessage': '',
        'location': 'event page',
        'oddsBoost': 'no'
    }
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Log in
        DESCRIPTION: Place bet
        """
        # event 1
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.event1_ID = event['event']['id']
        outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                         market['market'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.event1_team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                            outcome['outcome'].get('outcomeMeaningMinorCode')and
                                            outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
        if not self.event1_team1:
            raise SiteServeException('No Home team found')
        self._logger.info(f'*** Found Football event with event id "{self.event1_ID}" and team "{self.event1_team1}"')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_ids.append(selection_ids[self.event1_team1])

        # event 2
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.event2_ID = event['event']['id']
        outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                         market['market'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.event2_team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                            outcome['outcome'].get('outcomeMeaningMinorCode') and
                                            outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
        if not self.event2_team1:
            raise SiteServeException('No Home team found')
        self._logger.info(f'*** Found Football event with event id "{self.event2_ID}" and team "{self.event2_team1}"')
        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.selection_ids.append(selection_ids[self.event2_team1])

        # need to login with No Freebet available user VOL-1621
        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.open_betslip_with_selections(self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_001_navigate_to_my_bets_on_event_details(self):
        """
        DESCRIPTION: Navigate to MY BETS tab on Event Details page
        """
        if self.brand == "ladbrokes":
            self.site.close_betreceipt()
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_edp(event_id=self.event1_ID)
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_do_partial_cash_out(self):
        """
        DESCRIPTION: Set partial Cash Out amount and confirm Cash Out
        """
        if self.brand == "ladbrokes":
            bet_name, bet = self.site.cashout.tab_content.accordions_list. \
                get_bet(bet_type=vec.betslip.TBL.upper(), event_names=self.event1_team1, number_of_bets=3)
        else:
            bet_name, bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(
                event_names=self.event1_team1, number_of_bets=2)
        bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(bet.buttons_panel.wait_for_cashout_slider(), msg='PARTIAL CASHOUT slider was not appeared')
        self.__class__.cashout_amount = bet.buttons_panel.partial_cashout_button.amount.value
        bet.buttons_panel.partial_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        success_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS if self.brand == 'ladbrokes' \
            else vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(bet.wait_for_message(message=success_message, timeout=10),
                        msg=f'Message "{success_message}" was not shown')

    def test_003_verify_data_layer_response(self):
        """
        DESCRIPTION: Get dataLayer response and verify it contains required
        DESCRIPTION: Tracking of Successful Cash Out push
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='cash out')
        self.__class__.expected_response['cashOutOffer'] = float(self.cashout_amount)
        if self.brand == 'ladbrokes':
            self.__class__.expected_response['successMessage'] = 'partial cash out successful'
        else:
            self.__class__.expected_response['successMessage'] = \
                f'successful cash out, your cash out attempt was successful £{self.cashout_amount}. ' \
                f'50% of your bet was cashed out.'
        self.compare_json_response(actual_response, self.expected_response)
