import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28485_Verify_number_of_columns_for_Market(Common):
    """
    TR_ID: C28485
    NAME: Verify number of columns for Market
    DESCRIPTION: Verify number of columns for particular Market displaying.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Please check the Number of Columns per Display Sort Name in the table using the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Generic+Sport+Template+-+Selections+Display+Rules
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.events = \
                self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,all_available_events=True)
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            self.__class__.event = event.ss_response
        for event in self.events:
            self.__class__.exp_market = 'Match Betting' if self.brand == 'bma' else 'Match Result'
            self.__class__.outcomes = next(((market['market']['children']) for market in event['event']['children']
                                            if self.exp_market in market['market']['templateMarketName'] and
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
            self.__class__.eventID = event['event']['id']
            self.__class__.event =event
            self._logger.info(f'*** Football event with event id "{self.eventID}"')
        if not self.team1:
            raise SiteServeException('No Home team found')
        if not self.team2:
            raise SiteServeException('No Aways team found')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        # Covered in step-3

    def test_003_clicktap_on_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Click/Tap on Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, timeout=60)

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by clicking/tapping the accordions
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.all_markets),
                        msg='"ALL MARKETS" is not active tab')
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        markets_dict = {market_names.upper(): markets for market_names, markets in markets_list.items()}
        self.assertTrue(markets_list, msg='Markets list is not present')
        self.__class__.exp_market = next((markt_name for markt_name in markets_dict.keys() if 'MATCH RESULT' == markt_name or 'MATCH BETTING' == markt_name))
        self.assertTrue(self.exp_market, msg='Can not find Match Result section')
        self.__class__.market = markets_dict.get(self.exp_market)
        self.assertTrue(self.market, msg='Can not find Match Result section')

        self.market.collapse()
        self.assertFalse(self.market.is_expanded(), msg='Cannot collapse the section "%s"' % self.exp_market)
        self.market.expand()
        self.assertTrue(self.market.is_expanded(), msg='Cannot expand the section "%s"' % self.exp_market)

    def test_005_check_presence_and_value_ofdispsortname_attribute_of_verified_market_using_the_first_link_from_preconditions(self):
        """
        DESCRIPTION: Check presence and value of **dispSortName** attribute of verified Market using the first link from Preconditions
        EXPECTED: *   If **dispSortName **tag is available -> go to step №6
        EXPECTED: *   If **dispSortName **tag is NOT available -> go to step №7
        """
        dispsort_name = next((market['market']['dispSortName'] for market in self.event['event']['children'] if
                              self.exp_market in market['market']['templateMarketName'].upper()), '')
        self.assertTrue(dispsort_name,
                        msg=f'"**dispSortName" attribute and its correeponding value "{dispsort_name}" is not available for specific market')

    def test_006_find_correspondingdispsortnamein_the_table_using_the_second_link_from_preconditions(self):
        """
        DESCRIPTION: Find corresponding **dispSortName **in the table using the second link from Preconditions
        EXPECTED: Number of columns found in the table corresponds to number of columns displayed on front-end for verified Market
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

    def test_007_verify_number_of_selections_in_such_market(self):
        """
        DESCRIPTION: Verify number of selections in such Market
        EXPECTED: *   1-6 selections within Market -> they are displayed in **ONE **column
        EXPECTED: *   6-24 selections -> Market selections are displayed in **TWO **columns
        EXPECTED: *   More than 24 selections -> Market selections are displayed in **THREE **columns
        """
        # Covered in above steps

    def test_008_repeat_steps_4_5_for_several_different_markets(self):
        """
        DESCRIPTION: Repeat steps №4-5 for several different Markets
        EXPECTED:
        """
        # Covered in above steps
