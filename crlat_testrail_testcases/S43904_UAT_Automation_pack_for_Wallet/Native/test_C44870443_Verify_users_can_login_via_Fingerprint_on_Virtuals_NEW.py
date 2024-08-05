import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C44870443_Verify_users_can_login_via_Fingerprint_on_Virtuals_NEW(Common):
    """
    TR_ID: C44870443
    NAME: Verify users can login via Fingerprint on Virtuals (NEW)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
