import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C491859_To_EditVerify_loading_DOM_elements_on_In_Play_page(Common):
    """
    TR_ID: C491859
    NAME: [To Edit]Verify loading DOM elements on 'In-Play' page
    DESCRIPTION: This test case verifies loading DOM elements on 'In-Play' page
    DESCRIPTION: **TO EDIT:**
    DESCRIPTION: The structure was changed. Currently, we have 'accordion' container that loads when accordion is collapsed and contains <header> tags only. After expanding the accordions the new <accordion-body> tags are added in 'accordion' container.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * Open Dev Tools -> Elements tab in order to check DOM elements
    """
    keep_browser_open = True

    def test_001_choose_select_an_element_in_page_to_inspect_option_in_dev_tools_and_hover_on_expanded_sport_competition(self):
        """
        DESCRIPTION: Choose 'Select an element in page to inspect' option in Dev tools and hover on expanded <Sport> competition
        EXPECTED: * Elements with HTML tags **<header>**, **<div>**, **<section>** with all acosiated data are loaded in DOM structure of the page
        """
        pass

    def test_002_choose_select_an_element_in_page_to_inspect_option_in_dev_tools_and_hover_on_collapsed_sport_competition(self):
        """
        DESCRIPTION: Choose 'Select an element in page to inspect' option in Dev tools and hover on collapsed <Sport> competition
        EXPECTED: * Only elements with HTML tag **<header>** is loaded in DOM structure of the page
        """
        pass

    def test_003_expand_collapsed_competition_and_repeat_step_1(self):
        """
        DESCRIPTION: Expand collapsed competition and repeat step 1
        EXPECTED: * Elements with HTML tags **<header>**, **<div>**, **<section>** with all acosiated data are loaded in DOM structure of the page
        """
        pass

    def test_004_repeat_steps_1_3_for_upcoming_sectiontab(self):
        """
        DESCRIPTION: Repeat steps 1-3 for Upcoming section/tab
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_4_on_homepage__in_play_tab_for_mobiletablet_homepage__live_stream_tab_for_mobiletablet_homepage__live_stream_page_from_sports_menu_ribbon_or_main_navigation_menu_sports_landing_page__in_play_tab_homepage__in_play__live_stream_section_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-4 on:
        DESCRIPTION: * Homepage > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Live Stream' tab **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Live Stream' page from Sports Menu Ribbon or 'Main Navigation' menu
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section **For Desktop**
        EXPECTED: 
        """
        pass
