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
class Test_C2031419_Tracking_of_clicking_on_Full_Race_Card_link_in_Next_Races_widget_on_the_HR_Landing_page(Common):
    """
    TR_ID: C2031419
    NAME: Tracking of clicking on 'Full Race Card' link in 'Next Races' widget on the HR Landing page
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Full Race Card' link in 'Next Races' widget on the HR Landing page
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

    def test_002_navigate_to_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to the 'Horse Racing' Landing page
        EXPECTED: * Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Next Races' widget is shown as the carousel in 3rd column or below main content (depends on screen resolution)
        EXPECTED: * 'Full Race Card' link is displayed below every event card in 'Next Races' widget
        """
        pass

    def test_003_click_on_full_race_card_link(self):
        """
        DESCRIPTION: Click on 'Full Race Card' link
        EXPECTED: User is navigated to 'Horse Racing' Details page of the particular event
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'widget',
        EXPECTED: 'eventAction' : 'next races',
        EXPECTED: 'eventLabel' : 'full race card - << EVENT >>' //e.g. full race card - 2.30 Ascot
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_clicking_on_full_race_card_link_for_another_card(self):
        """
        DESCRIPTION: Repeat steps 3-4 clicking on 'Full Race Card' link for another card
        EXPECTED: 
        """
        pass
