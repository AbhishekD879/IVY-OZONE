import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.ob_smoke
@pytest.mark.medium
@pytest.mark.event_details
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.desktop
@pytest.mark.mobile
@vtest
class Test_C28849_Verify_Race_Each_Way_Terms(BaseRacing):
    """
    TR_ID: C28849
    VOL_ID: C9698168
    NAME: Verify Race Each Way Terms
    """
    keep_browser_open = True
    eventIDs = {}
    ew_terms = ''

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/find in SS racing event with Each Way terms
        EXPECTED: Racing event with Each Way terms is created/found
        """
        if tests.settings.backend_env == 'prod':
            ew_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE)
            event_ew_available = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                     additional_filters=ew_available_filter)[0]

            ew_not_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_FALSE)
            event_ew_not_available = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                         additional_filters=ew_not_available_filter)[0]
            self.__class__.eventIDs.update({'ew_available': event_ew_available['event']['id'],
                                            'ew_not_available': event_ew_not_available['event']['id']
                                            })
            market = next((market['market'] for market in event_ew_available['event']['children'] if market['market'].get('eachWayPlaces')), None)
            if not market:
                raise SiteServeException('No market with eachWayPlaces parameter')
            self.__class__.expected_ew_terms = {"ew_places": market["eachWayPlaces"],
                                                "ew_fac_num": market["eachWayFactorNum"],
                                                "ew_fac_den": market["eachWayFactorDen"]}
        else:
            self.__class__.expected_ew_terms = {"ew_places": 3, "ew_fac_num": 1, "ew_fac_den": 6}
            event_ew_available = self.ob_config.add_UK_racing_event(ew_terms=self.expected_ew_terms, number_of_runners=1)
            event_ew_not_available = self.ob_config.add_UK_racing_event(ew_terms=False, number_of_runners=1)
            self.__class__.eventIDs.update({'ew_available': event_ew_available.event_id,
                                            'ew_not_available': event_ew_not_available.event_id
                                            })
        self._logger.info(f'*** Found/Created events with IDs {self.eventIDs}')

    def test_001_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the event details page
        EXPECTED: 1. Event details page is opened
        EXPECTED: 2. 'Win or E/W' tab is opened by default
        """
        self.navigate_to_edp(event_id=self.eventIDs['ew_available'], sport_name='horse-racing')
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(tab_name)

    def test_002_check_terms_displaying(self):
        """
        DESCRIPTION: Check terms displaying
        EXPECTED: 1. Each-way terms are displayed if **'isEachWayAvailable'** = 'true' attribute is present from SiteServer response
        EXPECTED: 2. Each-way terms are displayed above the list of selection
        """
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market_name, market = list(markets.items())[0]

        self.__class__.ew_terms = market.section_header.each_way_terms
        self.assertTrue(self.ew_terms != '', msg='Each Way terms are empty')
        self._logger.debug(f'*** Race each way terms: "{self.ew_terms}" for market "{market_name}"')

    def test_003_verify_terms_correctness(self):
        """
        DESCRIPTION: Verify terms correctness
        EXPECTED: Terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and** 'eachWayPlaces'** attributes from the Site Server
        """
        self.check_each_way_terms_correctness(each_way_terms=self.ew_terms,
                                              expected_each_way_terms=self.expected_ew_terms)

    def test_004_check_terms_format(self):
        """
        DESCRIPTION: Check terms format
        EXPECTED:  Terms are displayed in the following format:
        EXPECTED:  " Each Way: x/y odds - places z,j,k" where:
        EXPECTED:   -  x = eachWayFactorNum
        EXPECTED:   -  y = eachWayFactorDen
        EXPECTED:   -  z,j,k = eachWayPlaces
        """
        self.check_each_way_terms_format(each_way_terms=self.ew_terms)

    def test_005_verify_event_which_has_markets_where_attribute_iseachwayavailabletrue_is_absent(self):
        """
        DESCRIPTION: Verify event which has markets where attribute **'isEachWayAvailable'**='true' is absent
        EXPECTED: Terms are not displayed for those markets
        """
        self.navigate_to_edp(event_id=self.eventIDs['ew_not_available'], sport_name='horse-racing')
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(tab_name)

        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        market = list(markets.values())[0]

        ew_terms = False if not market.has_header() else market.section_header.has_each_way_terms(expected_result=False)
        self.assertFalse(ew_terms, msg='Each Way terms should not be displayed')
