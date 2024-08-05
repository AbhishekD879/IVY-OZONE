import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from crlat_ob_client.create_event import CreateSportEvent


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305130_To_Win_Eachway_markets_are_shown_in_Now_and_Next_tab(Common):
    """
    TR_ID: C65305130
    NAME: To Win-Eachway markets are shown in Now and Next tab
    DESCRIPTION: To verify created To Win-Eachway market is shown in Now and Next tab under (Teams)Bet in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)To Win-Eachway markets is created in OB for that type or competition
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa
    new_market_name = "To Win Eachway"

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3) Top Goal Scorer market is created in OB for that type or competition
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(self.teamname.title(), str(typeId))
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        self.__class__.market_template_id = outright_event.ss_response['event']['children'][0]['market'][
            'templateMarketId']
        selection_name, selection_id = list(outright_event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=self.teamname,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=type_id)
        event.update_market_settings(market_id=outright_event.default_market_id, event_id=outright_event.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True, timeout=10)
        self.site.wait_content_state("football", timeout=10)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)

        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        # covered in above step

    def test_002_now_navigate_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Now navigate Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User should be navigated to Homepage /Football slp/A-Z menu/Sports ribbon
        """
        # covered in above step

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

    def test_004_verify_is_user_is_able_to_see_to_win_eachway_market_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify is user is able to see To Win-Eachway market in Now and next Tab
        EXPECTED: User should be able to see To Win-Eachway market under (Team)bet label in Now and Next tab
        """
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        markets_list = outrights.items_as_ordered_dict
        self.assertIn(self.new_market_name, markets_list,
                      msg=f'Market "{self.new_market_name}" is not in the market list')
