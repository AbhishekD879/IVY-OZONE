import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C29129_Pending_review_on_Mobile(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C29129
    NAME: Pending review on Mobile
    DESCRIPTION:
    PRECONDITIONS: 1. User is logged in to application on mobile device
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: How to enable overask: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    """
    keep_browser_open = True
    max_bet = None
    stake_part1 = 1.50
    price_part1 = 1.50
    stake_part2 = 0.50
    price_part2 = 0.50

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and login
        EXPECTED: Events are created and user is logged In
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)

        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id_1 = list(selection_ids.values())[0]

        event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID_2 = event_params_2.event_id
        self.__class__.expected_market = event_params_2.ss_response['event']['children'][0]['market']['name']

        self.site.login()

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id_1)

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        # Covered in step-3

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background anchored to the footer
        EXPECTED: *   Loading spinner is shown on the green button, replacing 'BET NOW' label
        EXPECTED: *   'Clear Betslip' and 'BET NOW' buttons become disable
        EXPECTED: *   'Stake' field becomes disable
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        self.__class__.bet_amount = self.max_bet + 0.10
        self.place_single_bet(number_of_stakes=1)

        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')
        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

    def test_004_while_review_is_pending_tap_disabled_clear_betslip_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Clear Betslip' button
        EXPECTED: Nothing happens, it is impossible to clear betslip
        """
        # not valid step from OX 99

    def test_005_while_review_is_pending_tap_disabled_bet_now_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Bet Now' button
        EXPECTED: Nothing happens, it is impossible to place a Bet
        """
        # not valid step from OX 99

    def test_006_while_review_is_pending_tap_disabled_stake_field(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Stake' field
        EXPECTED: Nothing happens, it is impossible to modify entered Stake
        """
        # Can not be automate

    def test_007_while_review_is_pending_go_to_another_pages_and_try_to_add_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: While review is pending go to another pages and try to add more selections to the Betslip
        EXPECTED: *   New selections cannot be added
        EXPECTED: *   After trying to add selection user is navigated to Betslip with bet in review automatically
        """
        self.navigate_to_edp(event_id=self.eventID_2, timeout=40)
        self.site.wait_content_state(state_name='EventDetails', timeout=5)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        market = self.expected_market if self.brand == 'ladbrokes' else self.expected_market.upper()
        section = markets_list.get(market)
        self.assertTrue(section, msg='Match result section is not found')
        prices = section.outcomes.items_as_ordered_dict
        self.assertTrue(prices, 'No one bet price was found')
        self.__class__.outputprice = list(prices.values())[0].output_price
        list(prices.values())[0].bet_button.click()

        self.site.add_first_selection_from_quick_bet_to_betslip()

        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')

        self.verify_betslip_counter_change(expected_value=1)

    def test_008_try_to_cancel_review_process(self):
        """
        DESCRIPTION: Try to cancel review process.
        EXPECTED: User cannot cancel review process by himself
        """
        self.device.refresh_page()
        self.site.header.bet_slip_counter.click()
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')
