from time import sleep
import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.quick_bet
@pytest.mark.reg167_fix
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.login
@vtest
class Test_C717042_C892300_C15392871_Verify_Quick_Stakes(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C717042
    TR_ID: C892300
    TR_ID: C15392871
    VOL_ID: C9698186
    NAME: Verify Quick Stakes
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True
    lp = {0: '1/2'}
    quick_bet = None

    def test_001_create_test_event_and_navigate_to_it(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Open created event
        """
        self.__class__.currencies = {
            '£': tests.settings.betplacement_user,
            '$': tests.settings.user_with_usd_currency_and_card,
            '€': tests.settings.user_with_euro_currency_and_card,
        }
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         expected_template_market='Win or Each Way',
                                                         all_available_events=True)
            event = None
            for potential_event in events:
                for market in potential_event['event']['children']:
                    if market['market'].get('children') and market.get('market').get(
                            'templateMarketName') == 'Win or Each Way':
                        outcomes_resp = market['market']['children']
                        for outcome in outcomes_resp:
                            if outcome['outcome'].get('children'):
                                for child in outcome['outcome']['children']:
                                    if child.get('price'):
                                        if 'SP' not in child.get('price').get('priceType'):
                                            event = potential_event
                                break
                        break
                break

            if not event:
                raise SiteServeException('There are no Event where selections with LP prices only')

            self.__class__.eventID = event['event']['id']
            self._logger.debug(f'*** Found Horse racing event "{self.eventID}"')
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.lp)
            self.__class__.eventID = event.event_id

    def test_002_verify_quick_stakes_for_gbp_usd_eur_currency(self):
        """
        DESCRIPTION: Add <Race> selection to Quick Bet
        DESCRIPTION: Verify Quick Stakes
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: Added selection and all data are displayed in Quick Bet
        EXPECTED: Quick Stakes buttons are displayed with the next values:
        EXPECTED: * +<currency symbol>5
        EXPECTED: * +<currency symbol>10
        EXPECTED: * +<currency symbol>50
        EXPECTED: * +<currency symbol>100
        """
        for currency, username in self.currencies.items():
            self._logger.info(f'*** Verifying user "{username}" with "{currency}" currency')

            self.site.login(username=username)
            self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
            self.site.wait_content_state_changed(timeout=15)
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
            odds_boost = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, verify_name=False, timeout=5)
            if odds_boost:
                odds_boost.close_dialog()
            self.add_selection_to_quick_bet()
            self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=10),
                            msg='Amount input field is not displayed')
            self.__class__.quick_bet = self.site.quick_bet_panel.selection
            quick_stakes_fe = self.quick_bet.quick_stakes.items_as_ordered_dict
            # handles each way tooltip pop-up in quick bet
            if self.quick_bet.content.has_odds_boost_tooltip():
                sleep(10)
            self.quick_bet.content.amount_form.input.click()

            if tests.settings.backend_env != 'prod':
                odds = self.lp.values()

            bet_amount = 0
            quick_stakes_cms = self.cms_config.get_system_configuration_structure()['PredefinedStakes'][
                'quickbet_stakes'].split(',')
            if len(quick_stakes_cms) != 4:
                quick_stakes_cms = self.cms_config.get_system_configuration_structure()['PredefinedStakes'][
                    'global_stakes'].split(',')
            stakes_order_cms = []
            for stake in quick_stakes_cms:
                expected_key = ('+' + currency + str(stake))
                stakes_order_cms.append(expected_key)
                self.assertIn(expected_key, quick_stakes_fe.keys(),
                              msg=f'"{expected_key}" not found in "{list(quick_stakes_fe.keys())}"')

                bet_amount += float(stake)
                self.quick_bet.quick_stakes.keys[expected_key].click()
                est_returns = self.quick_bet.bet_summary.total_estimate_returns
                if tests.settings.backend_env == 'prod':
                    odds = self.quick_bet.content.odds_value
                self.verify_estimated_returns(est_returns=est_returns, bet_amount=bet_amount, odds=odds)
            # Verify Quick stake buttons order as per cms
            self.assertListEqual(stakes_order_cms, list(quick_stakes_fe.keys()), msg=f'Quick stakes from cms {stakes_order_cms} is not equal to {list(quick_stakes_fe.keys())}')
            self.quick_bet.content.amount_form.input.value = self.bet_amount
            key = ('+' + currency + stake)
            self.quick_bet.quick_stakes.keys[key].click()

            est_returns = self.quick_bet.bet_summary.total_estimate_returns
            self.verify_estimated_returns(est_returns=est_returns,
                                          bet_amount=float(self.bet_amount) + float(stake),
                                          odds=odds)

            self.site.quick_bet_panel.header.close_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
            self.site.open_betslip()
            self.clear_betslip()
            self.site.logout()
