import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C2747978_Verify_navigation_to_Responsible_Gambling_page_via_direct_link_for_the_logged_out_user(Common):
    """
    TR_ID: C2747978
    NAME: Verify navigation to 'Responsible Gambling' page via direct link for the logged out user
    DESCRIPTION: This test case verifies navigation to 'Responsible Gambling' page via direct link for the logged out user
    PRECONDITIONS: User is logged out
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 'Responsible Gambling EN' static block should be configured in CMS and set to active (CMS_ENDPOINT/static-blocks/, where CMS_ENDPOINT can be found using devlog)
    """
    keep_browser_open = True

    def test_001_go_to_the_responsible_gambling_page_via_direct_linkhttpsenvironmentresponsible_gambling(self):
        """
        DESCRIPTION: Go to the 'Responsible Gambling' page via direct link:
        DESCRIPTION: https://{environment}/responsible-gambling
        EXPECTED: * 'Responsible Gambling' page is NOT loaded
        EXPECTED: * Homepage is opened instead
        """
        pass
