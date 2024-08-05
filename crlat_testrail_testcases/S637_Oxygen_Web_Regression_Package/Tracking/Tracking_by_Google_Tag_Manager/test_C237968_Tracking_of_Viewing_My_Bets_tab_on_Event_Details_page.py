import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C237968_Tracking_of_Viewing_My_Bets_tab_on_Event_Details_page(Common):
    """
    TR_ID: C237968
    NAME: Tracking of Viewing 'My Bets' tab on Event Details page
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer due clicking on 'My Bets' tab within the Event Details page.
    DESCRIPTION: Jira ticket: BMA-19137 Google Analytics (Blast) – View ‘My Bets’
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * User has available Open bets
    PRECONDITIONS: **Note**:
    PRECONDITIONS: For changing number of Open Bets in the 'My Bets (x)' tab
    PRECONDITIONS: * (x) decrease by one: for COMB aligned bet - make full cash out for open bet
    PRECONDITIONS: * (x) increase by one: Place a bet using selection from the same event
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_003_navigate_to_the_football_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Football Event Details page
        EXPECTED: * 'Markets' tab is opened by default
        EXPECTED: * 'My Bets' tab is shown on Event Details page
        """
        pass

    def test_004_click_on_my_bets_tab(self):
        """
        DESCRIPTION: Click on 'My Bets' tab
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_005_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'content',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'event page - my bets (x)',
        EXPECTED: 'eventID': '123456'
        EXPECTED: 'location': 'event page'
        EXPECTED: });
        """
        pass

    def test_006_verify_parameters_that_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that present in current object in 'dataLayer'
        EXPECTED: * eventLabel = (x) is the number of Open Bets (present in the 'My Bets (x)' title)
        EXPECTED: * eventID = the unique Openbet Event ID for the event being viewed
        EXPECTED: * ‘event action’ =  'click'
        EXPECTED: * ‘location’ = ‘event page’
        """
        pass

    def test_007_change_the_number_of_open_bets_in_the_my_bets_x_tabsee_note_from_preconditions(self):
        """
        DESCRIPTION: Change the number of Open Bets in the 'My Bets (x)' tab
        DESCRIPTION: (see **Note** from Preconditions)
        EXPECTED: 
        """
        pass

    def test_008_change_focus_from_my_bets_x_tab_click_on_some_another_tab_on_event_details_page(self):
        """
        DESCRIPTION: Change focus from 'My Bets (x)' tab (click on some another tab on Event Details page)
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps 4-5
        EXPECTED: 
        """
        pass

    def test_010_verify_eventlabel_parameter(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter
        EXPECTED: 'eventLabel' : 'event page - my bets (x)',
        EXPECTED: (x) - decreased by one
        """
        pass
