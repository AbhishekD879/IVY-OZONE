import pytest
import tests
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2779917_Verify_displaying_odds_boost_button_in_Quick_Bet_for_logged_out_user(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2779917
    NAME: Verify displaying odds boost button in Quick Bet for logged out user
    DESCRIPTION: This test case verifies that odds boost button displaying in Quickbet for logged out user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quickbet is enabled
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         DESCRIPTION: "Odds Boost" Feature Toggle is enabled in CMS. Football event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Login button is not displayed')

        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(
                LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter,
                                                         in_play_event=False)[0]
            self.__class__.eventID = events['event']['id']
            market = next((market for market in events['event']['children']
                           if market.get('market').get('templateMarketName') == 'Match Betting' and
                           market['market'].get('children')), None)
            market_name = market['market']['name']
            market = next((market for market in events['event']['children']), None)
            outcomes_resp = market['market']['children']
            self.__class__.all_selection_ids = [i['outcome']['id'] for i in outcomes_resp]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.__class__.all_selection_ids = list(event_params.selection_ids.values())
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                    '')
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_with_odds_boost_availableverify_that_quick_bet_popup_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet popup is shown WITHOUT 'BOOST' button
        EXPECTED: - Quick Bet popup is shown
        EXPECTED: - 'BOOST' button is NOT shown in Quickbet
        """
        if self.device_type == 'mobile':
            self.navigate_to_edp(event_id=self.eventID)
            self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            self.assertFalse(self.site.quick_bet_panel.has_odds_boost_button(expected_result=False),
                             msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is shown')
        else:
            self.open_betslip_with_selections(selection_ids=self.all_selection_ids[1])
            self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                             msg='Odds Boost header is displayed on betslip')
