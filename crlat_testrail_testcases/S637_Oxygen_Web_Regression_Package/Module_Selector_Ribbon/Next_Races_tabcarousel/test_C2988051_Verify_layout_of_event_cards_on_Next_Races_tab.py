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
class Test_C2988051_Verify_layout_of_event_cards_on_Next_Races_tab(Common):
    """
    TR_ID: C2988051
    NAME: Verify layout of event cards on 'Next Races' tab
    DESCRIPTION: This test case verifies layout of event cards on 'Next Races' tab
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Race events are available for the current day
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) 'Next Races' tab is CMS configurable, please look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/29371 test case where this process is described.
    PRECONDITIONS: 2) The number of events and selections are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 3) To get info about class events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: 4) Please take a look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/1108083 test cases to check Racing Post Information.
    """
    keep_browser_open = True

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        pass

    def test_002_verify_event_cards_layout(self):
        """
        DESCRIPTION: Verify 'Event Cards' layout
        EXPECTED: * Event cards are displayed one by one as the list
        EXPECTED: * 'Event Card' consist of:
        EXPECTED: * Header
        EXPECTED: * Subheader
        EXPECTED: * Event card main body
        """
        pass

    def test_003_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: 'Event Card' header consists of:
        EXPECTED: * Event name in the next format: **'HH:MM typeName'**(correspond to **'typeName'** and **'startTime'** in SS response)
        EXPECTED: * 'More' link with chevron
        EXPECTED: * 'Going' status (corresponds to **'going'** within **'racingFormEvent'** section from SS response)
        EXPECTED: * 'Distance' value in the next format: **XXm XXf XXy** (corresponds to **'distance'** within **'racingFormEvent'** section from SS response)
        EXPECTED: * 'Countdown timer' in the next format: **'Starts in mm:ss'**
        """
        pass

    def test_004_verify_event_card_subheader_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout
        EXPECTED: 'Event Card' subheader consists of:
        EXPECTED: * 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (taken from SS response and correspond to **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes )
        EXPECTED: * 'Signposting Promotion' icon (if one or all of **'drilldownTagNames="EVFLAG_EPR,EVFLAG_FI,EVFLAG_MB,EVFLAG_BBL** attributes are received in SS response)
        EXPECTED: * 'CashOut' icon is shown on the right (if the event has **'cashoutAvail'='Y'** in SS response)
        EXPECTED: * 'WATCH' icon
        """
        pass

    def test_005_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: 'Event Card' body consists of:
        EXPECTED: * Runner Number (taken from **'racingFormEvent'** section in SS response)
        EXPECTED: * Draw Number (In brackets below Runner Number) (taken from **'racingFormEvent'** section in SS response)
        EXPECTED: * Silk (taken from **'racingFormEvent'** section in SS response)
        EXPECTED: * Horse Name (taken from **'racingFormEvent'** section in SS response)
        EXPECTED: * Jockey/Trainer Information (taken from **'racingFormEvent'** section in SS response)
        EXPECTED: * 'Odds' button
        """
        pass
