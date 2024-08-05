import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28929_Coral_Event_Section_Data(Common):
    """
    TR_ID: C28929
    NAME: [Coral] Event Section Data
    DESCRIPTION: This test case verifies event section data correctness on 'Special' tab
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8961 Horse Racing Specials Tab
    DESCRIPTION: AUTOTEST: [C527906]
    PRECONDITIONS: To retrieve an information from the Site Server use the following link:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   **'typeID' **on type level to see type id for Racing Specials
    PRECONDITIONS: *   **'classID'** on event level to see class id for selected event type
    PRECONDITIONS: *   **'className'** on event level to see class name where event belongs to
    PRECONDITIONS: *   **'name'** on event level to see event name and local time
    PRECONDITIONS: *   **'eachWayFactorNum', '****eachWayFactorDen', '****eachWayPlaces' **to check each-way terms correctness
    PRECONDITIONS: *   **'name'** on outcome level to see selection name
    PRECONDITIONS: *   **'PriceNum'** and **'PriceDen'** to see current odds in fractional format
    PRECONDITIONS: *   **'PriceDec' **to see current odds in decimal format
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_click__tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        pass

    def test_004_go_to_events_in_the_particular_module(self):
        """
        DESCRIPTION: Go to events in the particular module
        EXPECTED: Events are shown
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to the 'name' attribute on event level from the Site Server
        EXPECTED: Event start time is NOT shown near the event name (despite the fact when time is a part of event name)
        """
        pass

    def test_006_verify_event_date(self):
        """
        DESCRIPTION: Verify event date
        EXPECTED: Event date is shown near the event name
        """
        pass

    def test_007_verify_each_way_terms(self):
        """
        DESCRIPTION: Verify Each-way terms
        EXPECTED: Terms are displayed in the following format:
        EXPECTED: ***" Each Way: x/y odds - places z,j,k"***
        EXPECTED: where:
        EXPECTED: *   x = **eachWayFactorNum**
        EXPECTED: *   y= **eachWayFactorDen**
        EXPECTED: *   z,j,k = **eachWayPlaces**
        """
        pass

    def test_008_check_event_selections(self):
        """
        DESCRIPTION: Check event selections
        EXPECTED: Selections are listed under event name
        EXPECTED: Selection name and selection price/odds button are shown
        """
        pass

    def test_009_verify_selection_names(self):
        """
        DESCRIPTION: Verify selection names
        EXPECTED: Selection names correspond to the "name" attribute on selection level
        """
        pass

    def test_010_verify_priceodds_button_next_to_the_selection(self):
        """
        DESCRIPTION: Verify price/odds button next to the selection
        EXPECTED: Price/odds button is shown based on priceTypeCodes on market level:
        EXPECTED: - one LP button with actual price - when priceTypeCodes=LP
        EXPECTED: - one active SP button - when priceTypeCodes=SP
        EXPECTED: - one active LP button with actual price - when priceTypeCodes = LP,SP and price are available
        EXPECTED: - one active SP button with actual price - when priceTypeCodes = LP,SP and price are not available
        """
        pass

    def test_011_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selection is ordered by rules:
        EXPECTED: - by LP price from lowest to highest - when price is available
        EXPECTED: - by 'name' alphabetically in case prices are the same
        EXPECTED: - by 'name' alphabetically in case SP price
        """
        pass

    def test_012_check_adding__removal_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Check adding / removal selections to the Bet Slip
        EXPECTED: Adding / removal selections to the Bet Slip is performed correctly as for simple racing events
        """
        pass

    def test_013_check_bet_placement(self):
        """
        DESCRIPTION: Check bet placement
        EXPECTED: Bet placement is performed correctly
        """
        pass
