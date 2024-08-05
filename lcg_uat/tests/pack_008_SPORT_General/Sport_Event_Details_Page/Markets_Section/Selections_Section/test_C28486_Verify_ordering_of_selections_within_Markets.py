import pytest
import tests
from fractions import Fraction
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2  # Need to update for QA2 once QA2 envs are available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28486_Verify_ordering_of_selections_within_Markets(BaseSportTest):
    """
    TR_ID: C28486
    NAME: Verify ordering of selections within Markets
    DESCRIPTION: This test case verifies ordering of selections in different Markets
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Selections Order per Display Sort Name in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.event = \
                self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = self.event['event']['id']

            self.__class__.outcomes = next(((market['market']['children']) for market in self.event['event']['children']
                                            if 'Match Betting' in market['market']['templateMarketName'] and
                                            market['market'].get('children')), None)
            if self.outcomes is None:
                raise SiteServeException('There are no available outcomes')

            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            if not self.team2:
                raise SiteServeException('No Aways team found')
            self._logger.info(f'*** Football event with event id "{self.eventID}"')
            self.__class__.section_name = self.expected_market_sections.match_result
        else:
            pass

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: 'Sport' Landing Page is opened
        """
        # Covered in Step# 3

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by tapping the section's header
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.all_markets),
                        msg='"ALL MARKETS" is not active tab')
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')

        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            self.__class__.market = markets_list.get(self.section_name.title())
        else:
            self.__class__.market = markets_list.get(self.section_name.upper())
        self.assertTrue(self.market, msg='Can not find Match Result section')

        self.market.collapse()
        self.assertFalse(self.market.is_expanded(), msg='Cannot collapse the section "%s"' % self.section_name)
        self.market.expand()
        self.assertTrue(self.market.is_expanded(), msg='Cannot expand the section "%s"' % self.section_name)

    def test_005_check_presence_and_value_ofdispsortnameattribute_of_verified_market_using_first_link_from_preconditions(
            self):
        """
        DESCRIPTION: Check presence and value of **dispSortName **attribute of verified Market using first link from Preconditions
        EXPECTED: *   If **dispSortName **tag is available -> go to step №6
        EXPECTED: *   If **dispSortName **tag is NOT available -> go to step №9
        """
        dispsort_name = next((market['market']['dispSortName'] for market in self.event['event']['children'] if
                              'Match Betting' in market['market']['templateMarketName']), '')
        self.assertTrue(dispsort_name,
                        msg=f'"**dispSortName" attribute and its correeponding value "{dispsort_name}" is not available for specific market')

    def test_006_check_presence_and_value_ofoutcomemeaningminorcode_attributes_of_selections_within_verified_market(
            self):
        """
        DESCRIPTION: Check presence and value of **outcomeMeaningMinorCode **attributes of selections within verified Market
        EXPECTED: *   If **outcomeMeaningMinorCode **tags are available -> go to step №7
        EXPECTED: *   If **outcomeMeaningMinorCode **tags are not available -> go to step №8
        """
        # Covered in Step# 7 & 8

    def test_007_find_corresponding_to_verified_marketdispsortnamein_the_table_using_the_second_link_from_preconditions(
            self):
        """
        DESCRIPTION: Find corresponding to verified Market **dispSortName **in the table using the second link from Preconditions
        EXPECTED: Selections order found in the table corresponds to selections order displayed on front-end for verified Market based on **outcomeMeaningMinorCode **tag
        EXPECTED: (e.g.H-left side, A-right side, D,N,L-middle)
        """
        header_resp_team1 = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes
                                  if i["outcome"]['name'] == self.team1), '')
        self.assertTrue(header_resp_team1,
                        msg=f'Home/Away outcome code for {self.team1} '
                            f'is not found in Siteserve response "{self.outcomes}"')
        header_resp_draw = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes
                                 if i["outcome"]['name'] == 'Draw'), '')
        self.assertTrue(header_resp_draw,
                        msg=f'Home/Away outcome code for {"Draw"} '
                            f'is not found in Siteserve response "{self.outcomes}"')
        header_resp_team2 = next((i["outcome"]["outcomeMeaningMinorCode"] for i in self.outcomes
                                  if i["outcome"]['name'] == self.team2), '')
        self.assertTrue(header_resp_team2,
                        msg=f'Home/Away outcome code for {self.team2} '
                            f'is not found in Siteserve response "{self.outcomes}"')
        self.assertEqual('H', header_resp_team1,
                         msg=f'Price for "{self.team1}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_team1}"')
        self.assertEqual('D', header_resp_draw,
                         msg=f'Price for "{"Draw"}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_draw}"')
        self.assertEqual('A', header_resp_team2,
                         msg=f'Price for "{self.team2}" is in wrong order,'
                             f'not the same as in Siteserve response "{header_resp_team2}"')

    def test_008_checkdisplayorder_attributeof_selections_within_verified_market(self):
        """
        DESCRIPTION: Check **displayOrder **attribute of selections within verified Market
        EXPECTED: Selections are ordered by **displayOrder **tag value of selections in ascending order
        """
        outcomes = sorted(self.outcomes, key=lambda i: i['outcome']['displayOrder'])
        if self.brand == 'bma':
            expected_outcomes = [i['outcome']['name'] for i in outcomes]
        else:
            expected_outcomes = [(i['outcome']['name']).upper() for i in outcomes]

        outcomes_ui = self.market.outcomes.items_as_ordered_dict
        outcomes_ui_actual = list(outcomes_ui.keys())

        self.assertEqual(expected_outcomes, outcomes_ui_actual,
                         msg=f'Expected Outcomes "{expected_outcomes}" are not same as actual outcomes "{outcomes_ui_actual}"')

    def test_009_check_prices_of_selections_within_verified_market(self):
        """
        DESCRIPTION: Check prices of selections within verified Market
        EXPECTED: *   Selections are ordered **by price** in ascending order
        EXPECTED: *   If Price is the same for two or more selections - selections are ordered **alphabetically**
        """
        outcomes_ui = self.market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes_ui, msg='No outcomes are shown for Match Result market')
        sorted_outcomes = [outcome.name for outcome in
                           sorted(outcomes_ui.values(), key=lambda x: Fraction(x.bet_button.outcome_price_text))]
        self.assertTrue(sorted_outcomes, msg=f'Issue in outcomes sorting')

        # Selections are not ordered by price, rather, orderd by **displayOrder
        # self.assertListEqual(list(outcomes_ui.keys()), sorted_outcomes,
        #                      msg=f'Incorrect order of selections: '
        #                          f'Actual: {list(outcomes_ui.keys())} \nExpected: {sorted_outcomes}')

    def test_010_repeat_steps_4_5_for_sseveral_different_markets(self):
        """
        DESCRIPTION: Repeat steps №4-5 for several different Markets
        """
        # Covered in above steps
