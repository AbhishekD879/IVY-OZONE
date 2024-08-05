import pytest
import datetime
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.environments import constants as vec
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65305295_To_verify_user_is_able_to_place_surface_bet_bets_from_betslip_single_multiple(BaseBetSlipTest):
    """
    TR_ID: C65305295
    NAME: To verify user is able to place surface bet bets from betslip single/multiple
    DESCRIPTION: To verify user is able to place surface bet bets from betslip single/multiple
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'
    price_num = 1
    price_den = 2

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Surface bets are created with with below data:
        PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
        PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id_2 = list(event_selection.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            selection_id_2 = event.selection_ids[event.team2]
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)
        self.__class__.surface_bet_2 = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id_2,
                                                                               priceNum=self.price_num,
                                                                               priceDen=self.price_den)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount="20",
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(2)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click() as per the new change, after subscription, we will be in fanzone page only
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_user_is_able_to_see_surface_bet_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Surface bet in Now and Next tab
        EXPECTED: User should be able to see Surface bets in Now and Next tab
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = [self.surface_bet['title'].upper(), self.surface_bet_2['title'].upper()]
        self.__class__.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        for bet in surface_bet_name:
            self.assertIn(bet, self.surface_bets,
                          msg=f'Created surface bet "{bet}" is not present in "{self.surface_bets}"')

    def test_003_click_on_the_odd_value_displayed_in_surface_bet_and_add_it_to_betslip(self):
        """
        DESCRIPTION: Click on the odd value displayed in surface bet and add it to betslip
        EXPECTED: User should be able to add surface bet to betslip
        """
        wait_for_haul(3)

        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)

        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()
        for surface_bet in self.surface_bets.values():
            if surface_bet.bet_button.is_enabled():
                surface_bet.bet_button.click()
                break
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel(timeout=10)
            self.site.quick_bet_panel.add_to_betslip_button.click()
        else:
            counter_value = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(counter_value, "1", msg=f'Actual counter value {counter_value} is not '
                                                     f'same as Expected value {"1"}')

    def test_004_add_2_3_more_surface_bet_to_betslip(self):
        """
        DESCRIPTION: Add 2-3 more surface bet to betslip
        EXPECTED: User should be able to add surface bet to betslip
        """
        count = 1
        for surface_bet in self.surface_bets.values():
            button = surface_bet.bet_button
            if button.is_enabled() and not button.is_selected():
                surface_bet.bet_button.click()
                count += 1
                counter_value = self.site.header.bet_slip_counter.counter_value
                self.assertEqual(counter_value, str(count), msg=f'Actual counter value {counter_value} is not '
                                                                f'same as Expected value {str(count)}')
                if count == 3:
                    break

    def test_005_click_on_place_order(self):
        """
        DESCRIPTION: Click on place order
        EXPECTED: User should be able to place order successfully for the surface bets
        """
        if self.device_type == 'mobile':
            self.site.open_betslip()
        self.place_multiple_bet(number_of_stakes=1)
