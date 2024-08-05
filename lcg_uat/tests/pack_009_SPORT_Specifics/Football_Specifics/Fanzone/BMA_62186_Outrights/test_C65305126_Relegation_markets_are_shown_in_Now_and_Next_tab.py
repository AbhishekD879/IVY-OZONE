import time
import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.Common import Common
from crlat_ob_client.create_event import CreateSportEvent


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2 # Not configured in tst2
# @pytest.mark.lad_prod # Can not create outright events in PROD
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305126_Relegation_markets_are_shown_in_Now_and_Next_tab(Common):
    """
    TR_ID: C65305126
    NAME: Relegation markets are shown in Now and Next tab
    DESCRIPTION: To verify created Relegation market is shown in Now and Next tab under (Teams)Bet in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Relegation market is created in OB for that type or competition
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2
    teamname = vec.fanzone.TEAMS_LIST.aston_villa.title()
    new_market_name = "Relegation"

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create outright event
        """
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(self.teamname.title(), str(typeId))
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        market_template_id = outright_event.ss_response['event']['children'][0]['market']['templateMarketId']
        selection_name, selection_id = list(outright_event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=self.teamname,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=type_id)
        event.update_market_settings(market_id=outright_event.default_market_id, event_id=outright_event.event_id,
                                     market_template_id=market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(self.teamname)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=type_id)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_now_navigate_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Now navigate Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User should be navigated to Homepage /Football slp/A-Z menu/Sports ribbon
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[self.teamname].scroll_to_we()
        teams[self.teamname].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10,
                        name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        time.sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_003_click_on_fanzone_labelfanzone_launch_banner(self):
        """
        DESCRIPTION: Click on Fanzone label/Fanzone launch banner
        EXPECTED: User should be on Fanzone page
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_verify_is_user_is_able_to_see_relegation_market_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify is user is able to see Relegation Market in Now and next Tab
        EXPECTED: User should be able to see Relegation market under (Team)bet label in Now and Next tab
        """
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        markets_list = list(outrights.accordions_list.items_as_ordered_dict)[0].split()[0]
        self.assertIn(self.new_market_name, markets_list,
                      msg=f'Market "{self.new_market_name}" is not in the market list')
