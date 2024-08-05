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
class Test_C60004608_Verify_adding_New_Market_template_Market_Description(Common):
    """
    TR_ID: C60004608
    NAME: Verify adding New Market template- Market Description
    DESCRIPTION: Verify that as an Admin role user has access to add New Market template to the Market Description table
    PRECONDITIONS: 1: User should have CMS access
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        pass

    def test_002_navigate_to_racing_edp_template_and_add_new_market_to_the_market_description_table(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and add new market to the Market description table
        EXPECTED: User should be able to Add new market to the Market description table
        """
        pass
