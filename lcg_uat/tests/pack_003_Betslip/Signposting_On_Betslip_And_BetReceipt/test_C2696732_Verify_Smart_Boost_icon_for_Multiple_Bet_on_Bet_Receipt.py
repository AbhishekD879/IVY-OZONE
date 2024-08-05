import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create event on Market level with Smart Boost icon
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2696732_Verify_Smart_Boost_icon_for_Multiple_Bet_on_Bet_Receipt(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2696732
    NAME: Verify Smart Boost icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the Smart Boost icon is displayed for Multiple Bet on the Bet Receipt within BetSlip
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-33500]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Smart Boost promo is available for event on Market level
    PRECONDITIONS: * Smart Boost promo is available for Specials
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION:  Create test events and login
        """
        event = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True,
                                                                          cashout=False)
        self.__class__.selection_id1 = list(event.selection_ids.values())[0]
        self.__class__.eventID = event.event_id

        event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID2 = event2.event_id
        self.__class__.selection_id2 = list(event2.selection_ids.values())[0]

        event3 = self.ob_config.add_autotest_premier_league_football_event(price_boost=True, market_price_boost=True,
                                                                           cashout=False)
        self.__class__.selection_id3 = list(event3.selection_ids.values())[0]
        self.__class__.eventID3 = event3.event_id

        event4 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID4 = event4.event_id
        self.__class__.selection_id4 = list(event4.selection_ids.values())[0]

        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state_changed()

    def test_001_add_few_selections_with_and_without_smart_boost_promo_available_to_betslip(self):
        """
        DESCRIPTION: Add few selections with and without Smart Boost promo available to betslip
        EXPECTED: Selection are added
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])

    def test_002_enter_value_in_stake_field_for_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for Multiple bet and place a bet
        EXPECTED: * Multiple bet is placed
        EXPECTED: * Bet Receipt is displayed
        """
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_smart_boost_icon_on_the_bet_receipt(self, expected_result=True):
        """
        DESCRIPTION: Verify 'Smart Boost' icon on the Bet Receipt
        EXPECTED: * 'Smart Boost' icon is displayed under each selection (under market name/event name section) which has this promo available
        EXPECTED: * If there are some other signposting icons they go in one line one by one (eg. 'Cashout' icon coming first).
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        price_boost_label = self.site.bet_receipt.has_price_boost_label()
        if expected_result:
            self.assertTrue(first_section.has_promo_icon(expected_result=True),
                            msg='Smart Boost icon is not present on betreceipt')
            self.assertTrue(price_boost_label, msg='"Smart Boost" is displayed')
        else:
            self.assertFalse(first_section.has_promo_icon(expected_result=False),
                             msg='Smart Boost icon is present on betreceipt')
            self.assertFalse(price_boost_label, msg='"Smart Boost" is displayed')

    def test_004_add_few_selections_with_smart_boost_promo_available_to_betslip_and_place_multiple_bet(self):
        """
        DESCRIPTION: Add few selections with Smart Boost promo available to betslip and place multiple bet
        EXPECTED: 'Smart Boost' icon is displayed under each selection
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id3])
        self.test_002_enter_value_in_stake_field_for_multiple_bet_and_place_a_bet()
        self.test_003_verify_smart_boost_icon_on_the_bet_receipt(expected_result=True)

    def test_005_add_few_selections_without_smart_boost_promo_available_to_betslip_and_place_multiple_bet(self):
        """
        DESCRIPTION: Add few selections without Smart Boost promo available to betslip and place multiple bet
        EXPECTED: No 'Smart Boost' icon is displayed in receipt.
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id2, self.selection_id4])
        self.test_002_enter_value_in_stake_field_for_multiple_bet_and_place_a_bet()
        self.test_003_verify_smart_boost_icon_on_the_bet_receipt(expected_result=False)
