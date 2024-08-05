import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


@pytest.mark.lad_tst2  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.login
@pytest.mark.reg160_fix
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-54572')
class Test_C10359156_Verify_Racing_Post_Pick_on_the_Race_Card(BaseGreyhound):
    """
    TR_ID: C10359156
    NAME: Verify Racing Post Pick on the Race Card
    DESCRIPTION: This test case verifies displaying of Racing Post Pick information on Greyhound event Race Card
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - User is logged in
        PRECONDITIONS: - User is at Greyhound Race Card (Event Details page)
        PRECONDITIONS: - Racing Post Pick information is present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/229095238[eventID] in 'postPick' attribute, (e.g. "postPick": "3-6-4")
        """
        event_id = self.get_event_details(racing_post_pick=True).event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.login()

    def test_001_verify_racing_post_pick_information(self):
        """
        DESCRIPTION: Verify Racing Post Pick information
        EXPECTED: - 'RACING POST PICK' logo is displayed in Race Card meeting details section
        EXPECTED: - Greyhound racing numbers sequence is displayed to the right of 'RACING POST PICK' logo (e.g. "3" "6" "4")
        EXPECTED: - Racing numbers design and colors are the same as Runner Number
        """
        markets_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list
        if markets_tabs.current != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            markets_tabs.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
            self.site.wait_content_state_changed(timeout=5)

        self.assertTrue(self.site.greyhound_event_details.tab_content.post_info.has_logo_icon(),
                        msg='Racing Post logo icon is not found')
        markets = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='Market does not have any items')

        all_silks_list = [outcome.get_silk_attribute('class') for outcome in outcomes.values() if outcome.has_silks]
        self.assertTrue(all_silks_list, msg='There are no outcome with racing post pick silks')
        racing_post_silks_list = self.site.greyhound_event_details.tab_content.post_info.items_as_ordered_dict
        self.assertTrue(racing_post_silks_list, msg='There are no racing post pick silks')

        result = all(silk in all_silks_list for silk in racing_post_silks_list)
        self.assertTrue(result, msg='"Racing Post Pick" Racing numbers design and colors not present in Runners')
