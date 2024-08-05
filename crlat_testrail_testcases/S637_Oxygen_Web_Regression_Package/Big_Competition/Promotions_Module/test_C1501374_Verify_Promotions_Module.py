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
class Test_C1501374_Verify_Promotions_Module(Common):
    """
    TR_ID: C1501374
    NAME: Verify Promotions Module
    DESCRIPTION: This test case verifies Promotions Module
    PRECONDITIONS: - Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: - 'Promotions' module should be created within Promotions tab > Big Competition
    PRECONDITIONS: - Promotions should be added/correctly configured in CMS > Promotions (for more detailed steps please use the next TC - https://ladbrokescoral.testrail.com/index.php?/cases/view/29311&group_by=cases:section_id&group_order=asc&group_id=4103 )
    PRECONDITIONS: - The show promotions on Big Competition should be checked in CMS ('Show on Competition' field > e.g. 'World Cup' check box) > Promotions > Show on Competition option (for more detailed steps please use the next TC https://ladbrokescoral.testrail.com/index.php?/cases/view/1501591 )
    """
    keep_browser_open = True

    def test_001_load_oxygen_page(self):
        """
        DESCRIPTION: Load Oxygen page
        EXPECTED: Application is loaded
        """
        pass

    def test_002_go_to_big_competition_eg_world_cup_page(self):
        """
        DESCRIPTION: Go to Big Competition (e.g. World Cup) page
        EXPECTED: * Big Competition (e.g. World Cup) page is opened
        EXPECTED: * Featured tab is opened by default
        """
        pass

    def test_003_go_to_promotions_module(self):
        """
        DESCRIPTION: Go to Promotions Module
        EXPECTED: Promotions Module is opened
        """
        pass

    def test_004_verify_promotions_page(self):
        """
        DESCRIPTION: Verify Promotions page
        EXPECTED: 'Promotions' page consists of:
        EXPECTED: - 'Back' button
        EXPECTED: - 'Promotions' page title
        EXPECTED: - Page content
        EXPECTED: - Section content
        """
        pass

    def test_005_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: The section consists of:
        EXPECTED: - Promotion image
        EXPECTED: - Section title
        EXPECTED: - Short description
        EXPECTED: - 'More info' button
        """
        pass

    def test_006_verify_presence_of_added_promotions(self):
        """
        DESCRIPTION: Verify presence of added Promotions
        EXPECTED: - Only added Promotions for Big Competition module are shown on 'Promotions' page
        EXPECTED: - Promotion is displayed within the correctly uploaded image
        EXPECTED: - All data is displayed according to CMS
        """
        pass
