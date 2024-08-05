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
class Test_C2031416_Tracking_of_clicking_on_Extra_Place_meeting_area_at_HR_Enhances_Races_widget(Common):
    """
    TR_ID: C2031416
    NAME: Tracking of clicking on Extra Place meeting area at 'HR Enhances Races' widget
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on Extra Place meeting area link at 'Virtuals' widget on HR Landing page.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_horse_race_landing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Race' Landing page
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'HR Enhances Races' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        """
        pass

    def test_003_click_on_the_extra_place_meeting_area_within_hr_enhances_races_widget(self):
        """
        DESCRIPTION: Click on the Extra Place meeting area within 'HR Enhances Races' widget
        EXPECTED: User is redirected to the HR Details page of a corresponding event once clicked
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'todays enhanced races',
        EXPECTED: 'eventLabel' : 'view event'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_for_another_extra_place_meeting(self):
        """
        DESCRIPTION: Repeat steps 3-4 for another Extra Place meeting
        EXPECTED: 
        """
        pass
