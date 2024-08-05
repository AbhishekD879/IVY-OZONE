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
class Test_C9769894_Verify_More_link_functionality_for_Next_Races_module_on_Greyhounds(Common):
    """
    TR_ID: C9769894
    NAME: Verify 'More' link functionality for 'Next Races' module on Greyhounds
    DESCRIPTION: This test case verifies 'More' link functionality for 'Next Races' module on Greyhounds
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile [C23201020]
    PRECONDITIONS: 1. "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app.
    PRECONDITIONS: 3. Tap on 'Next Races' tab on the Greyhounds.
    PRECONDITIONS: 4. Race events are available for the current day.
    PRECONDITIONS: 5. List of Event Cards is displayed at the page.
    PRECONDITIONS: Note:
    PRECONDITIONS: 1. The number of events is not CMS configurable. There should be always 20 events displayed.
    PRECONDITIONS: 2. To get info about class use link:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    """
    keep_browser_open = True

    def test_001_verify_more_link_displaying(self):
        """
        DESCRIPTION: Verify 'More' link displaying.
        EXPECTED: * Link is displayed at the 'Event Card' header.
        EXPECTED: * Link is displayed for each event in the 'Next Races' module.
        EXPECTED: * Link is aligned to the right.
        """
        pass

    def test_002_tap_on_more_link(self):
        """
        DESCRIPTION: Tap on 'More' link.
        EXPECTED: The user is taken to the particular event details page.
        """
        pass

    def test_003_tap_on_the_back_button(self):
        """
        DESCRIPTION: Tap on the 'Back' button.
        EXPECTED: The previously visited page is opened.
        """
        pass