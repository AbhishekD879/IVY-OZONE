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
class Test_C28843_ADD_Verify_Event_Details_Page_of_unavailable_Race_events(Common):
    """
    TR_ID: C28843
    NAME: ADD Verify Event Details Page of unavailable <Race> events
    DESCRIPTION: This test case verifies <Races> event details page of an unavailable <Race> event
    PRECONDITIONS: To get an info about event use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_go_to_races_landing_page(self):
        """
        DESCRIPTION: Go to <Races> landing page
        EXPECTED: <Races> landing page is opened
        """
        pass

    def test_003_go_to_event_details_page_of_any_races_event(self):
        """
        DESCRIPTION: Go to event details page of any <Races> event
        EXPECTED: <Races> event details page is opened
        """
        pass

    def test_004_in_ti_undisplay_event_from_step_3(self):
        """
        DESCRIPTION: In TI: Undisplay event from Step 3
        EXPECTED: Event is undisplayed
        """
        pass

    def test_005_in_application_refresh_the_page(self):
        """
        DESCRIPTION: In application: Refresh the page
        EXPECTED: * <Races> header with 'Back' button is available
        EXPECTED: * "No markets are currently available for this event" text is displayed
        """
        pass
