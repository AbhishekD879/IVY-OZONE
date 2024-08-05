import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1232381_Enhanced_Multiples_carousel_on_Pre_Match_EDP_when_the_event_becomes_live_for_Desktop(Common):
    """
    TR_ID: C1232381
    NAME: Enhanced Multiples carousel on Pre-Match EDP when the event becomes live for Desktop
    DESCRIPTION: This test case verifies Enhanced Multiples carousel on Pre-Match EDP when the event becomes live for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Navigate to Pre-match <Sports> Event Details Page and make sure that Enhanced Multiples events are present
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. **Pre-match events:**
    PRECONDITIONS: Event should not be started **(isStarted=false)**
    PRECONDITIONS: Event should **NOT** have attribute **isMarketBetInRun=true**
    PRECONDITIONS: 2. **Started events:**
    PRECONDITIONS: Event should have attribute **drilldownTagNames=EVFLAG_BL**
    PRECONDITIONS: Event should have attribute **isMarketBetInRun="true" **(on the any Market level)
    PRECONDITIONS: Event should have attribute **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
    PRECONDITIONS: 3. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XXX - is a comma-separated list of **Class **ID's;
    PRECONDITIONS: XX - sports **Category **ID
    PRECONDITIONS: X.XX - current supported version of the OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_enhanced_multiples_events(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' events
        EXPECTED: • 'Enhanced Multiples' events are displayed in the carousel below banner area
        EXPECTED: • Each event card in carousel contains label 'Enhanced' in the top left corner
        """
        pass

    def test_002_trigger_situation_when_event_becomes_live(self):
        """
        DESCRIPTION: Trigger situation when event becomes live
        EXPECTED: 'Enhanced Multiples' carousel with events is still displaying below Stats (if applicable) or 'Breadcrumbs' trail
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Enhanced Multiples' carousel with events is NOT displayed anymore
        """
        pass
