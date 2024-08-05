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
class Test_C1799767_Tracking_of_clicking_on_View_All_Horse_Racing_Events_link_in_Next_Races_section_at_the_Homepage_and_Races_module_at_the_Featured_section(Common):
    """
    TR_ID: C1799767
    NAME: Tracking of clicking on 'View All Horse Racing Events' link in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View All Horse Racing Events' link in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section.
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
        EXPECTED: * Footer with 'View All Horse Racing Events' link is displayed below event cards in 'Next Races' section
        """
        pass

    def test_003_click_on_the_view_all_horse_racing_events_link(self):
        """
        DESCRIPTION: Click on the 'View All Horse Racing Events' link
        EXPECTED: User is navigated to 'Horse Racing' Landing page
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'featured races',
        EXPECTED: 'eventLabel' : 'view all'
        EXPECTED: })
        """
        pass

    def test_005_scroll_the_page_down_to_the_featured_section_and_make_sure_that_races_module_is_displayed_cms_configurable_see_preconditions(self):
        """
        DESCRIPTION: Scroll the page down to the 'Featured' section and make sure that 'Races' module is displayed (CMS configurable, see preconditions)
        EXPECTED: * 'Races' module is displayed in 'Featured' section
        EXPECTED: * Event cards are displayed within 'Races' carousel
        EXPECTED: * Footer with link is displayed below event cards in 'Races' module
        """
        pass

    def test_006_click_on_the_link_at_the_footer_in_races_module(self):
        """
        DESCRIPTION: Click on the link at the footer in 'Races' module
        EXPECTED: User is navigated to the page set in CMS
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'featured races',
        EXPECTED: 'eventLabel' : 'view all'
        EXPECTED: })
        """
        pass
