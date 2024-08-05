import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C1108264_NEED_TO_BE_UPDATED_Verify_layout_of_module_created_by_Greyhounds_Type_Id_on_Featured_tab(Common):
    """
    TR_ID: C1108264
    NAME: [NEED TO BE UPDATED] Verify layout of module created by Greyhounds Type Id on Featured tab
    DESCRIPTION: This case verifies Race Type Id layout on Featured tab
    DESCRIPTION: TO BE UPDATED
    DESCRIPTION: **NOTE** Ladbrokes - step 4 - 'SEE ALL' and 'MORE' hyperlink ("View Full Race Card" only on CORAL  DESTOP)
    DESCRIPTION: AUTOTEST [C1108264]
    PRECONDITIONS: Configure on CMS a <Race Type Id> for Greyhounds under Featured Tab Modules
    PRECONDITIONS: NOTE: This test case should check also Virtual Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen App
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id_from_pre_conditions(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID from pre-conditions
        EXPECTED: * 'Feature' tab is selected by default
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_004_observe_the_layout_of_created_greyhounds_module(self):
        """
        DESCRIPTION: Observe the layout of created Greyhounds module
        EXPECTED: * Module 'Title'
        EXPECTED: * Below title there should be present a box for each event with following components present:
        EXPECTED: - Time, Venue
        EXPECTED: - Each Way: x odds - places 1,2 - **only for mobile/tablet;**
        EXPECTED: * Below there should be present greyhound selections with following components:
        EXPECTED: - Color square box with number of greyhound, name of greyhound and price
        EXPECTED: * In the footer of box there should be present hyperlink named "View Full Race Card"
        """
        pass

    def test_005_observe_correctness_of_layout_among_all_event_boxes_present_in_the_featured_tab(self):
        """
        DESCRIPTION: Observe correctness of layout among all event boxes present in the featured tab
        EXPECTED: All layout components described in step #2 should be all aligned
        """
        pass
