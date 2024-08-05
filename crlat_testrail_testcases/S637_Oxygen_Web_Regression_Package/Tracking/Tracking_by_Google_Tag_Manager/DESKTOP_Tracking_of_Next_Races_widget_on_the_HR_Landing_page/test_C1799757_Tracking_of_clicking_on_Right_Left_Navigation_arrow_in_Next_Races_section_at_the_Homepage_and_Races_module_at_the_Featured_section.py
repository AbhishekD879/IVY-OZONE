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
class Test_C1799757_Tracking_of_clicking_on_Right_Left_Navigation_arrow_in_Next_Races_section_at_the_Homepage_and_Races_module_at_the_Featured_section(Common):
    """
    TR_ID: C1799757
    NAME: Tracking of clicking on Right/Left Navigation arrow in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on Right/Left Navigation arrow in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Take a look at the following test case https://ladbrokescoral.testrail.com/index.php?/cases/view/29408 for creation 'Races' module in 'Featured' section by CMS.
    PRECONDITIONS: Links to CMS for different endpoints:
    PRECONDITIONS: DEV - https://coral-cms-dev0.symphony-solutions.eu/
    PRECONDITIONS: TST2 - https://coral-cms-tst2.symphony-solutions.eu/
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/
    PRECONDITIONS: HL - https://coral-cms-hl.symphony-solutions.eu/
    PRECONDITIONS: PROD - https://coral-cms.symphony-solutions.eu/
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_scroll_the_page_down_to_the_next_races_section_and_make_sure_that_several_event_cards_are_available_for_example_4(self):
        """
        DESCRIPTION: Scroll the page down to the 'Next Races' section and make sure that several event cards are available (for example 4)
        EXPECTED: * 'Next Races' section is displayed on the Homepage below 'In-Play & Live Stream' section
        EXPECTED: * Event cards are displayed within 'Next Races' carousel
        """
        pass

    def test_003_hover_the_mouse_over_event_cards_in_next_races_section_and_click_on_the_right_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'Next Races' section and click on the Right Navigation Arrow
        EXPECTED: Event cards are swiped to the left side
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'next races',
        EXPECTED: 'eventLabel' :  'navigate right'
        EXPECTED: })
        """
        pass

    def test_005_hover_the_mouse_over_event_cards_in_next_races_section_and_click_on_the_left_navigation_arrow(self):
        """
        DESCRIPTION: Hover the mouse over event cards in 'Next Races' section and click on the Left Navigation Arrow
        EXPECTED: Event cards are swiped to the right side
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'next races',
        EXPECTED: 'eventLabel' :  'navigate left'
        EXPECTED: })
        """
        pass

    def test_007_repeat_steps_3_6_for_races_module_in_featured_section_on_the_homepage_cms_configurable_see_preconditions(self):
        """
        DESCRIPTION: Repeat steps 3-6 for 'Races' module in 'Featured' section on the Homepage (CMS configurable, see preconditions)
        EXPECTED: 
        """
        pass
