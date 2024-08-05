import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.timeout(1200)
@vtest
class Test_C11250804_Verify_display_of_multiple_card_actual(BaseBetSlipTest):
    """
    TR_ID: C11250804
    NAME: Verify display of multiple card
    DESCRIPTION: This test case verifies displaying of multiple card
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True
    number_of_events = 8
    selection_ids = []

    def check_multiple_card(self, card_name, card_market_name, section):
        self.assertIn(card_name, section.keys(),
                      msg=f'No "{card_name}" stake was found in "{section.keys()}"')
        multiple_stake = section.get(card_name)
        self.assertEqual(multiple_stake.market_name, card_market_name,
                         msg=f'Actual Bet summary info "{multiple_stake.market_name}" does not match expected "{card_market_name}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: create test event
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(number_of_events=self.number_of_events,
                                                         category_id=self.ob_config.football_config.category_id)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market['market'].get('children') and
                                            market.get('market').get('marketMeaningMinorCode') == 'MR'), None)
                outcomes = match_result_market['children']
                selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                self.selection_ids.append(list(selection_ids.values())[0])
        else:
            for _ in range(self.number_of_events):
                event_params = self.ob_config.add_autotest_premier_league_football_event()
                self.selection_ids.append(list(event_params.selection_ids.values())[0])

    def test_001_add_2_or_more_selections_from_different_events_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add 2 or more selections from different events to the Betslip and open Betslip
        EXPECTED: The bet slip is displayed
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1], self.selection_ids[2]])

    def test_002_verify_that_the_multiple_card_is_displayed_in_multiple_section_under_single_section(self):
        """
        DESCRIPTION: Verify that the multiple card is displayed in 'Multiple' section under 'Single' section
        EXPECTED: The multiple card is displayed in 'Multiple' section under 'Single' section
        """
        selection_list = self.get_betslip_content().betslip_sections_list
        self.assertEqual(selection_list.multiple_selections_label, vec.betslip.MULTIPLES,
                         msg=f'Selection message "{selection_list.multiple_selections_label}" '
                         f'is not the same as expected "{vec.betslip.MULTIPLES}"')

    def test_003_verify_the_card_elements(self):
        """
        DESCRIPTION: Verify the card elements
        EXPECTED: The card should contain:
        EXPECTED: - multiple bet type name (multiples will include number of bets e.g. acca = x1)
        EXPECTED: price
        EXPECTED: - 'estimated returns' / 'potential returns' for that individual bet
        EXPECTED: stake box
        EXPECTED: - bet type summary info
        """
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(self.multiples_section, msg='Multiples section does not appear')
        stake = list(self.multiples_section.values())[0]
        self.assertTrue(stake.odds, msg='Price is not displayed')
        for stake in list(self.multiples_section.values()):
            self.assertTrue(stake.est_returns_label, msg='"Est. Returns" field is not displayed')
            self.assertTrue(stake.amount_form, msg='Stake box is not displayed')
        # bet type summary info and multiple bet type name will be verified in step 4

    def test_004_verify_bet_type_summary_info_text(self):
        """
        DESCRIPTION: Verify bet type summary info text
        EXPECTED: Bet summary info text:
        EXPECTED: - Trixie: '3 doubles and a treble'
        EXPECTED: - Fourfold: 'Accumulator Bet'
        EXPECTED: (Continued for Fivefold to Twentyfold as above)
        EXPECTED: - Patent: ' 3 singles, 3 doubles and a treble'
        EXPECTED: - Yankee: '6 doubles, 4 trebles and a fourfold accumulator'
        EXPECTED: - Canadian: '10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
        EXPECTED: - Heinz: '15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
        EXPECTED: - Super Heinz: '21 doubles, 35 trebles, 35 fourfolds, 21 fivefolds, 7 sixfolds and a sevenfold accumulator'
        EXPECTED: - Goliath: '28 doubles, 56 trebles, 70 fourfolds, 56 fivefolds, 28 sixfolds, 8 sevenfolds and an eightfold accumulator'
        EXPECTED: - Lucky 15: '4 singles, 6 doubles, 4 trebles and a fourfold accumulator'
        EXPECTED: - Lucky 31: '5 singles, 10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
        EXPECTED: - Lucky 63: '6 singles, 15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
        """
        self.check_multiple_card(card_name=vec.betslip.TRX,
                                 card_market_name=vec.betslip.TRX_INFO,
                                 section=self.multiples_section)

        self.check_multiple_card(card_name=vec.betslip.PAT,
                                 card_market_name=vec.betslip.PAT_INFO,
                                 section=self.multiples_section)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[3])
        multiples_section = self.get_betslip_sections(multiples=True).Multiples

        self.check_multiple_card(card_name=vec.betslip.ACC4,
                                 card_market_name=vec.betslip.ACC_INFO,
                                 section=multiples_section)

        self.check_multiple_card(card_name=vec.betslip.YAN,
                                 card_market_name=vec.betslip.YAN_INFO,
                                 section=multiples_section)

        self.check_multiple_card(card_name=vec.betslip.L15,
                                 card_market_name=vec.betslip.L15_INFO,
                                 section=multiples_section)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[4])
        multiples_section = self.get_betslip_sections(multiples=True).Multiples

        self.check_multiple_card(card_name=vec.betslip.ACC5,
                                 card_market_name=vec.betslip.ACC_INFO,
                                 section=multiples_section)

        self.check_multiple_card(card_name=vec.betslip.CAN,
                                 card_market_name=vec.betslip.CAN_INFO,
                                 section=multiples_section)

        self.check_multiple_card(card_name=vec.betslip.L31,
                                 card_market_name=vec.betslip.L31_INFO,
                                 section=multiples_section)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[5])
        multiples_section = self.get_betslip_sections(multiples=True).Multiples

        self.check_multiple_card(card_name=vec.betslip.HNZ,
                                 card_market_name=vec.betslip.HNZ_INFO,
                                 section=multiples_section)

        self.check_multiple_card(card_name=vec.betslip.L63,
                                 card_market_name=vec.betslip.L63_INFO,
                                 section=multiples_section)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[6])
        multiples_section = self.get_betslip_sections(multiples=True).Multiples

        self.check_multiple_card(card_name=vec.betslip.SHNZ,
                                 card_market_name=vec.betslip.SHNZ_INFO,
                                 section=multiples_section)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[7])
        multiples_section = self.get_betslip_sections(multiples=True).Multiples

        self.check_multiple_card(card_name=vec.betslip.GOL,
                                 card_market_name=vec.betslip.GOL_INFO,
                                 section=multiples_section)
