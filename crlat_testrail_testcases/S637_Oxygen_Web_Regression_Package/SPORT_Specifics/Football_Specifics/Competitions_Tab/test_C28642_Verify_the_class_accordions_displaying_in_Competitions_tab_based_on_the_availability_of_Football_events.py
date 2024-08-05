import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28642_Verify_the_class_accordions_displaying_in_Competitions_tab_based_on_the_availability_of_Football_events(Common):
    """
    TR_ID: C28642
    NAME: Verify the class accordions displaying in 'Competitions' tab based on the availability of Football events
    DESCRIPTION: This test case verifies the class accordions displaying in 'Competitions' tab based on the availability of Football events
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Football' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. IDs that are typically set in **'A-ZClassIDs'** field: 115,592,591,595,100,109,104,103,102,101,108,106,105,136,137,134,135,138,139,548,133,132,131,130,145,146,147,148,149,140,142,141,144,143,118,119,116,117,114,112,113,111,110,127,128,129,123,124,125,126,120,652,122,121,584,179,178,172,173,170,171,176,177,174,175,587,586,589,181,182,183,180,159,158,157,154,155,152,153,150,151,168,167,169,163,164,165,166,160,161,162,69,68,715,73,74,71,72,70,724,79,76,75,78,77,82,83,84,85,80,81,730,89,88,87,86,739,91,92,90,95,96,93,94,743,744,745,740,741,742,98,97,99,603,16291
    PRECONDITIONS: 5. IDs that are typically set in **'InitialClassIDs'** field:
    PRECONDITIONS: * International (Class ID = 115)
    PRECONDITIONS: * UEFA Club Comps (Class ID = 165)
    PRECONDITIONS: * England (Class ID = 97)
    PRECONDITIONS: * Scotland (Class ID=158)
    PRECONDITIONS: * Spain (Class ID=166)
    PRECONDITIONS: * Italy (Class ID=120)
    PRECONDITIONS: * Germany (Class ID=105)
    PRECONDITIONS: * France (Class ID=102)
    PRECONDITIONS: * Netherlands (Class ID=140)
    PRECONDITIONS: * USA (Class ID=176)
    PRECONDITIONS: **(!)** 'CompetitionsFootball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_verify_popular_and_a_z_class_accordions_displaying(self):
        """
        DESCRIPTION: Verify 'Popular' and 'A-Z' class accordions displaying
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        """
        pass

    def test_002_trigger_undisplaying_all_events_for_any_class_in_the_openbet_system_ti_and_reload_the_page(self):
        """
        DESCRIPTION: Trigger undisplaying all events for any class in the OpenBet system (ti) and reload the page
        EXPECTED: 
        """
        pass

    def test_003_verify_lass_accordion_displaying_if_all_events_are_undisplayed(self):
        """
        DESCRIPTION: Verify Сlass accordion displaying if all events are undisplayed
        EXPECTED: The Class accordion is no longer shown in the list
        """
        pass

    def test_004_trigger_finishing_of_all_events_for_any_class_in_the_openbet_system_ti_and_reload_the_page(self):
        """
        DESCRIPTION: Trigger finishing of all events for any class in the OpenBet system (ti) and reload the page
        EXPECTED: 
        """
        pass

    def test_005_verify_lass_accordion_displaying_if_all_events_are_finished(self):
        """
        DESCRIPTION: Verify Сlass accordion displaying if all events are finished
        EXPECTED: The Class accordion is no longer shown in the list
        """
        pass

    def test_006_verify_content_of_the_page_when_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of the page when there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on the page
        """
        pass
