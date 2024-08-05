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
class Test_C1288313_Common_breadcrumbs_UI_and_navigation_for_Big_Competition(Common):
    """
    TR_ID: C1288313
    NAME: Common breadcrumbs UI and navigation for Big Competition
    DESCRIPTION: This test case verifies common breadcrumbs UI and navigation for Big Competition
    PRECONDITIONS: Have a big competition already created with at least one tab, one sub-tab and one module.
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section_in_cms(self):
        """
        DESCRIPTION: Go to Big Competition section in CMS
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_tap_on_a_big_competition_already_created(self):
        """
        DESCRIPTION: Tap on a 'Big competition' already created
        EXPECTED: A new window is loaded, displaying the configuration of tabs previously created
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name
        """
        pass

    def test_004_tap_on_the_tab_already_created(self):
        """
        DESCRIPTION: Tap on the 'Tab' already created
        EXPECTED: Respective tab landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name > 'Tabs page' name
        """
        pass

    def test_005_tap_on_the_sub_tab_already_created(self):
        """
        DESCRIPTION: Tap on the 'Sub-tab' already created
        EXPECTED: Respective sub-tab landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name > 'Tabs page' name > 'Sub-tab' name
        """
        pass

    def test_006_tap_on_the_module_already_created(self):
        """
        DESCRIPTION: Tap on the 'Module' already created
        EXPECTED: Respective module landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name > 'Tabs page' name > 'Sub-tab' name> 'Module' name
        """
        pass

    def test_007_tap_on_sub_tab_from_family_tree(self):
        """
        DESCRIPTION: Tap on 'Sub-tab' from family tree
        EXPECTED: Respective sub-tab landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name > 'Tabs page' name > 'Sub-tab' name
        """
        pass

    def test_008_return_to_step_6tap_on_the_tab_from_family_tree(self):
        """
        DESCRIPTION: Return to step #6:
        DESCRIPTION: Tap on the 'Tab' from family tree
        EXPECTED: Respective sub-tab landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name > 'Tabs page' name
        """
        pass

    def test_009_return_to_step_6tap_on_a_big_competition_from_family_tree(self):
        """
        DESCRIPTION: Return to step #6:
        DESCRIPTION: Tap on a 'Big competition' from family tree
        EXPECTED: Respective sub-tab landing page is loaded
        EXPECTED: A 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name
        """
        pass
