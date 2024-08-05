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
class Test_C28931_Verify_Daily_Racing_Special_Event_Types(Common):
    """
    TR_ID: C28931
    NAME: Verify 'Daily Racing Special' Event Types
    DESCRIPTION: This test case verifies which events are related to the 'Daily Racing Special' events and how they should be displayed in the 'Oxygen' application
    PRECONDITIONS: To retrieve an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: Horse Racing **categoryId**=21
    PRECONDITIONS: **Class id** = 227 - HR specails
    PRECONDITIONS: **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load 'Oxygen' application
        EXPECTED: 
        """
        pass

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: 1.  'By Meeting' sorting type is selected by default
        EXPECTED: 2.  'Next 4 Races' is displayed
        """
        pass

    def test_004_verify_special_event_types(self):
        """
        DESCRIPTION: Verify special event types
        EXPECTED: 4 special event types are displayed:
        EXPECTED: *   Enhanced Multiples
        EXPECTED: *   Price Bomb
        EXPECTED: *   Mobile Exclusive
        EXPECTED: *   Winning Distances
        """
        pass

    def test_005_verify_special_events_displaying(self):
        """
        DESCRIPTION: Verify special events displaying
        EXPECTED: 1.  Special events are displayed under 'Today' tab only
        EXPECTED: 2.  Special events are shown under 'Next 4 Races' module
        """
        pass

    def test_006_verify_event_type_names(self):
        """
        DESCRIPTION: Verify event type names
        EXPECTED: the following 'typeName' attributes are displayed:
        EXPECTED: 1.  **'typeName'**='Enhanced Multiples'
        EXPECTED: 2.  **'typeName'**='Price Bomb'
        EXPECTED: 3.  **'typeName'**='Mobile Exclusive'
        EXPECTED: 4.  **'typeName'**='Winning Distances
        """
        pass

    def test_007_verify_event_types_order(self):
        """
        DESCRIPTION: Verify event types order
        EXPECTED: 1.
        EXPECTED: 'Winning Distances' are always displayed at the bottom of the list of special events
        EXPECTED: 2.
        EXPECTED: 'Enhanced Multiples', 'Price Bomb' and 'Mobile Exclusive' are displayed in alphabetical A-Z order
        """
        pass

    def test_008_verify_special_events_when_they_are_not_available(self):
        """
        DESCRIPTION: Verify special events when they are not available
        EXPECTED: If event types are not available -&gt; sections should not be shown
        """
        pass
