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
class Test_C1799766_Tracking_of_clicking_on_View_Full_Race_Card_link_in_Next_Races_section_at_the_Homepage_and_Races_module_at_the_Featured_section(Common):
    """
    TR_ID: C1799766
    NAME: Tracking of clicking on 'View Full Race Card' link in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View Full Race Card' link in 'Next Races' section at the Homepage and 'Races' module at the 'Featured' section.
    DESCRIPTION: Need to run the test case on Desktop.
    DESCRIPTION: **Need to be updated: Ladbrokes in Featured module created by Race Type ID 'More' = 'View Full Race Card**
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

    def test_002_scroll_the_page_down_to_the_next_races_section(self):
        """
        DESCRIPTION: Scroll the page down to the 'Next Races' section
        EXPECTED: * 'Next Races' section is displayed on the Homepage below 'In-Play & Live Stream' section
        EXPECTED: * Event cards are displayed within 'Next Races' carousel
        EXPECTED: * 'View Full Race Card' link is displayed below every event card
        """
        pass

    def test_003_click_on_view_full_race_card_link_below_any_event_card_within_next_races_section(self):
        """
        DESCRIPTION: Click on 'View Full Race Card' link below any event card within 'Next Races' section
        EXPECTED: User is navigated to 'Horse Racing' Details page of the particular event
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
        EXPECTED: 'eventLabel' : 'full race card - << EVENT >>' //e.g. full race card - 2.30 Ascot
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_clicking_on_view_full_race_card_link_for_another_card(self):
        """
        DESCRIPTION: Repeat steps 3-4 clicking on 'View Full Race Card' link for another card
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_3_5_for_races_module_in_featured_section_on_the_homepage_cms_configurable_see_preconditions(self):
        """
        DESCRIPTION: Repeat steps 3-5 for 'Races' module in 'Featured' section on the Homepage (CMS configurable, see preconditions)
        EXPECTED: 
        """
        pass
