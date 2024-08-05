import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
import random
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.navigation
@pytest.mark.adhoc_suite
@pytest.mark.trending_bets
@pytest.mark.other
@vtest
class Test_C65972741_Verify_the_Display_of_popular_bets_carousel_in_Bet_Receipt_page_for_Non_football_selection_bets(
    BaseBetSlipTest):
    """
    TR_ID: C65972741
    NAME: Verify the Display of popular bets carousel in Bet Receipt page for Non football selection bets
    DESCRIPTION: This testcase is to verifies the Display of popular bets carousel in Bet Receipt page for Non football selection bets
    PRECONDITIONS: Should have non football events
    PRECONDITIONS: Should able to placebet
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    line_name = 'Line 1'
    result=[]

    def generate_random_numbers(self):
        """
        DESCRIPTION :Generate 5 unique random numbers between 1 and 49
        """
        # Generate 5 unique random numbers between 1 and 49
        random_numbers = random.sample(range(1, 50), 5)
        return random_numbers

    def test_000_preconditions(self):
        """preconditions"""
        trending_carousel_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_betslip:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)
        trending_carousel_betreceipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get(
            'active')
        if not trending_carousel_betreceipt:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(active=True)

        events = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id, number_of_events=2)
        all_selection_ids = []
        for event in events:
            market = next((market for market in event['event']['children'] if market['market'].get('children') and int(market['market'].get('maxAccumulators'))>1), None)
            if market:
                outcomes_resp = market['market']['children']
                filtered_outcomes = [i for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']]
                if len(filtered_outcomes) >= 2:
                    selection_ids = [outcome['outcome']['id'] for outcome in filtered_outcomes]
                    if len(all_selection_ids) == 0:
                        self.__class__.selection_id = selection_ids[0]
                    elif len(all_selection_ids) >= 1:
                        self.__class__.selection_id1 = selection_ids[1]
                    all_selection_ids.extend(selection_ids)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.login()

    def test_002_click_on_the_any_sport_other_than_football(self):
        """
        DESCRIPTION: Click on the any Sport other than football
        EXPECTED: Able to navigate to the sports landing page
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')

    def test_003_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any Selection
        EXPECTED: Single Selection is added to Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.site.close_betslip()


    def test_004_add_more_than_1_selection_to_betslip(self):
        """
        DESCRIPTION: Add more than 1 selection to betslip
        EXPECTED: Should able to add selections to betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id1)

    def test_005_place_bet_in_betslip(self):
        """
        DESCRIPTION: Place bet in betslip
        EXPECTED: Should able to place bet and betreceipt should be loaded
        """
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False),
                         msg=f'betslip has trending_bet carousel which should not be available')
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_006_verify_betreceipt(self):
        """
        DESCRIPTION: Verify betreceipt
        EXPECTED: Popular bets carousel should not display in bet receipt page
        """
        self.assertFalse(self.site.bet_receipt.has_trending_bet_carousel(),
                         msg=f'bet receipt has trending bet carousel which shouldnt be available')

    def test_007_place_a_bet_from_virtuals_and_verify_the_betreceipt(self):
        """
        DESCRIPTION: Place a bet from virtuals and verify the betreceipt
        EXPECTED: Popular bets carousel should not display in bet receipt page
        """
        self.navigate_to_page('/')
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() == "TOP SPORTS"), None)
            wait_for_result(lambda: virtual_section, bypass_exceptions=VoltronException)
            list(virtual_section.items_as_ordered_dict.values())[0].click()
        virtual_sports_list = self.site.virtual_sports
        open_tab = virtual_sports_list.sport_carousel.open_tab('Greyhounds')
        wait_for_result(lambda: open_tab, bypass_exceptions=VoltronException)
        wait_for_haul(5)
        sections = self.site.virtual_sports.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        runner_button_1 = list(sections.values())[0]
        runner_button_1.bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip(timeout=3)
        self.site.open_betslip()
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False),
                         msg=f'betslip has trending_bet carousel which shouldnt be available')
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.assertFalse(self.site.bet_receipt.has_trending_bet_carousel(),
                         msg=f'bet receipt has trending bet carousel which shouldnt be available')

    def test_008_place_a_bet_from_fan_prize_selection_and_verify_the_betreceipt(self):
        """
        DESCRIPTION: Place a bet from fan prize selection and verify the betreceipt
        EXPECTED: Popular bets carousel should not display in bet receipt page
        """
        #can not be automatable as fan price is configured before the match day.

    def test_009_place_a_bet_from_pools_and_verify_the_betreceipt(self):
        """
        DESCRIPTION: Place a bet from pools and verify the betreceipt
        EXPECTED: Popular bets carousel should not display in bet receipt page
        """
        #no events in pools

    def test_010_place_a_bet_from_lottos_and_verify_the_betreceipt(self):
        """
        DESCRIPTION: Place a bet from Lottos and verify the betreceipt
        EXPECTED: Popular bets carousel should not display in bet receipt page
        """

        self.navigate_to_page('/')
        sport_categories = self.cms_config.get_sport_categories()
        for sport_category in sport_categories:
            if sport_category.get('imageTitle') == "Lotto" and sport_category.get('disabled') == True:
                raise CmsClientException('"LOTTO" Page is not configured')
        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')
        # clicking on choose numbers button
        self.assertTrue(self.site.lotto.tab_content.choose_numbers.is_displayed(),
                        msg='choose numbers button is not present in lotto page')
        self.site.lotto.tab_content.choose_numbers.click()
        # verifying whether select number dialogue popup is visible or not in lotto page
        dialog_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=5)
        self.assertIsNotNone(dialog_popup, msg='Dialogue popup is not opened')
        #  generating random numbers to select numbers in select numbers dialogue page
        lotto_numbers = sorted(self.generate_random_numbers())
        self.__class__.lotto_numbers_str = [str(element) for element in lotto_numbers]
        # getting ui numbers from select numbers dialogue page
        ui_lotto_numbers = dialog_popup.number_selectors_ordered_dict
        # selecting random five numbers in select number dialogue page
        for lotto_number in self.lotto_numbers_str:
            ui_lotto_numbers.get(lotto_number).click()
        # checking whether add line button is visible or not in select numbers dialogue page
        self.assertTrue(dialog_popup.done_button.is_displayed(),
                        msg='add line button is not visible in select numbers dialogue')
        dialog_popup.done_button.click()
        # checking whether user is able to navigate "line summary" page
        current_url = self.device.get_current_url()
        self.assertIn("linesummary", current_url, msg='Not able to navigate to line summary page')
        # verifying "selection numbers" which user added from "choose number selection" dialogue popup page
        actual_selected_numbers = self.site.lotto.line_summary.line_section.items_as_ordered_dict.get(
            self.line_name).selected_numbers
        self.assertListEqual(actual_selected_numbers, self.lotto_numbers_str,
                             msg=f'Actual numbers from FE : {actual_selected_numbers} is not same expected numbers:{self.lotto_numbers_str}')
        # verifying lucky buttons are available under "Choose Your Draws"
        choose_your_draws = self.site.lotto.line_summary.choose_your_draws_section.items_as_ordered_dict
        length_choose_your_draws = len(choose_your_draws)
        if length_choose_your_draws > 0:
            date_name = random.sample(list(choose_your_draws), 1)[0]
            time_draw = choose_your_draws[date_name].items_as_ordered_dict
            time_draw_name = random.sample(list(time_draw), 1)[0]
            words = (time_draw_name.split())[:-1]
            self.__class__.draw_name = ' '.join(word.capitalize() for word in words)
            self.__class__.expected_day_and_time = f'{date_name} - {time_draw_name.split()[-1]}'
            time_draw[time_draw_name].click()
        else:
            raise SiteServeException('Draw buttons are not available under "choose your draws"')
        # verifying week buttons are available under "How Many Weeks"
        weeks = self.site.lotto.line_summary.how_many_weeks_section.week_selections_items
        length_weeks = len(weeks)
        if length_weeks > 0:
            weeks['1'].click()
        else:
            raise SiteServeException('week buttons are not available under "How Many Weeks"')
        self.assertTrue(self.site.lotto.line_summary.add_to_betslip.is_displayed(),
                        msg='add To Betslip is not visible in Line Summary Page')
        self.site.lotto.line_summary.add_to_betslip.click()
        lottery_name = "49's 6 Ball Draw" if self.brand == "bma" else "49's 6 Ball"
        # Common verification logic for both draws
        self.assertTrue(self.site.has_betslip_opened(), msg="Betslip is not opened")
        lotto_bestslip_name = self.site.lotto_betslip
        numbers = ' '.join(item for item in self.lotto_numbers_str)
        lotto_bet = lotto_bestslip_name.betslip_sections_list.items_as_ordered_dict.get(
            f"{lottery_name}-{self.draw_name}-{self.expected_day_and_time}-{numbers}"
        )
        lotto_bet.amount_form.input.click()
        keyboard = lotto_bestslip_name.keyboard
        keyboard.enter_amount_using_keyboard(value=0.1)
        lotto_bestslip_name.bet_now_button.click()
        self.assertFalse(self.site.lotto_bet_receipt.has_trending_bet_carousel(expected_result=False),
                          msg=f'betslip has trending_bet carousel which should not be available')



