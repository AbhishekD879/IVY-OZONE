import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9770753_Verify_excluding_of_identical_events_from_modules_on_Featured_tab_in_case_its_already_present_in_one_of_them(Common):
    """
    TR_ID: C9770753
    NAME: Verify excluding of identical events from modules on 'Featured' tab in case it's already present in one of them
    DESCRIPTION: This test case verifies excluding of identical events from modules on 'Featured' tab in case it's already present in one of them
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and the 'Featured' tab is selected
    PRECONDITIONS: 3. Make sure that at least one identical event is set in 'Highlights Carousel', 'In-Play' and 'Featured' modules
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'Highlights Carousel' module should be enabled in CMS > Sports Configs > Structure > Highlight Carousel
    PRECONDITIONS: - 'Highlights Carousel' module should be be 'Active' in CMS > Sports Pages > Homepage > Highlights Carousel module
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - 'Feature' module should be created in CMS > Featured Tab Modules
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    PRECONDITIONS: If the same event is set for 'Highlights Carousel', 'In-Play' and 'Featured' activated modules be aware that event will be displayed according to the following prioritization:
    PRECONDITIONS: - 'Highlights Carousel' module
    PRECONDITIONS: - 'In-Play' module
    PRECONDITIONS: - 'Featured' module
    PRECONDITIONS: It means the event that is present in the first module will be excluded from the rest.
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_event_see_preconditions_in_highlights_carousel_module(self):
        """
        DESCRIPTION: Verify displaying of the event (see preconditions) in 'Highlights Carousel' module
        EXPECTED: * 'Highlights Carousel' module is displayed in 'Featured' tab
        EXPECTED: * The event is present in the 'Highlights Carousel' module
        """
        pass

    def test_002_verify_displaying_of_the_event_in_in_play_module(self):
        """
        DESCRIPTION: Verify displaying of the event in 'In-Play' module
        EXPECTED: * The event is excluded from the 'In-Play' module and is NOT displayed there
        EXPECTED: * The whole 'In-Play' module is NOT displayed in case it contains only one event
        """
        pass

    def test_003_verify_displaying_of_the_event_in_the_featured_module(self):
        """
        DESCRIPTION: Verify displaying of the event in the 'Featured' module
        EXPECTED: * The event is excluded from the 'Featured' module and is NOT displayed there
        EXPECTED: * The whole 'Featured' module is NOT displayed in case it contains only one event
        """
        pass

    def test_004_go_to_cms_and_deactivate_the_highlights_carousel_module(self):
        """
        DESCRIPTION: Go to CMS and deactivate the 'Highlights Carousel' module
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_005_back_to_oxygen_app__featured_tab_and_verify_displaying_of_the_event_within_in_play_module(self):
        """
        DESCRIPTION: Back to Oxygen app > 'Featured' tab and verify displaying of the event within 'In-Play' module
        EXPECTED: * 'Highlights Carousel' module disappears from the page
        EXPECTED: * The event appears within 'In-Play' module
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: 
        """
        pass

    def test_007_go_to_cms_and_deactivate_the_in_play_module(self):
        """
        DESCRIPTION: Go to CMS and deactivate the 'In-Play' module
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_back_to_oxygen_app__featured_tab_and_verify_displaying_of_the_event_within_in_play_module(self):
        """
        DESCRIPTION: Back to Oxygen app > 'Featured' tab and verify displaying of the event within 'In-Play' module
        EXPECTED: * 'In-Play' module disappears from the page
        EXPECTED: * The event appears within 'Featured' module
        """
        pass
