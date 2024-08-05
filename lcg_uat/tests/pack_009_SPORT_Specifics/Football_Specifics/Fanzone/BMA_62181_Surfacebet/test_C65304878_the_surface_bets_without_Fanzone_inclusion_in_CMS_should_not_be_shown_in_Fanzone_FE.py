import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_hl
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304878_The_surface_bets_without_Fanzone_inclusion_in_CMS_should_not_be_shown_in_Fanzone_FE(Common):
    """
    TR_ID: C65304878
    NAME: The surface bets without Fanzone inclusion in CMS should not be shown in Fanzone FE
    DESCRIPTION: To verify if created surface bets in CMS are not mapped to Fanzone in CMS then those surface bets should not be displayed in Fanzone FE
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, without making it fanzone inclusion in CMS
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2

    def test_000_precondition(self):
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            event_type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            event_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(aston_villa)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=event_type_id)
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state(state_name='Football')
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams.get(aston_villa).scroll_to_we()
        teams.get(aston_villa).click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab
        EXPECTED: User should not be able to see surface bets in Now and Next tab as fanzone inclusion is not marked in CMS
        """
        if self.site.fanzone.tab_content.has_surface_bets():
            surface_bet_name = self.surface_bet['title'].upper()
            surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
            self.assertNotIn(surface_bet_name, surface_bets,
                             msg=f'Created surface bet "{surface_bet_name}" is present in "{surface_bets}"')
