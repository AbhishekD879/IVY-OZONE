import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304881_User_should_be_able_to_scroll_Left_Right(Common):
    """
    TR_ID: C65304881
    NAME: User should be able to scroll Left/Right
    DESCRIPTION: To verify user is able to scroll left/right to see all the available surface bets in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = [1, 3]
    price_den = [2, 4]

    def test_000_precondition(self):
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id1 = list(event_selection.values())[0]
            selection_id2 = list(event_selection.values())[1]
            event_type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id1 = event.selection_ids[event.team1]
            selection_id2 = event.selection_ids[event.team2]
            event_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=event_type_id)
        self.__class__.surface_bet1 = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id1,
                                                                              priceNum=self.price_num[0],
                                                                              priceDen=self.price_den[0])

        self.__class__.surface_bet2 = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id2,
                                                                              priceNum=self.price_num[1],
                                                                              priceDen=self.price_den[1])
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()     as per the new change, after subscription, we will be in fanzone page only
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        self.__class__.surface_bet_name1 = self.surface_bet1['title'].upper()
        self.__class__.surface_bet_name2 = self.surface_bet1['title'].upper()
        self.__class__.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(self.surface_bet_name1, self.surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name1}" is not present in "{self.surface_bets}"')
        self.assertIn(self.surface_bet_name2, self.surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name2}" is not present in "{self.surface_bets}"')

    def test_003_verify_user_is_able_to_scroll_leftright_for_the_available_surface_bets(self):
        """
        DESCRIPTION: Verify user is able to scroll left/right for the available surface bets
        EXPECTED: User should be able to scroll left/right for surface bets as Required
        """
        for surface_bet in self.surface_bets.values():
            if surface_bet.name in [self.surface_bet_name1, self.surface_bet_name2]:
                surface_bet.scroll_to()
                self.assertTrue(surface_bet.has_bet_button(), msg=f'Dynamic price button is not present for "{surface_bet.name}"')
                self.assertTrue(surface_bet.content, msg=f'Offer content is not present for "{surface_bet.name}"')
