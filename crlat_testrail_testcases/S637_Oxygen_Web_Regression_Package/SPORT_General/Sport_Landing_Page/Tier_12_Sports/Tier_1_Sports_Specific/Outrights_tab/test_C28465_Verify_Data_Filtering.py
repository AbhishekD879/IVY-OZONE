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
class Test_C28465_Verify_Data_Filtering(Common):
    """
    TR_ID: C28465
    NAME: Verify Data Filtering
    DESCRIPTION: This test case verifies data filtering
    DESCRIPTION: **JIRA Tickets** :
    DESCRIPTION: * BMA-5106 'Market Filter for In-Play Events'
    DESCRIPTION: * BMA-9146 'Apply new design to Outrights and Enhanced Multiples'
    DESCRIPTION: * BMA-17707 'Remove Cash Out icons from the accordions on the Outrights tab'
    DESCRIPTION: **NOTE** :
    DESCRIPTION: for Football Sport only, Outright' tab is removed from the module header into 'Competition Module Header' within 'Matches' tab
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XXX - is a comma separated list of **Class **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. For each Type retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&translationLang=LL&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   XXX - is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED: *   'Outrights' Events page is opened
        EXPECTED: *   Navigation is carried out smoothly
        """
        pass

    def test_004_verify_list_of_events_in_each_section(self):
        """
        DESCRIPTION: Verify list of events in each section
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20)
        EXPECTED: *   AND/OR **dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        pass

    def test_005_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'Cash out' label
        EXPECTED: 'CASH OUT' label is **NOT shown** next to event Type name in any case for Outright tab
        """
        pass
