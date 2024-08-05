import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.environments import constants as vec
from datetime import datetime


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.mobile_only
@vtest
class Test_C2989456_Verify_count_and_order_of_Extra_Place_races_on_Home_page(Common):
    """
    TR_ID: C2989456
    NAME: Verify count and order of 'Extra Place' races on Home page
    DESCRIPTION: This test case verifies count and order of 'Extra Place' races on Home page depending on platform
    PRECONDITIONS: 1. 'Next Races' tab should be present on Home page (click [here](https://ladbrokescoral.testrail.com/index.php?/cases/view/29371) to see how to configure it)
    PRECONDITIONS: 2. 'Extra Place' horse racing events should be present
    PRECONDITIONS: 3. User is viewing 'Next Races' tab on Home page
    PRECONDITIONS: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
    PRECONDITIONS: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
    PRECONDITIONS: - HR event should have primary market 'Win or Each Way'
    PRECONDITIONS: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
    PRECONDITIONS: **To check info regarding event use the following link:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: **To get info about class events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **To get info about Extra place events use link:**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get events
        """
        if tests.settings.backend_env == 'prod':
            additional_filters = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                                           ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                                           OPERATORS.INTERSECTS, 'MKTFLAG_EPR'))
            self.__class__.events = self.get_active_events_for_category(category_id=21, additional_filters=additional_filters, all_available_events=True)
        else:
            event1 = self.ob_config.add_UK_racing_event(market_extra_place_race=True)
            event2 = self.ob_config.add_UK_racing_event(market_extra_place_race=True)
            self.__class__.events = [event1.ss_response, event2.ss_response]

    def test_001_verify_number_of_extra_place_racing_events_shown(self):
        """
        DESCRIPTION: Verify number of 'Extra Place' racing events shown
        EXPECTED: Two 'Extra Place' racing events are shown for **Coral** and one for **Ladbrokes**
        """
        self.site.wait_content_state('homepage')
        self.assertIn(vec.sb.TABS_NAME_NEXT.upper(), self.site.home.tabs_menu.items_as_ordered_dict.keys(),
                      msg='Next Races tab not present in homepage')
        self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
        self.__class__.extra_place_events = self.site.home.next_races.extra_place_module_dict.items_as_ordered_dict.keys()
        if self.brand == 'bma':
            self.assertEqual(len(self.extra_place_events), 2, msg=f'{len(self.extra_place_events)} number of events shown instead of 2')
        else:
            self.assertEqual(len(self.extra_place_events), 1, msg=f'{len(self.extra_place_events)} number of events shown instead of 1')

    def test_002_verify_order_of_extra_place_racing_events(self):
        """
        DESCRIPTION: Verify order of 'Extra Place' racing events
        EXPECTED: 'Extra Place' racing events are ordered by 'startTime' attribute from SS response in ascending
        """
        if self.brand == 'bma':
            for event in self.events:
                if event['event']['name'] == list(self.extra_place_events)[0]:
                    self.__class__.event1_time = event['event']['startTime']
                if event['event']['name'] == list(self.extra_place_events)[1]:
                    self.__class__.event2_time = event['event']['startTime']
            if self.event1_time and self.event2_time is not None:
                datetime1 = datetime.strptime(self.event1_time, '%Y-%m-%dT%H:%M:%SZ')
                datetime2 = datetime.strptime(self.event2_time, '%Y-%m-%dT%H:%M:%SZ')
                self.assertTrue(datetime1 < datetime2, msg=f'Events "{self.extra_place_events}" are not ordered by "startTime" attribute from SS response ')
            else:
                raise Exception('No extra place events found')
