import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893063_Verify_the_add_to_bet_slip_functionality_for_MC_user_login_by_selecting_bet_online_from_FCB_popup(BaseBetSlipTest):
    """
    TR_ID: C64893063
    NAME: Verify the add to bet slip functionality for MC user login by selecting bet online from FCB popup.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_mc_user2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4select_bet_online_from_fcb_popup5select_few_filters_and_click_on_find_bets6click_on_add_to_bet_slip_button7open_bet_slip_and_click_on_place_betexpected_result1sports_web_application_should_be_launch2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter4user_should_be_able_to_select_bet_online_from_fcb_popup5user_should_be_able_to_select_few_filters_and_able_to_click_on_find_bets_button6user_should_be_able_to_click_on_add_to_bet_slip_button7user_should_be_able_to_open_bet_slip_and_place_bet_successfully(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid MC user.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the grid hub menu items.
        DESCRIPTION: 4.Select bet online from FCB popup.
        DESCRIPTION: 5.Select few filters and click on find bets
        DESCRIPTION: 6.Click on add to bet slip button.
        DESCRIPTION: 7.Open bet slip and click on place bet.
        EXPECTED: 1. 1.Sports web application should be launch.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter.
        EXPECTED: 4.User should be able to select bet online from FCB popup.
        EXPECTED: 5.User should be able to select few filters and able to click on find bets button.
        EXPECTED: 6.User should be able to click on add to bet slip button.
        EXPECTED: 7.User should be able to open bet slip and place bet successfully.
        """
        self.site.login(tests.settings.mc_user)
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        for section in sections.values():
            filters = section.items_as_ordered_dict
            for filter in filters.values():
                filter.click()
                find_bets_button = self.site.football_bet_filter.find_bets_button
                if find_bets_button.is_enabled() and self.site.football_bet_filter.read_number_of_bets() < 40:
                    find_bets_button.click()
                    self.__class__.flag = True
                    break
                else:
                    filter.click()
            if self.flag:
                break

        self.site.football_bet_filter_results_page.button.click()
        self.assertTrue(self.site.has_betslip_opened(timeout=10), msg='Betslip is not opened')
        betnow_btn = self.get_betslip_content().bet_now_button
        section = list(self.get_betslip_sections().Singles.values())
        section[0].amount_form.enter_amount(value=0.1)
        self.assertTrue(betnow_btn.is_enabled(), msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" '
                                                     f'is not enabled after entering stake')
        betnow_btn.click()
        self.check_bet_receipt_is_displayed()
