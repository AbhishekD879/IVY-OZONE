import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28480_Verify_Other_Markets_tab_on_Pre_Match_and_In_Play_Event_Details_Pages(Common):
    """
    TR_ID: C28480
    NAME: Verify 'Other Markets' tab on Pre-Match and In-Play Event Details Pages 
    DESCRIPTION: This test case verifies 'Other Markets' tab on Pre-Match and In-Play Event Details Pages.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/SportToCollection?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/find test event
        """
        event = self.get_active_events_for_category(
            category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.eventID = event['event']['id']
        self._logger.info(f'*** Football event with event id "{self.eventID}"')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
        EXPECTED: <Sport> Landing Page is opened
        """
        # Covered in Step# 3

    def test_003_clicktap_on_event_name_or_more_link_in_the_event_card(self):
        """
        DESCRIPTION: Click/Tap on Event name or 'More' link in the event card
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_004_clicktap_on_other_markets_tab_and_verify_present_markets(self):
        """
        DESCRIPTION: Click/Tap on 'Other Markets' tab and verify present markets
        EXPECTED: Market's **collectionNames **doesn't contain any** **name of collection or **collectionNames **is absent at all
        """
        other_markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(other_markets, msg='No markets are shown')

        for market_name, market in other_markets.items():
            try:
                collections_names = market.collectionNames
                self.assertFalse(collections_names,
                                 msg=f'"{collections_names}" attribute is available for "Other markets" tab')
            except AttributeError:
                continue

        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        markets = event_details['children']
        self.assertTrue(markets, msg="Markets not available")

        my_dict = {}
        for market in markets:
            market_details = market['market']
            if market_details.get('name') and market_details.get('collectionIds'):
                if market_details.get('name') in my_dict.keys():
                    self.assertEqual(my_dict[market_details.get('name')], market_details.get('collectionIds'),
                                     msg=f'Different Collection ids "{my_dict[market_details.get("name")]}" & "{market_details.get("collectionIds")}" for Collection Name "{market_details.get("name")}"')
                else:
                    my_dict[market_details.get('name')] = market_details.get('collectionIds')

    def test_005_verify_present_market_type_sections(self):
        """
        DESCRIPTION: Verify present market type sections
        EXPECTED: *   The first **two **market type sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand  market type sections by tapping the section's header
        """
        # TODO: This step can be automated once the below Jira is closed
        # Jira: https://jira.egalacoral.com/browse/BMA-61139

    def test_006_verify_market_absence(self):
        """
        DESCRIPTION: Verify market absence
        EXPECTED: Market section is absent if it isn't available in the SiteServer
        """
        # Covered in step# 4
