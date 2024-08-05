import pytest
import tests
import datetime
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304899_Verify_user_is_able_to_navigate_to_EDP_through_HC_chevron_icon_and_place_bets_on_EDP_markets(Common):
    """
    TR_ID: C65304899
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
    card_number = 4506620004077430 if tests.settings.backend_env != 'prod' else 5137651100600001
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
        banner = self.site.home.fanzone_banner(timeout=30)
        banner.let_me_see.click()
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                                 name='Fanzone page not displayed')
        self.assertTrue(result, msg='fanzone page not loaded')

    def test_002_verify_user_is_able_to_see_events_in_highlight_carousel_format(self):
        """
        DESCRIPTION: Verify user is able to see Events in "Highlight Carousel" format
        EXPECTED: User should be able to see "Events" in Highlight carousel format
        """
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        self.__class__.events = carousel.items_as_ordered_dict
        self.assertTrue(self.events, msg="Events are not found under Now and Next tab")

    def test_003_click_on_chevron_icon_gt(self):
        """
        DESCRIPTION: Click on Chevron Icon '&gt;'
        EXPECTED: User should be navigated to EDP
        """
        event = list(self.events.values())[0]
        if self.device_type == 'mobile':
            event.chevron.click()
        else:
            event.click()
        self.site.wait_content_state(state_name='EventDetails')
