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
class Test_C2912283_TO_EDITBreadcrumbs_on_Races_Next_Races_event_details_page(Common):
    """
    TR_ID: C2912283
    NAME: [TO-EDIT]Breadcrumbs on <Races> 'Next Races' event details page
    DESCRIPTION: [TO-EDIT] - For both races the name of the event on EDP has a dropdown for meetings & when clicking on the Greyhound races Next Races tab or Today tab is open
    DESCRIPTION: This test case verifies breadcrumbs functionality on Horse Racing event details page when navigating from 'Next Races'
    PRECONDITIONS: 1. 'Next Races' module is configured in CMS on:
    PRECONDITIONS: - Horse Racing > 'Featured' tab
    PRECONDITIONS: - [NOT YET IMPLEMENTED] Horse Racing > 'Next Races' tab
    PRECONDITIONS: - Home Page > 'Next Races' tab
    PRECONDITIONS: 2. App is loaded
    PRECONDITIONS: 3. Home page > 'Next Races' tab is opened
    """
    keep_browser_open = True

    def test_001___tap_on_any_any_event_from_next_races__verify_breadcrumbs(self):
        """
        DESCRIPTION: - Tap on any any event from 'Next Races'
        DESCRIPTION: - Verify breadcrumbs
        EXPECTED: - Breadcrumbs are located below the page header
        EXPECTED: - Breadcrumbs are shown in a format '<Races>/Next Races'
        EXPECTED: - <Races> part is a highlighted hyperlink
        """
        pass

    def test_002_tap_on_raceshyperlink(self):
        """
        DESCRIPTION: Tap on <Races>hyperlink
        EXPECTED: <Races> landing page > 'Featured' tab (Horse Racing) or 'Today' tab ('Greyhounds') is opened
        """
        pass

    def test_003___go_to_home_page__next_races_tab__tap_on_any_event_from_next_races_tab__tap_on_any_event_time_tab__verify_breadcrumbs(self):
        """
        DESCRIPTION: - Go to 'Home' page > 'Next Races' tab
        DESCRIPTION: - Tap on any event from 'Next Races' tab
        DESCRIPTION: - Tap on any 'Event Time' tab
        DESCRIPTION: - Verify breadcrumbs
        EXPECTED: - Breadcrumbs are shown in a format '<Races>/Next Races'
        EXPECTED: - 'Horse Racing' part is a highlighted hyperlink
        """
        pass

    def test_004_tap_on_races_hyperlink(self):
        """
        DESCRIPTION: Tap on <Races> hyperlink
        EXPECTED: 'Horse Racing' landing page > 'Featured' tab (Horse Racing) or 'Today' tab ('Greyhounds') is opened
        """
        pass

    def test_005_repeat_steps_1_4_for__horse_racing__featured_tab__next_races_modulenot_yet_implemented__horse_racing__next_races_tab__greyhounds__today_tab__next_races_module(self):
        """
        DESCRIPTION: Repeat steps 1-4 for:
        DESCRIPTION: - Horse Racing > 'Featured' tab > 'Next Races' module
        DESCRIPTION: [NOT YET IMPLEMENTED]- Horse Racing > 'Next Races' tab
        DESCRIPTION: - Greyhounds > 'Today' tab > 'Next Races' module
        EXPECTED: 
        """
        pass
