import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod  # cannot suspend events in prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304877_Expired_surface_bets_should_not_be_displayed(Common):
    """
    TR_ID: C65304877
    NAME: Expired surface bets should not be displayed
    DESCRIPTION: To verify user should not be able to see expired surface bets in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, marking fanzone inclusion in CMS for event which is about to expire
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2

    def test_000_precondition(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event.event_id
        selection_id = event.selection_ids[event.team1]
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
        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)
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
        sleep(2)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(2)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu, msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        self.device.refresh_page()
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        self.__class__.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, self.surface_bets, msg=f'Created surface bet "{surface_bet_name}" is not present in "{self.surface_bets}"')

    def test_003_again_verify_the_surface_bets_in_fanzone_page_once_it_is_expired(self):
        """
        DESCRIPTION: Again verify the surface bets in Fanzone page once it is expired
        EXPECTED: User should not be able to see expired surface bets in Fanzone page
        """
        try:
            self.ob_config.change_event_state(event_id=self.event_id, displayed=False, active=False)
            sleep(3)
            self.device.refresh_page()
            surface_bet_name = self.surface_bet['title'].upper()
            self.__class__.surface_bets_1 = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
            self.assertNotIn(surface_bet_name, self.surface_bets_1, msg=f'Created surface bet "{surface_bet_name}" is not present in "{self.surface_bets}"')
        except VoltronException:
            self._logger.info('****Voltron exception raised as Surface bet is not displayed due to no data****')
