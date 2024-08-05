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
class Test_C44870448_Verify_auto_retry_of_connection_NEW(Common):
    """
    TR_ID: C44870448
    NAME: Verify auto retry of connection (NEW)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
