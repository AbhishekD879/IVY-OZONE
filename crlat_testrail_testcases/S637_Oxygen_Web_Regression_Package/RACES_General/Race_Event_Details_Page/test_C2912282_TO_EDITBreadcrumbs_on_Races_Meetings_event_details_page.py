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
class Test_C2912282_TO_EDITBreadcrumbs_on_Races_Meetings_event_details_page(Common):
    """
    TR_ID: C2912282
    NAME: [TO-EDIT]Breadcrumbs on <Races> 'Meetings' event details page
    DESCRIPTION: [TO-EDIT] - For both races the name of the event on EDP has a dropdown for meetings & when clicking on the Greyhound races Next Races tab or Today tab is open
    DESCRIPTION: This test case verifies breadcrumbs functionality on Racing event details page when navigating to 'Meetings' event details page
    PRECONDITIONS: - App is loaded
    PRECONDITIONS: - Horse Racing landing page > 'Featured' tab is opened for Horse racing EDP testing
    PRECONDITIONS: - Greyhounds landing page ('Today' tab) is opened for Greyhounds EDP testing
    """
    keep_browser_open = True

    def test_001___tap_on_any_event_from_featured_except_for_next_racesantepost_tabs__greyhounds_tap_on_any_event_from_today_except_for_next_racestomorrowfuture(self):
        """
        DESCRIPTION: - Tap on any event from Featured (except for 'Next Races')/'Antepost' tabs
        DESCRIPTION: - Greyhounds: Tap on any event from Today (except for 'Next Races')/Tomorrow/Future
        EXPECTED: Event details page of a corresponding event is opened
        """
        pass

    def test_002_verify_breadcrumbs_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify breadcrumbs displaying on the page
        EXPECTED: - Breadcrumbs are located below the page header
        EXPECTED: - Breadcrumbs are shown in a format '<Races>/[Event Name]'
        EXPECTED: - <Races> part is a highlighted hyperlink
        """
        pass

    def test_003_tap_on_races_hyperlink(self):
        """
        DESCRIPTION: Tap on '<Races> hyperlink
        EXPECTED: <Races> landing page is opened:
        EXPECTED: - 'Featured' tab for Horse Racing
        EXPECTED: - 'Today' tab for Greyhounds
        """
        pass

    def test_004___horse_racing_tap_on_any_event_from_featured_except_for_next_racesantepost_tabs__greyhounds_tap_on_any_event_from_today_except_for_next_racestomorrowfuture__tap_on_any_other_event_time_tab_on_event_details_page__verify_breadcrumbs(self):
        """
        DESCRIPTION: - Horse Racing: Tap on any event from Featured (except for 'Next Races')/'Antepost' tabs
        DESCRIPTION: - Greyhounds: Tap on any event from Today except for 'Next Races')/Tomorrow/Future
        DESCRIPTION: - Tap on any other 'Event Time' tab on event details page
        DESCRIPTION: - Verify breadcrumbs
        EXPECTED: - Breadcrumbs remain shown in a format <Races>/[Event Name]'
        EXPECTED: - <Races> part is a highlighted hyperlink
        """
        pass

    def test_005_tap_on_races_hyperlink(self):
        """
        DESCRIPTION: Tap on <Races> hyperlink
        EXPECTED: <Races> landing page is opened:
        EXPECTED: - 'Featured' tab for Horse Racing
        EXPECTED: - 'Today' tab for Greyhounds
        """
        pass
