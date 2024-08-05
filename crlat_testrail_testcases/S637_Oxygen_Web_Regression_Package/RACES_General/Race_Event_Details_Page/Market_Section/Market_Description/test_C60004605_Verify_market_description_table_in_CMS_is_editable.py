import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60004605_Verify_market_description_table_in_CMS_is_editable(Common):
    """
    TR_ID: C60004605
    NAME: Verify market description table in CMS is editable
    DESCRIPTION: This test case verifies market description table in CMS is editable
    PRECONDITIONS: 1: CMS access should be available
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        pass

    def test_002_navigate_to_racing_edp_template_and_edit_the_market_description_table(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and edit the Market description table
        EXPECTED: User should be able to Edit and save the changes successfully
        """
        pass
