import pytest
import tests
from faker import Faker
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.helpers import string_generator


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893062_Verify_the_registration_journey_from_bet_slip_after_selecting_bet_online_from_FCB_popup_and_added_selections_to_the_bet_slip(BaseBetSlipTest):
    """
    TR_ID: C64893062
    NAME: Verify the registration journey from bet slip after selecting bet online from FCB popup and added selections to the bet slip.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4select_bet_online_from_fcb_popup5select_few_filters_and_click_on_find_bets6click_on_add_to_bet_slip_button7open_bet_slip_and_click_on_login_to_place_bet_button8click_on_registration_button_and_add_funds9click_on_place_bet_button_from_bet_slip_tabexpected_result1sports_web_application_should_be_launch2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter4user_should_be_able_to_select_bet_online_from_fcb_popup5user_should_be_able_to_select_few_filters_and_able_to_click_on_find_bets_button6user_should_be_able_to_click_on_add_to_bet_slip_button7user_should_see_login_over_lay8user_should_give_valid_details_and_complete_user_registration_successfully_and_add_funds_with_the_sample_credit_cards9user_should_get_a_bet_receipt_number_on_successfully_placed(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Select bet online from FCB popup.
        DESCRIPTION: 5.Select few filters and click on find bets.
        DESCRIPTION: 6.Click on add to bet slip button.
        DESCRIPTION: 7.open bet slip and click on "login to place bet" button.
        DESCRIPTION: 8.Click on registration button and add funds.
        DESCRIPTION: 9.Click on place bet button from bet slip tab.
        EXPECTED: 1. 1.Sports web application should be launch.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter.
        EXPECTED: 4.User should be able to select bet online from FCB popup.
        EXPECTED: 5.User should be able to select few filters and able to click on find bets button.
        EXPECTED: 6.User should be able to click on add to bet slip button.
        EXPECTED: 7.User should see login over lay.
        EXPECTED: 8.User should give valid details and complete user registration successfully and add funds with the sample credit cards.
        EXPECTED: 9.User should get a bet receipt number on successfully placed.
        """
        self.site.wait_content_state('homepage')
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
        self.assertEqual(betnow_btn.name, vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Actual button name "{betnow_btn.name}" is not same as '
                             f'Expected button name "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        section = list(self.get_betslip_sections().Singles.values())
        section[0].amount_form.enter_amount(value=0.1)
        self.assertTrue(betnow_btn.is_enabled(), msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" '
                                                     f'is not enabled after entering stake')
        betnow_btn.click()
        self.site._wait_for_login_dialog(timeout=10)
        username = self.generate_user()
        self.site.login_dialog.create_an_account.click()
        if self.site.login_dialog.create_an_account.is_displayed():
            self.site.login_dialog.create_an_account.click()
        username = f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15]
        email = f'test+{username}@internalgvc.com'
        self.site.three_steps_registration.complete_all_registration_steps(social_title='Mr.',
                                                                           first_name=Faker().first_name_female(),
                                                                           last_name=Faker().last_name_female(),
                                                                           birth_date='01-06-1977',
                                                                           country='United Kingdom',
                                                                           post_code='PO16 7GZ',
                                                                           address_one='1 Owen Close',
                                                                           city='Fareham',
                                                                           mobile='+447537152317',
                                                                           email=email,
                                                                           username=username,
                                                                           password=tests.settings.default_password,
                                                                           currency='GBP')
        self.site.set_your_deposit_limits.set_limits()
        self.site.select_deposit_method.close_button.click()
        if self.device_type == 'mobile':
            self.site.wait_content_state('FootballBetFilterPage')
        else:
            self.site.wait_content_state('FootballBetFilterResultsPage')
        self.site.close_all_dialogs(async_close=False, timeout=4)
        self.gvc_wallet_user_client.login(username=username)
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='20',
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard', expiry_month='06',
                                                                     expiry_year='2026',
                                                                     cvv=tests.settings.master_card_cvv)
        if self.device_type == 'mobile':
            self.site.open_betslip()
        else:
            self.device.refresh_page()
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
