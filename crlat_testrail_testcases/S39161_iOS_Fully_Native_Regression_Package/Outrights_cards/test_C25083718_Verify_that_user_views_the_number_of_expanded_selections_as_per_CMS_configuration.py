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
class Test_C25083718_Verify_that_user_views_the_number_of_expanded_selections_as_per_CMS_configuration(Common):
    """
    TR_ID: C25083718
    NAME: Verify that user views the number of expanded selections as per CMS configuration
    DESCRIPTION: This test case verifies that the number of expanded Outrights market selections can be configured and changed in CMS
    PRECONDITIONS: * The app is installed and launched
    PRECONDITIONS: * Outrights market is created in CMS as featured module
    PRECONDITIONS: * The number of selections to be expanded is specified in CMS
    PRECONDITIONS: * Outright market has more selections configured than the number of selections specified in CMS
    """
    keep_browser_open = True

    def test_001__open_homepage_verify_the_count_of_selections_which_are_expanded_within_the_outrights_module(self):
        """
        DESCRIPTION: * Open Homepage
        DESCRIPTION: * Verify the count of selections which are expanded within the Outrights module
        EXPECTED: The count of selections expanded within the Outrights module is equal to the number of selections specified in CMS
        """
        pass

    def test_002_swipe_down_the_outrights_module(self):
        """
        DESCRIPTION: Swipe down the Outrights module
        EXPECTED: 'Show More' CTA is shown at the bottom of the module
        EXPECTED: ![](index.php?/attachments/get/57366)
        """
        pass

    def test_003_tap_on_show_more_cta(self):
        """
        DESCRIPTION: Tap on 'Show More' CTA
        EXPECTED: * The module expands and the rest of selections is displayed
        EXPECTED: * The count of selections should be equal to the count of selections configured for Outrights market
        """
        pass
