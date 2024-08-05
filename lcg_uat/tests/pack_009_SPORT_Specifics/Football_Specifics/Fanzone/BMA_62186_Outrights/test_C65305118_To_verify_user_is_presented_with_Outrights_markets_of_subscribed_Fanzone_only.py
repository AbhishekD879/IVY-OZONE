import pytest
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2 # Not configured in tst2
# @pytest.mark.lad_prod # Can not create outright events in PROD
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305118_To_verify_user_is_presented_with_Outrights_markets_of_subscribed_Fanzone_only(Common):
    """
    TR_ID: C65305118
    NAME: To verify user is presented with Outrights markets of subscribed Fanzone only
    DESCRIPTION: To verify user is presented with Outrights markets of subscribed Fanzone only
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) User is in Fanzone page Now and Next Tab
    """
    keep_browser_open = True

    def login_select_fanzone(self, fanzone_team):
        if fanzone_team in "manchester_city":
            fanzone_team = vec.fanzone.TEAMS_LIST.manchester_city.title()
        elif fanzone_team in "manchester_united":
            fanzone_team = vec.fanzone.TEAMS_LIST.manchester_united.title()
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(fanzone_team, str(typeId))
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page(name='sport/football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(fanzone_team)
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 5) User has subscribed to Fanzone
        PRECONDITIONS: 6) User is navigated to Fanzone page
        """
        self.site.wait_content_state('Home')
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = event.ss_response['event']['name'].upper()
        self.__class__.market_name = event.ss_response['event']['children'][0]['market']['templateMarketName']
        self.__class__.selection_name, selection_id = list(event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.manchester_city,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city)
        self.login_select_fanzone(fanzone_team="manchester_city")

    def test_001_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outright.items_as_ordered_dict.get(self.market_name)
        events = market.items_as_ordered_dict
        self.assertIn(self.selection_name, list(events),
                      msg=f'Expected event "{self.selection_name}" is not found in actual events "{list(events)}"')

    def test_002_now_logout_from_the_application(self):
        """
        DESCRIPTION: Now logout from the application
        EXPECTED: User should be able to logout from application successfully
        """
        self.site.logout()

    def test_003_now_login_to_application_with_a_user_having_other_team_fanzone(self):
        """
        DESCRIPTION: Now login to application with a user having other Team fanzone
        EXPECTED: User should be able to login to application successfully
        """
        self.login_select_fanzone(fanzone_team="manchester_united")

    def test_004_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page
        EXPECTED: User should be on respective Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_005_verify_if_the_outright_markets_created_for_other_fanzone_team_is_shown_in_team_bets(self):
        """
        DESCRIPTION: Verify if the outright markets created for Other Fanzone team is shown in Team bets
        EXPECTED: User should not be able to see Outright markets in Fanzone page as the outright markets were created for other team
        """
        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        self.assertIsNone(outright,
                          msg=f'Expected event "{self.event_name}" is found in actual events')
