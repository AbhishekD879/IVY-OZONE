import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.insprint_auto
@pytest.mark.bet_history_open_bets
@pytest.mark.specific_bet_types
@vtest
class Test_C66132268_Verify_ordering_of_leg_number_selection_name_in_tote_multiple_leg_bets(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C66132268
    NAME: Verify ordering of  leg number ,selection name in tote multiple leg bets
    DESCRIPTION: This test case verify ordering of  leg number ,selection name in tote multiple leg bets
    PRECONDITIONS: User should have a Horse Racing event
    PRECONDITIONS: Totepool market should be available
    """
    keep_browser_open = True
    bet_amount = 1

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_001_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_002_navigate_to__horse_racing_page(self):
        """
        DESCRIPTION: Navigate to  Horse racing page
        EXPECTED: Horse racing page is opened with all the available meetings
        """
        event = self.get_uk_tote_event(uk_tote_placepot=True)
        self.navigate_to_edp(event_id=event.event_id, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        placepot_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.placepot)
        self.assertTrue(placepot_opened, msg=f'"{vec.uk_tote.UK_TOTE_TABS.placepot}" tab is not opened')

    def test_003_check_for_the_events_which_has_totepools(self):
        """
        DESCRIPTION: Check for the events which has Totepools
        EXPECTED: Totepool market should be available with (WIN,Place,Exacta,Trifacta,Placepot,jackpot,ITV7placepot)
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found under TOTEPOOL tab')
        section_name, section = list(sections.items())[0]
        pool_legs = section.pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(pool_legs, 'Legs are not available under Placeppot tab')

        for leg_name, leg in pool_legs.items():
            leg.click()
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found under TOTEPOOL tab')
            section_name, section = list(sections.items())[0]
            outcome_name, outcome = section.pool.first_item
            outcome.select()
        section.bet_builder.summary.input.value = self.bet_amount
        self.assertTrue(section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO SLIP" button is disabled')
        section.bet_builder.summary.add_to_betslip_button.click()
        self.assertFalse(section.bet_builder.is_displayed(expected_result=False),
                         msg='Bet builder not disappears')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_place_bet_on_the_below_markets_for_multi_legs_placepotquadpotjackpotitv7placepot(self):
        """
        DESCRIPTION: Place bet on the below markets for multi-legs :
        DESCRIPTION: Placepot
        DESCRIPTION: Quadpot
        DESCRIPTION: Jackpot
        DESCRIPTION: ITV7placepot
        EXPECTED: Bets should be placed successfully on all the mention markets
        """
        # Covered in above step

    def test_005_navigate_to_mybets_openpool_bets(self):
        """
        DESCRIPTION: Navigate to mybets-open(Pool bets)
        EXPECTED: Open tab should be available with the tote  bets placed
        """
        self.site.open_my_bets_open_bets()
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg=f'{vec.bet_history.POOLS_TAB_NAME} tab is not opened')
        self.__class__.open_pools_tab_bet = next(
            iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
            None)
        self.assertIsNotNone(self.open_pools_tab_bet, msg='Bet is not available under Open >> Pools tab')

    def test_006_check_the_order_of_selections_and_leg_numbers_lines(self):
        """
        DESCRIPTION: Check the order of selections and leg numbers lines
        EXPECTED: Selections and leg number lines should be as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/6b718980-d5c6-4ec5-8a62-b6ae7540c020)
        """
        selctions_and_legs = self.open_pools_tab_bet.items_as_ordered_dict
        for selection_and_leg_name, selection_and_leg in selctions_and_legs.items():
            self.assertTrue(selection_and_leg.selection.location['y'] < selection_and_leg.event.location['y'], msg=f'Selection is not above the Leg for {selection_and_leg_name}')

    def test_007_go_to_settle_bets_after_the_pool_bets_got_settle(self):
        """
        DESCRIPTION: Go to settle bets after the pool bets got settle
        EXPECTED: Settle tab should be available with settled pool bets
        """
        # Can't Automate..Need to wait till bet got settled

    def test_008_check_the_order_of_selections_and_leg_numbers_lines(self):
        """
        DESCRIPTION: Check the order of selections and leg numbers lines
        EXPECTED: Selections and leg number lines should be as per Figma deign
        """
        # Covered in above steps
