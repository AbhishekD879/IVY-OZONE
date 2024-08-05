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
class Test_C29373_Verify_Module_Area(Common):
    """
    TR_ID: C29373
    NAME: Verify Module Area
    DESCRIPTION: This test case verifies Module area on the Feature tab (mobile/tablet) Featured section (desktop)
    DESCRIPTION: AUTOMATED [C13081439]
    PRECONDITIONS: 1. There are more than one event in the module section
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet device or Desktop
    PRECONDITIONS: **NOTE:** For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    """
    keep_browser_open = True

    def test_001_scroll_the_homepage_to_the_module_ribbon_tabs_section(self):
        """
        DESCRIPTION: Scroll the Homepage to the 'Module Ribbon Tabs' section
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default in the 'Module Ribbon Tabs' section
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_002_verifymodule_area(self):
        """
        DESCRIPTION: Verify 'Module Area'
        EXPECTED: 'Module Area' contains **Modules**
        """
        pass

    def test_003_verify_collapsingexpanding_of_module_header_using_down_chevron(self):
        """
        DESCRIPTION: Verify collapsing/expanding of Module header using 'Down' chevron
        EXPECTED: *   It is possible to expand the Module section using 'Down' chevrons
        EXPECTED: *   No chevron is displayed if the section is expanded
        EXPECTED: *   ''Down' chevron is displayed if the section is collapsed
        """
        pass

    def test_004_verify_collapsingexpanding_by_tappingclicking_onany_part_of_the_module_header(self):
        """
        DESCRIPTION: Verify collapsing/expanding by tapping/clicking on any part of the Module header
        EXPECTED: *   It is possible to collapse/expand Module section by tapping/clicking on any part of the Module header
        EXPECTED: *   No chevron is displayed if the section is expanded
        EXPECTED: *   ''Down' chevron is displayed if the section is collapsed
        """
        pass
