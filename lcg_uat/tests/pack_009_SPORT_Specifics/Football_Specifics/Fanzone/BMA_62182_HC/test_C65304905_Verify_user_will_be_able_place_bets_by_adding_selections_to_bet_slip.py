import pytest
import datetime
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.prod # can't create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304905_Verify_user_will_be_able_place_bets_by_adding_selections_to_bet_slip(BaseBetSlipTest):
    """
       TR_ID: C65304905
       NAME: Verify user will be able place bets by adding selections to bet slip
       DESCRIPTION: Verify user will be able place bets by adding selections to bet slip
       PRECONDITIONS: 1)User has access to CMS
       PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
       PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
       PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
       PRECONDITIONS: 5) HC should be created in CMS, as per below path
       PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
       """
    keep_browser_open = True

    price_num = 1
    price_den = 2
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title(),str(typeId))
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_united.title(),str(typeId))
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_id = event.selection_ids[event.team1]
        self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                priceNum=self.price_num,
                                                priceDen=self.price_den)
        event1 = self.ob_config.add_autotest_premier_league_football_event()
        selection_id1 = event1.selection_ids[event1.team1]
        self.cms_config.add_fanzone_surface_bet(selection_id=selection_id1,
                                                priceNum=self.price_num,
                                                priceDen=self.price_den)
        carousels = self.cms_config.get_fanzone_highlight_carousels()
        if not carousels:
            self.ob_config.create_fanzone_league_event_id(
                league_id=self.typeId,
                home_team=vec.fanzone.TEAMS_LIST.manchester_city,
                away_team=vec.fanzone.TEAMS_LIST.manchester_united,
                home_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city,
                away_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_united)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount='20',
                                                                     card_number='4506620004077430',
                                                                     card_type='visa',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(
            self):
        """
        DESCRIPTION: Navigate to Fanzone page any of the below listed entry points
        DESCRIPTION: a. Fanzone in Sports Ribbon(only mobile)
        DESCRIPTION: b. Fanzone in A-Z/All sports
        DESCRIPTION: c. Launch Banner in Home page
        DESCRIPTION: d. Launch banner in Football landing page
        EXPECTED: User should be navigated to Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                                 name='Fanzone page not displayed',
                                 timeout=5)
        self.assertTrue(result, msg='fanzone page not loaded')

    def test_002_verify_user_is_able_to_see_events_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify user is able to see Events in Now and Next tab
        EXPECTED: User should be able to see Events section in Now and Next tab
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(vec.fanzone.NOW_AND_NEXT)

    def test_003_click_on_any_odd_for_the_event_user_wants_to_place_bet(self):
        """
        DESCRIPTION: Click on any odd for the event user wants to place bet
        EXPECTED: Odd should be shown selected for quick bet
        """
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        self.__class__.events = list(carousel.items_as_ordered_dict.values())
        bet_buttons = self.events[0].items_as_ordered_dict
        for bet_button in bet_buttons.values():
            if bet_button.is_enabled():
                bet_button.click()
                break
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            sleep(2)

    def test_004_close_quick_bet_section_and_add_more_selection_bet_slip(self):
        """
        DESCRIPTION: Close Quick Bet section and add more selection bet slip
        EXPECTED: User should be able to add more than 1 selections to the bet slip
        """
        bet_buttons = self.events[1].items_as_ordered_dict
        for bet_button in bet_buttons.values():
            if bet_button.is_enabled():
                bet_button.click()
                break
        counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(counter, '2', msg='Unable to add more than one selection')
        league = list(self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        market = list(league.accordions_list.items_as_ordered_dict.values())[0]
        event = list(market.items_as_ordered_dict.values())[0]
        event.bet_button.click()
        counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(counter, '3', msg='Unable to add outright selection to betslip')

    def test_005_enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter Stake and Click on Place bet
        EXPECTED: User should be place bet successfully
        """
        self.site.open_betslip()
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

