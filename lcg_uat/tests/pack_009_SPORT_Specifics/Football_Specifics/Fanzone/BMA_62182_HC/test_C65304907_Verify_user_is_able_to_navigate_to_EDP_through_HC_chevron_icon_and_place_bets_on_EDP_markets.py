import pytest
import tests
import datetime
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304907_Verify_user_is_able_to_navigate_to_EDP_through_HC_chevron_icon_and_place_bets_on_EDP_markets(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C65304907
    NAME: Verify user is able to navigate to EDP through HC chevron icon and place bets on EDP markets
    DESCRIPTION: Verify user is able to navigate to EDP through HC chevron icon and place bets on EDP markets
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True
    bet_amount = 1
    price_num = 1
    price_den = 2
    card_number = tests.settings.visa_card if tests.settings.backend_env != 'prod' else tests.settings.master_card
    card_type = 'visa' if tests.settings.backend_env != 'prod' else 'mastercard'
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        carousels = self.cms_config.get_fanzone_highlight_carousels()
        if tests.settings.backend_env != 'prod':
            if not carousels:
                self.ob_config.create_fanzone_league_event_id(
                    league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                    home_team=vec.fanzone.TEAMS_LIST.aston_villa,
                    away_team=vec.fanzone.TEAMS_LIST.manchester_united,
                    home_team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa,
                    away_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_united)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount='20',
                                                                     card_number=self.card_number,
                                                                     card_type=self.card_type,
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True, timeout=10)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        team = teams[vec.fanzone.TEAMS_LIST.aston_villa.title()]
        team.scroll_to_we()
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=40)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=20)
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
        # banner = self.site.home.fanzone_banner(timeout=30)    as per the new change, after subscription, we will be in fanzone page only
        # banner.let_me_see.click()
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                                 name='Fanzone page not displayed')
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

    def test_003_verify_user_is_able_to_see_events_in_highlight_carousel_format(self):
        """
        DESCRIPTION: Verify user is able to see Events in "Highlight Carousel" format
        EXPECTED: User should be able to see "Events" in Highlight carousel format
        """
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        self.__class__.events = carousel.items_as_ordered_dict
        self.assertTrue(self.events, msg="Events are not found under Now and Next tab")

    def test_004_verify_user_is_able_chevron_for_events_in_next_game(self):
        """
        DESCRIPTION: verify user is able chevron for events in Next Game
        EXPECTED: User should be able to Chevron for Events in Now and Next tab
        """
        if self.device_type == 'mobile':
            for event in list(self.events.values()):
                self.assertTrue(event.chevron.is_displayed(), msg=f'"Chevron" is not displayed for {event.event_name}')

    def test_005_click_on_the_chevron_icon_gt_and_verify_user_is_navigate_to_edp(self):
        """
        DESCRIPTION: Click on the Chevron Icon '&gt;' and verify user is navigate to EDP
        EXPECTED: User should be navigated to Events EDP page
        """
        event = list(self.events.values())[0]
        if self.device_type == 'mobile':
            event.chevron.click()
        else:
            event.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_006_click_on_any_odd_for_the_event_user_wants_to_place_bet(self):
        """
        DESCRIPTION: Click on any odd for the event user wants to place bet
        EXPECTED: Odd should be shown selected for quick bet
        """
        selection_button = self.get_selection_bet_button(selection_name=vec.fanzone.TEAMS_LIST.aston_villa, market_name=None)
        selection_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')

    def test_007_enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: Enter stake and Click on Place bet
        EXPECTED: User should be place bet successfully
        """
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()
        else:
            self.site.open_betslip()
            self.place_and_validate_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
