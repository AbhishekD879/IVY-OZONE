import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C1168276_Verify_Big_Competition_section(Common):
    """
    TR_ID: C1168276
    NAME: Verify Big Competition section
    DESCRIPTION: This test case verifies elements of new Competition Homepage
    PRECONDITIONS: Have one or more competitions already created.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_big_competition_section(self):
        """
        DESCRIPTION: Go to Big Competition section
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_verify_presence_of_the_upper_elements_for_the_big_competition_section(self):
        """
        DESCRIPTION: Verify presence of the upper elements for the Big Competition section
        EXPECTED: The following elements are present:
        EXPECTED: * '+ Create Competition' button
        EXPECTED: * 'Download CSV' button
        EXPECTED: * 'Search for Competition' area
        """
        pass

    def test_004_verify_presence_of_the_middle_components_for_the_big_competition_section(self):
        """
        DESCRIPTION: Verify presence of the middle components for the Big Competition section
        EXPECTED: The following elements are present on the grid:
        EXPECTED: * 'Competition name'
        EXPECTED: * 'URL Structure'
        EXPECTED: * 'Active'
        EXPECTED: * 'Actions'
        """
        pass

    def test_005_verify_each_competition_line_structure(self):
        """
        DESCRIPTION: Verify each competition line structure
        EXPECTED: The following elements are present:
        EXPECTED: * 'Number'
        EXPECTED: * Respective 'Competition name'
        EXPECTED: * Respective 'URL Structure'
        EXPECTED: * 'Checkbox', which displays visibility status of competition
        EXPECTED: * 'Prohibited sign' button, which allows to delete competition
        EXPECTED: * 'Pen' button, which allows to edit competition
        """
        pass
