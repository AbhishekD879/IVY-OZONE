import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create event on Market level with Extra place promo icon
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.medium
@vtest
class Test_C2635879_Verify_Extra_Place_icon_for_Single_Bet_on_BetSlip_and_Bet_Receipt(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2635879
    NAME: Verify Extra Place icon for Single Bet on BetSlip and Bet Receipt
    DESCRIPTION: This test case verifies that the Extra Place icon is displayed on the Bet Receipt within BetSlip
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33486 Promo / Signposting : Extra Place : Icons for Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33486
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Extra Place promo is available for <Race> event on Market level
    PRECONDITIONS: NOTE: Extra place icon should NOT be displayed on Quick betslip and Main Bet Slip - but should be displayed on Bet Receipt and Quick Bet Receipt - https://jira.egalacoral.com/browse/BMA-51626?focusedCommentId=2656965&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-2656965
    """
    keep_browser_open = True
    prices = {0: '1/4'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
        PRECONDITIONS: * User is logged in and has positive balance
        PRECONDITIONS: * Extra Place promo is available for <Race> event on Market level.
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True, lp_prices=self.prices)
        self.__class__.eventID = event.event_id
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_001_add_race_selection_with_available_extra_place_promo_on_market_level_to_the_betslipquickbet_for_mobile(
            self):
        """
        DESCRIPTION: Add <Race> selection with available Extra Place promo on Market level to the BetSlip/Quickbet (for mobile)
        EXPECTED: <Race> selection is added to the BetSlip/Quickbet (for mobile)
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.open_betslip()

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_extra_place_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Bet Receipt
        EXPECTED: * 'Extra Place' icon is displayed below market name/event name section
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        self.assertTrue(first_section.has_promo_icon, msg='Extra Place icon is not present on betreceipt')
