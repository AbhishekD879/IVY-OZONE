import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choices
from time import sleep
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893593_Verify_the_bet_displays_in_open_bets_when_one_of_the_events_are_still_open(BaseBetSlipTest):
    """
    TR_ID: C64893593
    NAME: Verify the bet displays in open bets when one of the events are still open
    """
    keep_browser_open = True
    selection_ids = []

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_login_button_and_enter_valid_credentials4track_an_acca_bet_where_events_are_not_completed6_bet_remains_in_open_betexpected_resultbet_should_remain_in_open_bets(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports url.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on login button and enter valid credentials.
        DESCRIPTION: 4.Track an acca bet where events are not completed
        DESCRIPTION: 5. bet remains in open bet
        EXPECTED: 1. Bet should remain in open bets
        """
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.login()
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in cms')

            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter, all_available_events=True,
                                                         in_play_event=False)
            required_events = choices(events, k=4)
            for event in required_events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)

            for i in range(4):
                event = self.ob_config.add_autotest_premier_league_football_event()
                selection_id = event.selection_ids[event.team1]
                self.selection_ids.append(selection_id)

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=1)
        self.site.bet_receipt.close_button.click()

        self.site.open_my_bets_open_bets()
        sleep(2)
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets are available')
        bet = list(bets.values())[0]
        if bet.edit_my_acca_button:
            self._logger.info(msg='Acca bet is in openbets')
        else:
            raise VoltronException('Acca bet not found')
