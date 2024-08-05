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
class Test_C44870429_Verify_Auto_Login(Common):
    """
    TR_ID: C44870429
    NAME: Verify Auto Login
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
