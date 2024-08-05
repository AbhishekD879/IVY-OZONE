import pytest
import tests
from time import sleep
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from crlat_ob_client.create_event import CreateSportEvent


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2     # Not configured in tst2
# @pytest.mark.lad_prod     # not configured in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305115_To_verify_accordians_of_Outright_markets_are_in_open_state_for_all_the_markets(Common):
    """
    TR_ID: C65305115
    NAME: To verify accordians of Outright markets are in open state for all the markets
    DESCRIPTION: To verify accordians of Outright markets are in open state for all the markets
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.burnley
    new_market_name = "Top 6"

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 5) User has subscribed to Fanzone
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(self.teamname.title())
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        self.__class__.market_template_id = outright_event.ss_response['event']['children'][0]['market']['templateMarketId']
        selection_name, selection_id = list(outright_event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=self.teamname,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=type_id)
        event.update_market_settings(market_id=outright_event.default_market_id, event_id=outright_event.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_navigate_to_fanzone_page_via_below_entry_pointsa_launch_banner_in_home_pageb_fanzone_in_sports_ribbonc_fanzone_in_a_zall_sports_menud_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page via below entry points
        DESCRIPTION: a. Launch Banner in home page
        DESCRIPTION: b. Fanzone in Sports Ribbon
        DESCRIPTION: c. Fanzone in A-Z(All sports) menu
        DESCRIPTION: d. Launch Banner in Football landing page
        EXPECTED: User should be able to navigate Fanzone page
        """
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

    def test_003_verify_is_user_is_able_to_see_outright_market_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify is user is able to see Outright Market in Now and next Tab
        EXPECTED: User should be able to see Outright market under &lt;Team&gt; Bets section in Now and Next tab
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_004_verify_all_accordians_are_open_by_default_for_all_the_available_markets(self):
        """
        DESCRIPTION: Verify all accordians are open by default for all the available markets
        EXPECTED: All accordians should be open by default for all the available markets
        """
        outrights = list(self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        list_market = list(outrights.accordions_list.items_as_ordered_dict.values())
        list_market[0].is_expanded()
