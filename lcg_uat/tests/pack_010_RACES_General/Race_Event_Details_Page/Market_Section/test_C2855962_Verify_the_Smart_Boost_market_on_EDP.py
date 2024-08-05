import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from collections import OrderedDict
from crlat_siteserve_client.utils.exceptions import SiteServeException


@pytest.mark.prod
# @pytest.mark.tst2  # smart boosts market is present on prod
# @pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.reg156_fix
@vtest
class Test_C2855962_Verify_the_Smart_Boost_market_on_EDP(BaseSportTest):
    """
    TR_ID: C2855962
    NAME: Verify the 'Smart Boost' market on EDP
    DESCRIPTION: This test case verifies the  'Smart Boost' market on EDP and its content
    PRECONDITIONS: 1. User is on <Race> EDP
    PRECONDITIONS: 2. 'Smart Boost' market is created for the event and has flags 'Price Boost'/'Super Smart Boost' in Open Bet TI (on market level)
    PRECONDITIONS: 3. 'Smart Boost' market contains 1 selection with price change (indicated previous price) within type
    PRECONDITIONS: 4. Selection contains 'Was price' value in its name in brackets in Open Bet TI  (in decimal format)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is on <Sport> EDP, 'All Markets' tab
        PRECONDITIONS: 2. Smart Boost market is created for the event and has flags 'Price Boost'/'Super Smart Boost' in Open Bet TI (on market level)
        PRECONDITIONS: 3. Selection contains 'Was price' value in its name in brackets in Open Bet TI  (in decimal format)
        """

        def get_event_id_and_smart_boost_market_name(event):
            # setting the event id
            event_id = event['event']['id']
            # getting all the market names from the response for the current event
            all_market_names = {market_data['market']['templateMarketName'] for market_data in event['event']['children']}
            # converting all the market names to upper case letters
            upper_all_market_names = {item.upper() for item in all_market_names}
            # validating if the required 'Smart Boost' market is available in the responses market names depending upon the brand
            if self.brand == 'bma' and 'ODDS BOOSTERS' in upper_all_market_names:
                market_section_name = 'ODDS BOOSTERS'
            elif self.brand == 'ladbrokes':
                if 'PRICE BOOSTS' in upper_all_market_names:
                    market_section_name = 'PRICE BOOSTS'
                elif 'PRICE BOOST' in upper_all_market_names:
                    market_section_name = 'PRICE BOOST'
            else:
                raise SiteServeException(f'No required Smart Boost market found in response'
                                       f' for the event id: {event_id}, in the brand {self.brand}')
            return event_id, market_section_name

        filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.INTERSECTS, 'EVFLAG_PB')
        self.__class__.eventID, self.__class__.response_market_section_name = \
            get_event_id_and_smart_boost_market_name(
                self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=filter)[0])
        self.site.login()
        self.site.wait_content_state('Homepage')
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        self.navigate_to_edp(self.eventID, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=20)

    def test_001_verify_the_market_presence_on_edp(self):
        """
        DESCRIPTION: Verify the market presence on EDP
        EXPECTED: 'Smart Boost' market is present on race EDP
        """
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list,
                        msg='No one market tab found on event details page')
        markets_tabs = markets_tabs_list.items_as_ordered_dict
        self.assertTrue(markets_tabs, msg='No Market tabs found')
        markets_tabs_list.open_tab(vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}" is not active tab, '
                             f'active tab is "{current_tab}"')
        markets_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        uppercase_markets_sections = OrderedDict((key.upper(), value) for key, value in markets_sections.items())
        self.assertIn(self.response_market_section_name, uppercase_markets_sections,
                      msg=f'"{self.response_market_section_name}" market is not displayed')
        self.__class__.market = uppercase_markets_sections.get(self.response_market_section_name)
        self.assertTrue(self.market, msg='Can not find Price boosts section')

    def test_002_verify_the_view_of_selection_with_changed_price(self):
        """
        DESCRIPTION: Verify the view of selection with changed price
        EXPECTED: * Selection name is displayed on the left
        EXPECTED: * Price odds button is displayed opposite to the selection name (on the right)
        EXPECTED: * Previous price ('was price') of selection is placed under price odds button (on the right)
        """
        self.market.expand()
        self.assertTrue(self.market.promotion_icons.has_price_boost,
                        msg='Price boost is not displayed')
        selection_name = self.market.outcomes.items[0].outcome_name
        self.assertTrue(selection_name, msg=f'"{selection_name}" is not displayed')
        was_price = self.market.outcomes.items[0].was_price
        self.assertTrue(was_price, msg=f'"{was_price}" is not displayed')
        bet_button = self.market.outcomes.items[0].bet_button.name
        self.assertTrue(bet_button, msg=f'"{bet_button}" is not displayed')

    def test_003_switch_to_fractional_format_top_right_menu__settings__odds_format(self):
        """
        DESCRIPTION: Switch to fractional format (top right menu-> Settings-> odds format)
        EXPECTED: Selection previous price remains crossed out and displayed under odd price button
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Fractional')
        self.navigate_to_edp(self.eventID, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
        self.test_001_verify_the_market_presence_on_edp()
        self.test_002_verify_the_view_of_selection_with_changed_price()
