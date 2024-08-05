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
class Test_C25020344_Verify_that_Outrights_markets_are_displayed_on_Homepage_as_per_design(Common):
    """
    TR_ID: C25020344
    NAME: Verify that Outrights markets are displayed on Homepage as per design
    DESCRIPTION: This test case verifies that Outrights markets can be configured in CMS as featured modules and they display on the Homepage as per the design
    PRECONDITIONS: * The app is installed and launched
    PRECONDITIONS: * Outrights markets are created in CMS as featured modules
    """
    keep_browser_open = True

    def test_001__open_homepage_verify_the_appearance_of_outrights_markets_on_homepage(self):
        """
        DESCRIPTION: * Open Homepage
        DESCRIPTION: * Verify the appearance of Outrights markets on Homepage
        EXPECTED: * Outrights markets are displayed on Homepage as per the design below:
        EXPECTED: ![](index.php?/attachments/get/47393)
        EXPECTED: ![](index.php?/attachments/get/47394)
        """
        pass
