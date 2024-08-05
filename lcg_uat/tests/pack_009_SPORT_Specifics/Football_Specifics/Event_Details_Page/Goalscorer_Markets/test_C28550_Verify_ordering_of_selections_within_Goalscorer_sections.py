import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod // cannot create events for goalscorer
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28550_Verify_ordering_of_selections_within_Goalscorer_sections(Common):
    """
    TR_ID: C28550
    NAME: Verify ordering of selections within Goalscorer sections
    DESCRIPTION: This test case verifies ordering of selections within Goalscorer sections.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with goalscorer markets (First Goalscorer, Anytime Goalscorer, Goalscorer - 2 or More, Last Goalscorer, Hat trick)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Anytime Goalscorer"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Anytime"
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' event
        """
        markets = [('first_goalscorer', {'cashout': True}),
                   ('anytime_goalscorer', {'cashout': True}),
                   ('goalscorer_2_or_more', {'cashout': True}),
                   ('hat_trick', {'cashout': True}),
                   ('last_goalscorer', {'cashout': True})
                   ]

        event_params = self.ob_config.add_football_event_to_autotest_league2(
            markets=markets)
        self.__class__.eventID = event_params.event_id
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.team1, event_params.team2, event_params.selection_ids

        for market in event_params.ss_response['event']['children']:
            if self.brand == 'bma':
                self.__class__.market_names = ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 or More',
                                               'Hat trick', 'Last Goalscorer']
            else:
                self.__class__.market_names = ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 Or More',
                                               'Hat trick', 'Last Goalscorer']
            if market['market']['templateMarketName'] == self.market_names[0]:
                self.__class__.first_goalscorer_market = market['market']['children']
            elif market['market']['templateMarketName'] == self.market_names[4]:
                self.__class__.last_goalscorere_market = market['market']['children']

    def verify_price_order(self, section, market):
        # checking price order
        selection_price = []
        odds_price = []
        expected_selection_name = []

        for i in market:
            expected_selection_name.append(i['outcome']['name'])
            price_num = i['outcome']['children'][0]['price']['priceNum']
            price_den = i['outcome']['children'][0]['price']['priceDen']
            odds_price.append(f'{price_num}/{price_den}')

        for name, switcher in self.market_grouping_buttons.items():
            switcher.click()
            sleep(3)
            selections_list = section.outcome_table.items
            for selection in range(len(selections_list)):
                selection_price.append(selections_list[selection].bet_button.outcome_price_text)

        self.assertEquals(sorted(selection_price), odds_price,
                          msg=f'Actual odds price: "{selection_price}" is not in '
                              f'Expected odds price: "{odds_price}"')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No one market found on event details page')

    def test_003_go_to_popular_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Popular Goalscorer Markets' section
        EXPECTED: Section is expanded and displayed correctly
        """
        self.__class__.popular_goalscorer_section = self.markets.get(
            self.expected_market_sections.popular_goalscorer_markets)
        self.assertTrue(self.popular_goalscorer_section, msg='"POPULAR GOALSCORER MARKETS" section is not found')
        self.popular_goalscorer_section.collapse()
        self.assertFalse(self.popular_goalscorer_section.is_expanded(),
                         msg='"POPULAR GOALSCORER MARKETS" is not collapsible')
        self.popular_goalscorer_section.expand()
        self.assertTrue(self.popular_goalscorer_section.is_expanded(),
                        msg='"POPULAR GOALSCORER MARKETS" is not expandable')

    def test_004_find_first_available_market_first_column_in_the_list_in_goalscorer_section(self):
        """
        DESCRIPTION: Find first available market (first column) in the list in Goalscorer section
        EXPECTED: Markets are ordered in the following way
        EXPECTED: *   '1st' ('First Goalscorer')
        EXPECTED: *   'Anytime' ('Anytime Goalscorer')
        EXPECTED: *   '2 or More' ('Goalscorer - 2 or More')
        """
        actual_columns = self.popular_goalscorer_section.outcome_table.columns
        if self.device_type == 'desktop' and self.brand != 'bma':
            actual_columns = [each_string.upper() for each_string in actual_columns]
        self.assertEqual(actual_columns, vec.sb.EXPECTED_POPULAR_GOALSCORER_COLUMNS,
                         msg=f'Incorrect table columns. Actual: "{actual_columns}", Expected:"{vec.sb.EXPECTED_POPULAR_GOALSCORER_COLUMNS}"')

    def test_005_verify_prices_order_for_market_from_step_4(self):
        """
        DESCRIPTION: Verify prices order for market from step №4
        EXPECTED: *   Selections are ordered **by price** in ascending order for verified market
        EXPECTED: *   Players names are ordered accordingly with prices of verified market
        EXPECTED: *   Outcomes of other markets (e.g. '2 or More') are ordered accordingly
        EXPECTED: *   'No goalscorer' is shown at the end of the list if available
        """
        self.__class__.market_grouping_buttons = self.popular_goalscorer_section.grouping_buttons.items_as_ordered_dict
        actual_players = sorted(self.popular_goalscorer_section.outcome_table.players)
        expected_home_players = sorted(self.selection_ids['last_goalscorer'].keys())[1::2]
        self.assertListEqual(actual_players, expected_home_players,
                             msg='Incorrect players. Actual: "%s", Expected:"%s"'
                                 % (actual_players, expected_home_players))
        self.verify_price_order(self.popular_goalscorer_section, self.first_goalscorer_market)

    def test_006_go_to_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: Section is expanded and displayed correctly
        """
        self.__class__.other_goalscorer_section = self.markets.get(
            self.expected_market_sections.other_goalscorer_markets)
        self.assertTrue(self.other_goalscorer_section, msg='OTHER GOALSCORER MARKETS section is not found')
        self.other_goalscorer_section.collapse()
        self.assertFalse(self.other_goalscorer_section.is_expanded(),
                         msg='"OTHER GOALSCORER MARKETS" is not collapsible')
        self.other_goalscorer_section.expand()
        self.assertTrue(self.other_goalscorer_section.is_expanded(), msg='"OTHER GOALSCORER MARKETS" is not expandable')

    def test_007_find_first_available_market_in_the_list_in_goalscorer_section(self):
        """
        DESCRIPTION: Find first available market in the list in Goalscorer section
        EXPECTED: Markets are ordered in the following way
        EXPECTED: *   'Last' ('Last Goalscorer')
        EXPECTED: *   'Hatrick' ('Hat trick')
        """
        actual_columns = self.other_goalscorer_section.outcome_table.columns
        if self.device_type == 'desktop' and self.brand != 'bma':
            actual_columns = [each_string.upper() for each_string in actual_columns]
        self.assertEqual(actual_columns, vec.sb.EXPECTED_OTHER_GOALSCORER_COLUMNS,
                         msg=f'Incorrect table columns. Actual: "{actual_columns}", Expected:"{vec.sb.EXPECTED_OTHER_GOALSCORER_COLUMNS}"')

    def test_008_verify_prices_order_for_market_from_step_7(self):
        """
        DESCRIPTION: Verify prices order for market from step №7
        EXPECTED: *   Selections are ordered **by price** in ascending order for verified market
        EXPECTED: *   Players names are ordered accordingly with prices of verified market
        EXPECTED: *   Outcomes of other market are ordered accordingly
        EXPECTED: *   'No goalscorer' is shown in the end of the list if available
        """
        self.__class__.market_grouping_buttons = self.other_goalscorer_section.grouping_buttons.items_as_ordered_dict
        actual_players = sorted(self.other_goalscorer_section.outcome_table.players)
        expected_home_players = sorted(self.selection_ids['last_goalscorer'].keys())[1::2]
        self.assertListEqual(actual_players, expected_home_players,
                             msg='Incorrect players. Actual: "%s", Expected:"%s"'
                                 % (actual_players, expected_home_players))
        self.verify_price_order(self.other_goalscorer_section, self.last_goalscorere_market)
