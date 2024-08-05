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
class Test_C44870428_iOS_Verify_login_flows_via_Face_ID(Common):
    """
    TR_ID: C44870428
    NAME: [iOS] Verify login flows via Face ID
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
