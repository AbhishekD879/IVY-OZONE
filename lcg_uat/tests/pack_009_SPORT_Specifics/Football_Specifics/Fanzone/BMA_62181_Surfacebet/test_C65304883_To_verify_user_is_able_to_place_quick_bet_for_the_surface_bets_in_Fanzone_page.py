import pytest
import datetime
import tests
import voltron.environments.constants as vec
from collections import OrderedDict
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304883_To_verify_user_is_able_to_place_quick_bet_for_the_surface_bets_in_Fanzone_page(BaseBetSlipTest):
    """
    TR_ID: C65304883
    NAME: To verify user is able to place quick bet for the surface bets in Fanzone page
    DESCRIPTION: To verify user is able to place quick bet for the surface bets in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS- for eg:Everton team
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    bet_amount = 0.1
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            event_type_id = event['event']['typeId']
            card_number = tests.settings.master_card
            card_type = 'mastercard'
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            outcomes = next(((market['market']['children']) for market in event.ss_response['event']['children'] if
                             'Match Betting' in market['market']['templateMarketName'] and market['market'].get(
                                 'children')), None)
            selection_id = event.selection_ids[event.team1]
            event_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            card_number = tests.settings.visa_card
            card_type = 'visa'
        price_values = OrderedDict([(outcome['outcome']['name'],
                                     f'{outcome["outcome"]["children"][0]["price"]["priceNum"]}/'
                                     f'{outcome["outcome"]["children"][0]["price"]["priceDen"]}')
                                    for outcome in outcomes])
        self.__class__.price_val = list(price_values.values())[0]
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                       typeId=str(event_type_id))
        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=3,
                                                                             priceDen=7)
        self.__class__.surface_bet_name = self.surface_bet['title'].upper()
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=card_number,
                                                                     card_type=card_type,
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10,
                        name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        # as per the new change, after subscription, we will be in fanzone page only
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_002_verify_if_user_is_able_to_see_surface_bet_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Surface bet in Now and Next tab
        EXPECTED: User should be able to see Surface bets in Now and Next tab
        """
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')

    def test_003_click_on_the_odd_value_displayed_in_surface_bet(self):
        """
        DESCRIPTION: Click on the odd value displayed in surface bet
        EXPECTED: The selected odd should be added to quick bet and user should be able to place order
        """
        surface_bet = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict[self.surface_bet_name]
        surface_bet.bet_button.click()
        sleep(2)
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            odds_value = self.site.quick_bet_panel.selection.content.odds_value
            self.assertEqual(odds_value, self.price_val,
                             msg=f'Expected price "{self.price_val}" is not equal to actual "{odds_value}"')
            quick_bet.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
        else:
            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[0]
            self.assertEqual(stake.odds, self.price_val,
                             msg=f'Expected price "{self.price_val}" is not equal to actual "{stake.odds}"')
            stake.amount_form.input.value = self.bet_amount
            self.get_betslip_content().bet_now_button.click()
            self.check_bet_receipt_is_displayed()
