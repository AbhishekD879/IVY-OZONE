import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2989464_Verify_More_link_functionality_for_Next_Races_module_on_the_Homepage(Common):
    """
    TR_ID: C2989464
    NAME: Verify 'More' link functionality for 'Next Races' module on the Homepage
    DESCRIPTION: This test case verifies 'More' / 'Full Race Card'(for Coral Desktop) link functionality for 'Next Races' module on the Homepage
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Tap on 'Next Races' tab at the Homepage (for Mobile) / scroll the homepage down to 'Next Races' carousel (for Desktop)
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. List of Event Cards is displayed at the page
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) 'Next Races' tab is CMS configurable, please look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/29371 test case where this process is described.
    PRECONDITIONS: 2) The number of events and selection are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 3) To get info about class use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    """
    keep_browser_open = True

    def test_001_verify_more__full_race_cardfor_coral_desktop_link_displaying(self):
        """
        DESCRIPTION: Verify 'More' / 'Full Race Card'(for Coral Desktop) link displaying
        EXPECTED: * Link is displayed at the 'Event Card' header / at the Event Card footer (for Coral Desktop)
        EXPECTED: * Link is displayed for each event in 'Next Races' module
        EXPECTED: * Link is aligned to the right
        """
        pass

    def test_002_tap_on_more__full_race_cardfor_coral_desktop_link(self):
        """
        DESCRIPTION: Tap on 'More' / 'Full Race Card'(for Coral Desktop) link
        EXPECTED: The user takes to the particular event details page
        """
        pass

    def test_003_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on 'Back' button
        EXPECTED: The previously visited page is opened
        """
        pass
