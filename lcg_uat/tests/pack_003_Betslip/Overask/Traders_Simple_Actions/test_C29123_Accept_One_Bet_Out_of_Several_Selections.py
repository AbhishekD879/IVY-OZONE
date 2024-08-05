import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Overask cannot be triggered in prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C29123_Accept_One_Bet_Out_of_Several_Selections(BaseBetSlipTest):
    """
    TR_ID: C29123
    NAME: Accept One Bet Out of Several Selections
    DESCRIPTION: This test case verifies accepting of one bet out of several selections by a trader triggered by overask functionality
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: [How to accept/decline/make an Offer with Overask functionality](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955)
    PRECONDITIONS: [How to disable/enable Overask functionality for User or Event Type](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: * Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: * Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: * The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: * The Initial Data response on homepage is absent
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create events
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        self.__class__.max_mult_bet = self.max_bet + 0.1
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|',
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.__class__.expected_user_balance = self.site.header.user_balance

    def test_002_add_a_few_selections_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Singles' section
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1]])

    def test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' fields that does not exceed max allowed bet limit for one of added selections
        EXPECTED: 'Stake' field is populated with value
        """
        if bet_type == 'Single':
            section = self.get_betslip_sections().Singles
        else:
            section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(section.items(), msg='*** No stakes found')

        self.__class__.stake_name1, self.__class__.stake1 = list(section.items())[0]
        if bet_type == 'Single':
            stake_bet_amounts1 = {self.stake_name1: self.max_bet - 0.01}
        else:
            stake_bet_amounts1 = {self.stake_name1: self.max_mult_bet - 0.01}
        self.enter_stake_amount(stake=(self.stake_name1, self.stake1), stake_bet_amounts=stake_bet_amounts1)

    def test_004_leave_at_list_one_stake_field_empty(self):
        """
        DESCRIPTION: Leave at list one 'Stake' field empty
        EXPECTED: 'Stake' field is empty
        """
        # covered in step 3

    def test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for one of added selections and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        if bet_type == 'Single':
            stake_bet_amounts1 = {self.stake_name1: self.max_bet + 0.01}
        else:
            stake_bet_amounts1 = {self.stake_name1: self.max_mult_bet + 0.01}
        sleep(3)
        self.enter_stake_amount(stake=(self.stake_name1, self.stake1), stake_bet_amounts=stake_bet_amounts1)
        sleep(3)
        self.get_betslip_content().bet_now_button.click()

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background above 'Bet now' button
        EXPECTED: *   Loading spinner is displayed on the green button, replacing 'Bet Now' label
        EXPECTED: *   'Stake','Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
        EXPECTED: *   The rest of selections remain at Betslip
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_007_trigger_accepting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger accepting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is accepted in OpenBet
        EXPECTED: *   Confirmation is sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_ids[0])
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.event_ids[0], bet_id=bet_id, betslip_id=betslip_id)

    def test_008_verify_betslip(self, bet_type='Single'):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Accepted in OB system bet is placed successfully with the original amount
        EXPECTED: *   Bet with entered 'Stake' field on step #3 is placed with the original amount
        EXPECTED: *   Bet with empty 'Stake' field is ignored and not placed
        EXPECTED: *   Balance is reduced accordingly
        EXPECTED: *   Placed bets are listed in 'Bet History' and 'My Account' pages
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        EXPECTED: *  Bet is placed successfully with the original amount
        EXPECTED: *  Bet Receipt is displayed for a user
        EXPECTED: *  Balance is reduced accordingly
        EXPECTED: *  Bet is listed in 'Bet History' and 'My Account' pages
        EXPECTED: ![](index.php?/attachments/get/34017) ![](index.php?/attachments/get/34016)
        """
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_enabled(),
                        msg='"Go betting" button isn\'t enabled')
        if bet_type == 'Single':
            self.__class__.expected_user_balance = self.expected_user_balance - (self.max_bet + 0.01)
        else:
            self.__class__.expected_user_balance = self.expected_user_balance - (self.max_mult_bet + 0.01)
        self.verify_user_balance(expected_user_balance=self.expected_user_balance)
        betreceipt_sections = list(self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict)
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        self.assertEqual(len(betreceipt_sections), 1, msg='More than one reciepts are found')
        self.device.refresh_page()
        self.__class__.expected_user_balance = self.site.header.user_balance

    def test_009_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        """
        self.test_002_add_a_few_selections_and_go_betslip_singles_section()

    def test_010_repeat_steps__3_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 3-8 for Multiple bet
        """
        self.test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(bet_type='Double')
        self.test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button(bet_type='Double')
        self.test_006_verify_betslip()
        self.test_007_trigger_accepting_the_bet_by_a_trader_in_openbet_system()
        self.test_008_verify_betslip(bet_type='Double')

    def test_011_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        """
        self.selection_ids.clear()
        self.event_ids.clear()
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=4, forecast=True,
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_012_repeat_steps__3_8_for_forecaststricastsbet(self):
        """
        DESCRIPTION: Repeat steps № 3-8 for Forecasts/Tricasts bet
        EXPECTED:
        """
        self.test_002_add_a_few_selections_and_go_betslip_singles_section()
        self.test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections()
        self.test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button()
        self.test_006_verify_betslip()
        self.test_007_trigger_accepting_the_bet_by_a_trader_in_openbet_system()
        self.test_008_verify_betslip()
