from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


class BasePrivateMarketsTest(BaseBetSlipTest, BaseSportTest):
    stake_amount = '0.02'

    @property
    def event_name(self):
        return 'Auto test Catherineview v Auto test Allenburgh' if self.brand == 'ladbrokes' else 'Auto test Scottton v Auto test West Brooketown'

    @property
    def event_start_time(self):
        return '18:17, 25 Nov' if self.brand == 'ladbrokes' else '17:30, 25 Nov'

    @property
    def outcome_name(self):
            return 'Auto test Allenburgh'.upper() if self.brand == 'ladbrokes' else 'Auto test Scottton'

    @property
    def private_market_name(self):
        return vec.siteserve.EXPECTED_MARKETS_NAMES.next_team_to_score

    @property
    def private_outcome_name(self):
        return 'Player 2' if self.brand == 'ladbrokes' else 'Player 1'

    @property
    def event_id(self):
        return 1670296 if self.brand == 'ladbrokes' else 10994801

    @property
    def match_betting_selection_id(self):
        return '146452780' if self.brand == 'ladbrokes' else '602043144'

    @property
    def pm_selection_id(self):
        return '146452782' if self.brand == 'ladbrokes' else '602043205'

    def trigger_private_market_appearance(self, user: str, expected_market_name: str) -> None:
        """
        Places a bet again on the event which triggers Private Market appearance
        """
        try:
            content = self.site.home.get_module_content(module_name=self.expected_sport_tabs.private_market)
            items = content.accordions_list.items_as_ordered_dict
            if expected_market_name.upper() not in items:
                raise VoltronException(f'{expected_market_name.upper()} not in {items.keys()}')
        except VoltronException:
            self.open_betslip_with_selections(selection_ids=self.match_betting_selection_id)
            singles_section = self.get_betslip_sections().Singles
            self.assertTrue(singles_section.items(), msg='No stakes found')
            stake_name, stake = list(singles_section.items())[0]
            self.enter_stake_amount(stake=(stake_name, stake))
            self.get_betslip_content().bet_now_button.click()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.close_button.click()
            self.__class__.expected_betslip_counter_value = 0

            self.device.refresh_page()
            self.site.wait_splash_to_hide()

        if self.device_type != 'desktop':
            wait_for_result(
                lambda: self.expected_sport_tabs.private_market in self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict,
                timeout=10,
                bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                name='Private Market module to appear')
        else:
            wait_for_result(
                lambda: self.expected_sport_tabs.private_market in self.site.home.desktop_modules.items_as_ordered_dict,
                timeout=10,
                bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                name='Private Market module to appear')
