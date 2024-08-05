import pytest
from faker import Faker

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.outrights
@pytest.mark.each_way
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C28490_Verify_Each_Way_Terms_for_Outrights_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C28490
    NAME: Verify Each Way Terms for 'Outrights' Event Details Page
    DESCRIPTION: This test case verifies <Sport> Event Details Page for 'Outrights' events
    """
    keep_browser_open = True

    def get_market_from_ss(self, event_id: str) -> dict:
        """
        Gets market for given event from SS response
        :param event_id: specifies event id
        :return: dict with market attributes and their values
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []

        self.assertEquals(len(markets), 1,
                          msg=f'Only one market is expected in SS response. Now there are {len(markets)} of them.')
        return markets[0]['market']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create outright event which has market with Each Way terms available
        """
        fake = Faker()
        self.__class__.ew_event_name = f'Event {fake.city()} with each way'
        self.__class__.event_name = f'Event {fake.name_female()} without each way'
        ew_event = self.ob_config.add_autotest_premier_league_football_outright_event(
            event_name=self.ew_event_name, ew_terms=self.ew_terms
        )
        event = self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.event_name)

        self.__class__.eventID = ew_event.event_id
        self.__class__.event_id = event.event_id

    def test_001_open_outright_details_page(self):
        """
        DESCRIPTION: Open Outright Details Page
        EXPECTED: Outright Details Page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        if self.device_type == 'desktop' and self.brand != 'ladbrokes':
            expected_event_name = self.ew_event_name.upper()
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            expected_event_name = self.ew_event_name.title()
        else:
            expected_event_name = self.ew_event_name
        event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(event_name, expected_event_name,
                         msg='Incorrect EDP is opened.\nActual event name is "%s"\nExpected: "%s"'
                             % (event_name, expected_event_name))

    def test_002_market_with_each_way_terms_available(self):
        """
        DESCRIPTION: Verify market with Each Way terms available
        EXPECTED: Each Way Terms are displayed at the top of market section
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertEqual(len(markets), 1,
                         msg=f'Only one market should be displayed. Now there are {len(markets)} of them')
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.__class__.outright_name = vec.siteserve.OUTRIGHT.upper()
        else:
            self.__class__.outright_name = vec.siteserve.OUTRIGHT
        section = markets.get(self.outright_name)
        self.assertTrue(section, msg=f'"{self.outright_name}" '
                                     f'is not found among markets "{list(markets.keys())}"')
        self.assertTrue(section.outcomes.has_terms, msg='No each way terms are displayed')
        self.__class__.ew_terms_text = section.outcomes.terms_text

    def test_003_verify_terms_correctness(self):
        """
        DESCRIPTION: Verify terms correctness
        EXPECTED: Terms attributes correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and** 'eachWay
        EXPECTED: Places'** attributes from the Site Server
        """
        market = self.get_market_from_ss(self.eventID)

        self.assertIn('isEachWayAvailable', market.keys(),
                      msg=f'There\'s no property "isEachWayAvailable" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['isEachWayAvailable'], 'true',
                          msg='Incorrect value for "isEachWayAvailable" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['isEachWayAvailable'], 'true'))

        self.assertIn('eachWayFactorNum', market.keys(),
                      msg=f'There\'s no property "eachWayFactorNum" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num']),
                          msg='Incorrect value for "eachWayFactorNum" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num'])))

        self.assertIn('eachWayFactorDen', market.keys(),
                      msg=f'There\'s no property "eachWayFactorDen" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den']),
                          msg='Incorrect value for "eachWayFactorDen" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den'])))

        self.assertIn('eachWayPlaces', market.keys(),
                      msg=f'There\'s no property "eachWayPlaces" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayPlaces'], str(self.ew_terms['ew_places']),
                          msg='Incorrect value for "eachWayPlaces" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayPlaces'], str(self.ew_terms['ew_places'])))

    def test_004_check_terms_format(self):
        """
        DESCRIPTION: Check terms format
        EXPECTED: Terms are displayed in the following format:  " Each Way: x/y odds - Places z,j,k", where
        EXPECTED: x = eachWayFactorNum, y = eachWayFactorDen, z,j,k = eachWayPlaces
        """
        self.check_each_way_terms_format(each_way_terms=self.ew_terms_text)
        self.check_each_way_terms_correctness(each_way_terms=self.ew_terms_text, expected_each_way_terms=self.ew_terms)

    def test_005_verify_outright_event_with_market_which_does_not_have_each_way_terms_available(self):
        """
        DESCRIPTION: Verify Outright event with market which doesn't have terms available:
        DESCRIPTION: Terms are not displayed for this market
        EXPECTED: Terms are not displayed for this market
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')

        market = self.get_market_from_ss(self.event_id)
        self.assertNotIn('isEachWayAvailable', market.keys())

        if self.device_type == 'desktop' and self.brand != 'ladbrokes':
            expected_event_name = self.event_name.upper()
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            expected_event_name = self.event_name.title()
        else:
            expected_event_name = self.event_name

        event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(event_name, expected_event_name,
                         msg='Incorrect EDP is opened.\nActual event name is "%s"\nExpected: "%s"'
                             % (event_name, expected_event_name))

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertEqual(len(markets), 1, msg='Only one market should be displayed')
        self.assertFalse(markets[self.outright_name].outcomes.has_terms,
                         msg='Each way terms should not be displayed')
