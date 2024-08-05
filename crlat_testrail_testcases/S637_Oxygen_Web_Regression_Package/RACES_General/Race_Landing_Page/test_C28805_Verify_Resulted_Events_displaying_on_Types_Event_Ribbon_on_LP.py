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
class Test_C28805_Verify_Resulted_Events_displaying_on_Types_Event_Ribbon_on_LP(Common):
    """
    TR_ID: C28805
    NAME: Verify Resulted Events displaying on Type's Event Ribbon on LP
    DESCRIPTION: This test case verifies how resulted events will be shown on Type's Event Ribbon
    DESCRIPTION: Test case is applicable for HR and GH landing pages
    PRECONDITIONS: In order to retrieve all **Event** outcomes for the Classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XX - category id*
    PRECONDITIONS: *
    PRECONDITIONS: ZZZZ is a comma separated list of Class ID's
    PRECONDITIONS: *   *YYYY1-MM1-DD1 is lower time bound*
    PRECONDITIONS: *   *YYYY2-MM2-DD2 is higher time bound*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: **isFinished = 'true'** on event level - to check whether event is finished
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application.
        EXPECTED: Application is opened.
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_race_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap <Race> icon.
        EXPECTED: <Race> landing page is opened.
        """
        pass

    def test_003_in_ti_trigger_results_for_eg_1_resulted_race_and_1_race_off_or_2_resulted_races_for_some_events_inside_1_type(self):
        """
        DESCRIPTION: In TI trigger Results (for e.g. 1 resulted race and 1 race off, or 2 resulted races) for some events inside 1 Type.
        EXPECTED: 
        """
        pass

    def test_004_reload_the_page(self):
        """
        DESCRIPTION: Reload the page.
        EXPECTED: The Races ribbon (where the races are shown) should move to the left as the races are being resulted.
        EXPECTED: The default view (when the page is loaded) should show 2 last resulted races if available.
        EXPECTED: Note: if there are only 1 or 2 races remaining, then more than 2 resulted races will be displayed.
        """
        pass

    def test_005_swipe_left(self):
        """
        DESCRIPTION: Swipe Left.
        EXPECTED: Previous resulted events are shown.
        EXPECTED: All events have 'Resulted' icon next to greyed time off.
        EXPECTED: All events are clickable and lead to Results tab with current event results.
        """
        pass
