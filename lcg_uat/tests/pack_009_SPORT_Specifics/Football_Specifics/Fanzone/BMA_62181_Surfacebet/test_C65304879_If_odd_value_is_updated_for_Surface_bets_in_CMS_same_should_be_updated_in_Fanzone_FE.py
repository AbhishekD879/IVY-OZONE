import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # Cannot update odd value for surface bet in prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304879_If_odd_value_is_updated_for_Surface_bets_in_CMS_same_should_be_updated_in_Fanzone_FE(Common):
    """
    TR_ID: C65304879
    NAME: If odd value is updated for Surface bets in CMS same should be updated in Fanzone FE
    DESCRIPTION: To verify user should be able to change the odds values in Surface bet which are mapped to Fanzone then updated odds values should be displayed in respective surface bet
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Surface bets are created with with below data:
    PRECONDITIONS: 1)Offer content 2)Dynamic price button 3)was price, making it fanzone inclusion in CMS
    PRECONDITIONS: 4)User has logged into application and navigated to Fanzone page
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2
    new_price_num = 1
    new_price_dec = 3
    selection_price = '4/5'

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id = event.selection_ids[event.team1]

        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=self.selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.burnley.title()].click()
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
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu, msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')

    def test_002_verify_if_the_surface_bets_are_shown_in_now_and_next_tab(self):
        """
        DESCRIPTION: verify if the surface bets are shown in Now and Next tab
        EXPECTED: User should be able to see surface bets in Now and Next tab
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        self.__class__.surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(self.surface_bet_name, surface_bets, msg=f'Created surface bet "{self.surface_bet_name}" is not present in "{surface_bets}"')

    def test_003_now_login_to_cms_and_update_the_price_of_the_surface_bets_created_for_fanzone_page_for_the_particular_team(self):
        """
        DESCRIPTION: Now login to CMS and update the price of the surface bets created for Fanzone page for the particular team
        EXPECTED: User should be able to update the price in CMS for the surface bets
        """
        id = self.surface_bet['id']
        self.cms_config.update_surface_bet(surface_bet_id=id, priceNum=self.new_price_num, priceDen=self.new_price_dec)
        self.ob_config.change_price(selection_id=self.selection_id, price=self.selection_price)

    def test_004_navigate_to_fanzone_fe_and_verify_the_surface_bets(self):
        """
        DESCRIPTION: Navigate to Fanzone fe and verify the surface bets
        EXPECTED: Price should be updated for respective surface bets in FE
        """
        self.device.refresh_page()
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict[self.surface_bet_name]
        self.assertTrue(surface_bet, msg='No surface bets found')
        was_price = surface_bet.old_price.value
        expected_was_price = f'{self.new_price_num}' + '/' + f'{self.new_price_dec}'
        self.assertEqual(was_price, expected_was_price, msg=f'Actual was price "{was_price}" is not same as Expected was price "{expected_was_price}"')
        new_price = surface_bet.bet_button.name
        self.assertEqual(new_price, self.selection_price, msg=f'Actual price "{new_price}" is not same as Expected price "{self.selection_price}"')
