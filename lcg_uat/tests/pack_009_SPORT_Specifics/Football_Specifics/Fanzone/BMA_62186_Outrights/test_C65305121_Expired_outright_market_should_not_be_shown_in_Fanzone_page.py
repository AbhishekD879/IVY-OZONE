import tests
import pytest
from crlat_ob_client.create_event import CreateSportEvent
from voltron.environments import constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2  # Not configured in tst2
# @pytest.mark.lad_prod  # we cannot create events in prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305121_Expired_outright_market_should_not_be_shown_in_Fanzone_page(Common):
    """
    TR_ID: C65305121
    NAME: Expired outright market should not be shown in Fanzone page
    DESCRIPTION: To verify expired Outright markets should not be displayed in Fanzone page under Now and Next tab
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) User is navigated to Fanzone page
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa
    new_market_name = "Top Outright"

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Create Outright market
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        outright_event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.eventid = outright_event.event_id
        self.__class__.event_name = outright_event.ss_response['event']['name'].upper()
        self.__class__.market_template_id = outright_event.ss_response['event']['children'][0]['market']['templateMarketId']
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
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.teamname.title())
        team.click()
        sleep(4)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        self.navigate_to_page('/fanzone/sport-football/' + self.teamname.title().replace(' ', '') + '/now-next',
                              fanzone=True)
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        markets_list = list(outrights.accordions_list.items_as_ordered_dict)
        self.assertIn(self.new_market_name, markets_list,
                      msg=f'Market "{self.new_market_name}" is not in the market list')

    def test_002_after_outright_events_are_expired_verify_if_those_outright_markets_are_shown_in_fe(self):
        """
        DESCRIPTION: After outright events are expired verify if those outright markets are shown in FE
        EXPECTED: User should not be able to see the expired Outright markets in FE in Fanzone page
        """
        self.ob_config.change_event_state(event_id=self.eventid, displayed=False, active=False)
        sleep(4)
        self.device.refresh_page()
        try:
            outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
            markets_list = list(outrights.accordions_list.items_as_ordered_dict)
            self.assertNotIn(self.new_market_name, markets_list,
                             msg=f'Market "{self.new_market_name}" is not in the market list')
        except Exception:
            self._logger.info("No outrights found")
