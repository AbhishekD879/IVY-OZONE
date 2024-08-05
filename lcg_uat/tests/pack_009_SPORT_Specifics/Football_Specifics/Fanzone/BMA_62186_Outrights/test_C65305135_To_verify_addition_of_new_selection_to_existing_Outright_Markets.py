import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # Cannot add new selection to outright in prod/beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305135_To_verify_addition_of_new_selection_to_existing_Outright_Markets(Common):
    """
    TR_ID: C65305135
    NAME: To verify addition of new selection to existing Outright Markets
    DESCRIPTION: To verify addition of new selection to existing Outright Markets
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) User is navigated to Fanzone page
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa.title()

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
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), str(typeId))
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = self.event.ss_response['event']['name'].upper()
        self.__class__.market_name = self.event.ss_response['event']['children'][0]['market']['templateMarketName']
        self.__class__.selection_name, selection_id = list(self.event.selection_ids.items())[0]
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
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname)
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.aston_villa,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)

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
        market = outright.accordions_list.items_as_ordered_dict.get(self.market_name)
        events = market.items_as_ordered_dict
        self.assertIn(self.selection_name, list(events),
                      msg=f'Expected event "{self.selection_name}" is not found in actual events "{list(events)}"')

    def test_002_login_to_open_bet__outrights_markets_and_add_new_selection_to_outright_market(self):
        """
        DESCRIPTION: Login to Open Bet--Outrights markets and add new selection to Outright market
        EXPECTED: Should be able to add new selection to outright market in Open Bet
        """
        self.__class__.selection_name2, selection_id2 = list(self.event.selection_ids.items())[1]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id2,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.aston_villa,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)

    def test_003_navigate_to_fanzone_page_in_front_end_and_verify_newly_added_selection_is_populated_in_the_outright_market(self):
        """
        DESCRIPTION: Navigate to Fanzone page in front end and verify newly added selection is populated in the outright market
        EXPECTED: Newly added selection should be populated in Outrigt Market
        """
        self.device.refresh_page()
        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outright.accordions_list.items_as_ordered_dict.get(self.market_name)
        events = market.items_as_ordered_dict
        self.assertIn(self.selection_name2, list(events),
                      msg=f'Expected event "{self.selection_name2}" is not found in actual events "{list(events)}"')
