import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.insprint_auto
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@vtest
# This test is covering C66132267
class Test_C66111704_Verify_CSS_elementsFont_size_font_color_of_Market_name_in_My_bets(BaseBetSlipTest, BaseUKTote):
    """
    TR_ID: C66111704
    NAME: Verify CSS elements(Font size, font color )of Market name in My bets
    DESCRIPTION: This testcase verifies CSS elements(Font size, color) of Market name in my bets
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True
    selection_outcomes = []

    def verify_my_bets_pools_tab_elements_font_color_size(self, bet=None, item=None):

        test_data = {'selection': {'font size': '13px', 'color': 'rgba(51, 51, 51, 1)',
                                   'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'market': {'font size': '11px', 'color': 'rgba(43, 43, 43, 1)',
                                'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'event': {'font size': '11px', 'color': 'rgba(43, 43, 43, 1)',
                               'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif'},
                     'potential returns label': {'font size': '12px', 'color': 'rgba(51, 51, 51, 1)',
                                                 'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif',
                                                 'font weight': '400'},
                     'potential returns value': {'font size': '12px', 'color': 'rgba(51, 51, 51, 1)',
                                                 'font': '"Helvetica Neue", Helvetica, Arial, sans-serif' if self.brand != 'bma' else 'Lato, Arial, "Helvetica Neue", Helvetica, sans-serif',
                                                 'font weight': '700'}
                     }

        element = None
        if item == 'selection':
            element = bet.selection
        elif item == 'market':
            element = bet.market
        elif item == 'event':
            element = bet.event
        elif item == 'potential returns label':
            element = bet.potential_returns_label
        elif item == 'potential returns value':
            element = bet.potential_returns_value

        actual_font_size = element.css_property_value('font-size')
        actual_color = element.css_property_value('color')
        actual_font = element.css_property_value('font-family')

        expected_font_size = test_data[item]['font size']
        expected_color = test_data[item]['color']
        expected_font = test_data[item]['font']

        if item == 'potential returns label' or item == 'potential returns value':
            expected_font_weight = test_data[item]['font weight']
            actual_font_weight = element.css_property_value('font-weight')
            self.assertEqual(expected_font_weight, actual_font_weight, msg=f'Expected My bets >> Open >> Pools tab {item} '
                                                               f'font weight is '
                                                               f'{expected_font_weight} but Actual '
                                                               f'{item} font weight is '
                                                               f'{actual_font_weight}')

        self.assertEqual(expected_font_size, actual_font_size,
                         msg=f'Expected My bets >> Open >> Pools tab {item} font size is {expected_font_size} but '
                             f'Actual {item} '
                             f'font size is {actual_font_size}')
        self.assertEqual(expected_color, actual_color, msg=f'Expected My bets >> Open >> Pools tab {item}'                                                                                        
                                                                                    f' color is '
                                                                                    f'{expected_color} but Actual '
                                                                                    f'{item} color is '
                                                                                    f'{actual_color}')
        self.assertEqual(expected_font, actual_font,
                         msg=f'Expected My bets >> Open >> Pools tab {item} font is {expected_font} but Actual '
                             f'{item} font is {actual_font}')

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        # Covered in last step

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        # Covered in last step

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        # Covered in C66111682 test

    def test_003_verify_market_name_of_bets_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify Market name of bets displayed in Open tab
        EXPECTED: Font size ,font colour should be as per figma
        EXPECTED: ![](index.php?/attachments/get/8359bf84-6ad3-4f50-975a-98e17aa0487a)
        """
        # Covered in C66111682 test

    def test_004_verify_market_names_of_bets_displayed_in_cashout_tab(self):
        """
        DESCRIPTION: Verify Market names of bets displayed in Cashout tab
        EXPECTED: Font size,font color should be as per figma
        """
        # Covered in C66111682 test

    def test_005_verify_market_names_of_bets_displayed_in_settled_tab(self):
        """
        DESCRIPTION: Verify Market names of bets displayed in Settled tab
        EXPECTED: Font size,font color should be as per figma
        """
        # Covered in C66111682 test

    def test_006_repeat_step_4_6__by_placing_bets_for_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat step 4-6  by placing bets for tier1 and tier2 Sports
        EXPECTED: Result should be same
        """
        # Covered in C66111682 test

    def test_007_repeat_step_4_6_by_placing_multiple_bets_and_complex_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 by placing multiple bets and complex bets
        EXPECTED: Result should be same
        """
        # Covered in C66111682 test

    def test_008_repeat_step_4_6_for_lotto_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 for lotto bets
        EXPECTED: Result should be same
        """
        # Need to verify for Lotto bets

    def test_009_repeat_step_4_6_fot_pools(self):
        """
        DESCRIPTION: Repeat step 4-6 fot pools
        EXPECTED: Result should be same
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.bet_amount = event.min_total_stake
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='Tote Pool tab is not opened')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')

        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        bet_builder.summary.add_to_betslip_button.click()

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')

        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')

        self.__class__.stake = stake

        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg=f'{vec.bet_history.POOLS_TAB_NAME} tab is not opened')
        bet = list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        open_pools_tab_bet = next(iter(list(bet.items_as_ordered_dict.values())), None)
        # open_pools_tab_bet = next(
        #     iter(list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=2).values())),
        #     None)
        self.assertIsNotNone(open_pools_tab_bet, msg='Bet is not available under Open >> Pools tab')

        self.verify_my_bets_pools_tab_elements_font_color_size(bet=open_pools_tab_bet, item='selection')
        self.verify_my_bets_pools_tab_elements_font_color_size(bet=open_pools_tab_bet, item='market')
        self.verify_my_bets_pools_tab_elements_font_color_size(bet=bet, item='potential returns label')
        self.verify_my_bets_pools_tab_elements_font_color_size(bet=bet, item='potential returns value')
        self.verify_my_bets_pools_tab_elements_font_color_size(bet=open_pools_tab_bet, item='event')
