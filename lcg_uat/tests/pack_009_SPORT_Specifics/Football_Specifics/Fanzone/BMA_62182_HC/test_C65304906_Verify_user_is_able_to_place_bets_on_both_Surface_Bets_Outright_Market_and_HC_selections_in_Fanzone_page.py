import pytest
import tests
import datetime
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import BaseHighlightsCarouselTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304906_Verify_user_is_able_to_place_bets_on_both_Surface_Bets_Outright_Market_and_HC_selections_in_Fanzone_page(BaseHighlightsCarouselTest, BaseBetSlipTest):
    """
    TR_ID: C65304906
    NAME: Verify user is able to place bets on both Surface Bets, Outright Market and HC selections in Fanzone page
    DESCRIPTION: Verify user is able to place bets on both Surface Bets, Outright Market and HC selections in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    PRECONDITIONS: 6) Surface Bets are configured in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    PRECONDITIONS: 7) Outright Markets data is configured in Open Bet
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_precondition(self):
        if tests.settings.backend_env != 'prod':
            fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
            if not fanzone_status.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = event.selection_ids[event.team1]
            self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=self.selection_id,
                                                                                 priceNum=self.price_num,
                                                                                 priceDen=self.price_den)
            carousels = self.cms_config.get_fanzone_highlight_carousels()
            if not carousels:
                self.ob_config.create_fanzone_league_event_id(
                    league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
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
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(self):
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

    def test_003_click_on_any_odd_for_the_event_user_wants_to_place_bet_from_highlight_carousel(self):
        """
        DESCRIPTION: Click on any odd for the event user wants to place bet from Highlight Carousel
        EXPECTED: Quick Bet window should popup
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

    def test_004_close_quick_bet_section_and_add_more_selection_bet_slip(self):
        """
        DESCRIPTION: Close Quick Bet section and add more selection bet slip
        EXPECTED: User should be able to add more than 1 selections to the bet slip
        """
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.add_to_betslip_button.click()
        sleep(2)

    def test_005_now_add_one_selection_from_surface_bet(self):
        """
        DESCRIPTION: Now add one selection from Surface bet
        EXPECTED: User should be able to add the selection in bet slip
        """
        bet_buttons = self.events[1].items_as_ordered_dict
        for bet_button in bet_buttons.values():
            if bet_button.is_enabled():
                bet_button.click()
                break
        counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(counter, '2', msg='Unable to add more than one selection')

    def test_006_now_add_one_selection_from_outright_market(self):
        """
        DESCRIPTION: Now add one selection from Outright Market
        EXPECTED: User should be able to add the selection in bet slip
        """
        league = list(self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        market = list(league.accordions_list.items_as_ordered_dict.values())[0]
        event = list(market.items_as_ordered_dict.values())[0]
        event.bet_button.click()
        counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(counter, '3', msg='Unable to add outright selection to betslip')

    def test_007_enter_stake_click_on_place_bet(self):
        """
        DESCRIPTION: Enter stake Click on Place bet
        EXPECTED: User should be place bet successfully
        """
        self.site.open_betslip()
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
