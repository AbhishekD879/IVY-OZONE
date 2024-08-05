import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.event_details
@pytest.mark.sports
@pytest.mark.surface_bets
@pytest.mark.login
@vtest
class Test_C9770802_Verify_bet_placement_from_the_Surface_Bets_on_EDP(BaseBetSlipTest):
    """
    TR_ID: C9770802
    VOL_ID: C12600641
    NAME: Verify bet placement from the Surface Bets on EDP
    DESCRIPTION: Test case verifies possibility to place bet from the Surface Bet on EDP
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True
    bet_amount = 0.3

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
        DESCRIPTION: 2. Open this EDP
        """
        event = self.ob_config.add_football_event_to_uefa_champions_league()
        surface_bet_event = self.ob_config.add_football_event_to_uefa_champions_league()
        event_id = event.event_id
        selection_ids, team1 = surface_bet_event.selection_ids, surface_bet_event.team1
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                      eventIDs=event_id, edpOn=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.site.login()
        self.navigate_to_edp(event_id, timeout=15)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id: {event_id}')
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='There are no surface bet in the container')
        self.__class__.surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')

    def test_001_place_the_bet_using_price_button_of_the_surface_bet_from_the_betslip_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the Betslip. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        self.surface_bet.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not opened')

        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.site.bet_receipt.footer.click_done()

    def test_002_place_the_bet_using_price_button_of_the_surface_bet_from_the_quickbet_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the QuickBet. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module disappears after Bet Placement')
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg=f'Surface bet "{self.surface_bet_title}" disappears after Bet Placement')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')

        surface_bet.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not opened')

        quick_bet = self.site.quick_bet_panel.selection
        quick_bet.content.amount_form.input.value = self.bet_amount
        self.site.quick_bet_panel.place_bet.click()

        self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
