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
class Test_C9770776_Verify_layout_of_event_cards_on_Next_Races_tab(Common):
    """
    TR_ID: C9770776
    NAME: Verify layout of event cards on 'Next Races' tab
    DESCRIPTION: This test case verifies layout of event cards on 'Next Races' tab
    DESCRIPTION: To add: step 5 - additional details (Trainer, Form) can be displayed in Event Card body if received from Racing Post MS
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds
    PRECONDITIONS: Note:
    PRECONDITIONS: To get info about class use link:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
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
        EXPECTED: * 'Event Card' consists of:
        EXPECTED: * Header
        EXPECTED: * Subheader
        EXPECTED: * Event card main body
        """
        pass

    def test_003_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: 'Event Card' header consists of:
        EXPECTED: * Event name in the next format: 'HH:MM typeName'(correspond to 'typeName' and 'startTime' in SS response)
        EXPECTED: * 'More' link with chevron
        """
        pass

    def test_004_verify_event_card_subheader_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout
        EXPECTED: * 'Event Card' subheader consists of:
        EXPECTED: * 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (taken from SS response and correspond to 'eachWayFactorNum', 'eachWayFactorDen' and 'eachWayPlaces' attributes )
        EXPECTED: * 'Signposting Promotion' icon (if one or all of 'drilldownTagNames="EVFLAGEPR,EVFLAGFI,EVFLAGMB,EVFLAGBBL" attributes are received in SS response)
        EXPECTED: * 'CashOut' icon is shown on the right (if the event has 'cashoutAvail'='Y' in SS response)
        EXPECTED: * 'WATCH' icon
        """
        pass

    def test_005_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: * 'Event Card' body consists of:
        EXPECTED: * Runner Number (taken from 'runnerNumber' section in SS response)
        EXPECTED: * Silk (depens on runner number)
        EXPECTED: * Greyhounds Name (taken from 'name' section in SS response)
        EXPECTED: * 'Prive/Odds' button
        """
        pass
