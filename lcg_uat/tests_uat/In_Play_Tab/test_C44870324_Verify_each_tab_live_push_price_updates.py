import pytest
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870324_Verify_each_tab_live_push_price_updates(Common):
    """
    TR_ID: C44870324
    NAME: Verify each tab live push price updates
    DESCRIPTION: this test case verify price updates
    """
    keep_browser_open = True
    bet_buttons_count = []

    def selections(self):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        self.length = len(bet_buttons_list)
        for i in range(0, self.length):
            selection_btn = bet_buttons_list[i]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.is_enabled() and not selection_btn.is_selected() and selection_btn.text != 'SP':
                try:
                    selection_btn.click()
                    break
                except ElementClickInterceptedException:
                    self.bet_buttons_count.append(selection_btn)
                    self._logger.info('ElementClickInterceptedException ..')
                    continue
            else:
                continue
        if len(self.bet_buttons_count) == self.length:
            self._logger.info('No enabled selections available')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen Application
        EXPECTED: Home Page is opened
        """
        self.site.wait_content_state(state_name='homepage')

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab is opened
        """
        if self.device_type == 'mobile':
            inplay = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            inplay = self.site.header.sport_menu.items_as_ordered_dict
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            inplay[vec.bma.IN_PLAY].click()
        else:
            inplay[vec.bma.IN_PLAY.upper()].click()
        self.site.wait_content_state(state_name='in-play')

    def test_003_verify_oddsprice_updates_for_all_inplay_sports(self):
        """
        DESCRIPTION: Verify odds/Price updates for all Inplay sports
        EXPECTED: Odd/price updated successfully
        """
        inplay_menu = self.site.inplay.inplay_sport_menu
        inplay = list(inplay_menu.items_as_ordered_dict.items())
        for sport_name, sport in inplay[0:6]:
            if sport_name != 'WATCH LIVE':
                inplay_menu.click_item(sport_name)
                if self.device_type == 'mobile':
                    if self.site.inplay.tab_content.live_now_counter == 0:
                        self._logger.info('No live events available')
                        continue
                else:
                    tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict['LIVE NOW']
                    if tabs.counter == 0:
                        self._logger.info('No live events available')
                        continue
                self.selections()
                if len(self.bet_buttons_count) == self.length:
                    self._logger.info('No enabled selections available')
                    continue
                if self.device_type == 'mobile':
                    self.site.quick_bet_panel.add_to_betslip_button.click()
                self.site.open_betslip()
                if self.site.betslip.warning_message == vec.betslip.SELECTION_DISABLED:
                    self.site.betslip.remove_all_button.click()
                    dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
                    dialog.continue_button.click()
                    self.selections()
                self.site.betslip.wait_for_warning_message_text(vec.betslip.SELECTION_DISABLED)
                self.site.betslip.remove_all_button.click()
                dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
                dialog.continue_button.click()
