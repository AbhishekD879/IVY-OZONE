import pytest
import tests
import datetime
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65304904_Verify_Quick_bet_functionality_on_by_placing_bets_on_HC(BaseBetSlipTest):
    """
    TR_ID: C65304904
    NAME: Verify Quick bet functionality on by placing bets on HC
    DESCRIPTION: Verify Quick bet functionality on by placing bets on HC
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
        PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
        PRECONDITIONS: 5) HC should be created in CMS, as per below path
        PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
        """
        if tests.settings.backend_env != 'prod':
            fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
            if not fanzone_status.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = event.selection_ids[event.team1]

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

    def test_003_click_on_any_odd_for_the_event_user_wants_to_place_bet(self):
        """
        DESCRIPTION: Click on any odd for the event user wants to place bet
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
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()

    def test_004_enter_the_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter the Stake and Click on Place bet
        EXPECTED: User should be able to place bet successfully
        """
        self.site.open_betslip()
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
