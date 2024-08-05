import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create event on Market level with BOG icon
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C47660499_Verify_BOG_icon_on_Bet_Receipt(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C47660499
    NAME: Verify BOG icon on Bet Receipt
    DESCRIPTION: This test case verifies that the BOG icon is displayed on the Bet Receipt and My Bets section
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has a positive balance
    PRECONDITIONS: * BOG has been enabled in CMS
    PRECONDITIONS: * 'GP available' checkbox is selected for the event in TI tool on the market level
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '1/3', 2: '2/3', 3: '2/7', 4: '1/9'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
        PRECONDITIONS: * User is logged in and has a positive balance
        PRECONDITIONS: * BOG has been enabled in CMS
        PRECONDITIONS: * 'GP available' checkbox is selected for the event in TI tool on the market level
        """
        bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']

        if not bog_toggle:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
        self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')

        event = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.eventID = event.event_id
        self.__class__.selection_id1 = list(event.selection_ids.values())[0]

        event2 = self.ob_config.add_UK_racing_event(gp=False, lp_prices=self.prices)
        self.__class__.eventID2 = event2.event_id
        self.__class__.selection_id2 = list(event2.selection_ids.values())[0]

        event3 = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.eventID3 = event3.event_id
        self.__class__.selection_id3 = list(event3.selection_ids.values())[0]

        event4 = self.ob_config.add_UK_racing_event(gp=True, lp_prices=self.prices)
        self.__class__.eventID4 = event4.event_id
        self.__class__.selection_id4 = list(event4.selection_ids.values())[0]

        self.site.login()

    def test_001_add_selection_with_available_bog_icon_to_betslipquickbet(self):
        """
        DESCRIPTION: Add selection with available BOG icon to Betslip/Quickbet
        EXPECTED: Selection is added to the BetSlip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id1)

    def test_002_enter_a_value_in_the_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter a value in the 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_bog_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'BOG' icon on the Bet Receipt
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        self.assertTrue(first_section.has_promo_icon, msg='BOG icon is not present on betreceipt')

    def test_004_add_selection_without_bog_icon_available_to_betslipquickbet_for_mobile_and_place_bet(self):
        """
        DESCRIPTION: Add selection without 'BOG' icon available to Betslip/Quickbet (for mobile) and place bet
        EXPECTED: There is NO 'BOG' icon displayed on Betslip/Quickbet (for mobile)
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id2)
        betslip_sections = self.get_betslip_content().betslip_sections_list
        self.assertTrue(betslip_sections, msg='No BetReceipt sections found')
        first_section = list(betslip_sections.values())[0]
        self.assertFalse(first_section.has_promo_icon(expected_result=False), msg='BOG icon is present on '
                                                                                  'betslip')

    def test_005_add_a_couple_of_hourse_selection_with_bog_icon_to_betslipquickbet(self):
        """
        DESCRIPTION: Add a couple of <Hourse> selection with BOG icon to Betslip/Quickbet
        EXPECTED: * <Hourse> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id3, self.selection_id4])

    def test_006_enter_a_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter a value in 'Stake' field for one of Multiple bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()

    def test_007_verify_bog_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'BOG' icon on the Bet Receipt
        EXPECTED: 'BOG' icon is displayed under EACH selection (under market name/event name section)
        """
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='Bet receipt sections not found')
        receipts = receipt_sections['Double'].items_as_ordered_dict
        self.assertTrue(receipts, msg='Receipts not found in bet receipt section')
        first_section = list(receipts.values())[0]
        self.assertTrue(first_section.has_promo_icon, msg='Failed to display "BOG" icon')
        second_section = list(receipts.values())[1]
        self.assertTrue(second_section.has_promo_icon, msg='Failed to display "BOG" icon')
