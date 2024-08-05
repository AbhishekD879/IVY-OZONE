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
class Test_C9346562_Verify_the_data_displaying_on_the_Competitions_tab_based_on_the_availability_of_Tennis_events(Common):
    """
    TR_ID: C9346562
    NAME: Verify the data displaying on the 'Competitions' tab based on the availability of Tennis events
    DESCRIPTION: This test case verifies the data displaying in the 'Competitions' tab based on the availability of Tennis events
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Tennis Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Tennis' and put class ID's in 'InitialClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 5. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 6. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_002_trigger_undisplaying_all_events_for_any_league_type_in_the_openbet_system_ti_and_reload_the_page(self):
        """
        DESCRIPTION: Trigger undisplaying all events for any league (type) in the OpenBet system (ti) and reload the page
        EXPECTED: 
        """
        pass

    def test_003_verify_league_type_displaying_if_all_events_are_undisplayed(self):
        """
        DESCRIPTION: Verify League (Type) displaying if all events are undisplayed
        EXPECTED: The League (Type) is no longer shown in the list
        """
        pass

    def test_004_trigger_finishing_of_all_events_for_any_any_league_type_in_the_openbet_system_ti_and_reload_the_page(self):
        """
        DESCRIPTION: Trigger finishing of all events for any any league (type) in the OpenBet system (ti) and reload the page
        EXPECTED: 
        """
        pass

    def test_005_verify_any_league_type_displaying_if_all_events_are_finished(self):
        """
        DESCRIPTION: Verify any League (Type) displaying if all events are finished
        EXPECTED: The League (Type) is no longer shown in the list
        """
        pass

    def test_006_verify_content_of_the_page_when_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of the page when there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on the page
        """
        pass
