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
class Test_C1218065_Verify_Enhanced_multiples_carousel(Common):
    """
    TR_ID: C1218065
    NAME: Verify Enhanced multiples carousel
    DESCRIPTION: This test case verifies that event type 'Enhanced Multiples' will be displayed as carousel on Featured tab in the 'Oxygen' application
    DESCRIPTION: AUTOTEST: [C1503473]
    PRECONDITIONS: Event should be created with class_id = 227 > type_name =  |Enhanced Multiples|;
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: 'typeName'='Enhaced Multiples'
    PRECONDITIONS: 'classID' on event level to see class id for selected event type
    PRECONDITIONS: 'className' on event level to see class name where event belongs to
    PRECONDITIONS: 'name' on event level to see event name and local time
    PRECONDITIONS: rawIsOffCode="Y" , **isStarted="true",** **rawIsOffCode="-" - **on event level to see whether event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_horse_racing_home_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' Home page
        EXPECTED: 1. Horse Racing landing page is opened
        EXPECTED: 2. 'Featured' tab is opened
        """
        pass

    def test_003_verify_enhanced_multiples_module(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' module
        EXPECTED: 1. 'Enhanced Multiples' module is displayed as carousel
        EXPECTED: 2. 'Enhanced Multiples' module is expanded by default and "-" symbol should be displayed
        EXPECTED: 3. 'Enhanced Multiples' module is collapsed/expanded once tapped
        """
        pass

    def test_004_verify_content_of_the_card(self):
        """
        DESCRIPTION: Verify content of the card
        EXPECTED: 1. Header title (is taken from event "name" attribute from SS response);
        EXPECTED: 2. Selection name (is taken from outcome "name" attribute from SS response) ;
        EXPECTED: 4. Clickable Odds button (adds selection to the Betslip)
        """
        pass

    def test_005_verify_selections_ordering(self):
        """
        DESCRIPTION: Verify selections ordering
        EXPECTED: Selections are ordered by event 'startTime' attribute in asc order
        """
        pass

    def test_006_verify_event_attributes_starttime_and_eventstatuscode(self):
        """
        DESCRIPTION: Verify event attributes 'startTime' and 'eventStatusCode'
        EXPECTED: Only active events are displayed in the section ('eventStatusCode='A')
        """
        pass

    def test_007_verify_event_with_attributes_rawisoffcodey_or_isstatedtrue_and_rawisoffcode_(self):
        """
        DESCRIPTION: Verify event with attributes **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        EXPECTED: Started events disappear from the 'Enhanced Multiples' carousel
        """
        pass

    def test_008_verify_event_with_outcomestatuscodes(self):
        """
        DESCRIPTION: Verify event with outcomeStatusCode='S'
        EXPECTED: Suspended events disappear from the 'Enhanced Multiples' section
        """
        pass

    def test_009_verify_enhanced_multiples_carousel_when_all_events_are_started(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' carousel when all events are started
        EXPECTED: Carousel is no more displayed if there are no events to show
        """
        pass
