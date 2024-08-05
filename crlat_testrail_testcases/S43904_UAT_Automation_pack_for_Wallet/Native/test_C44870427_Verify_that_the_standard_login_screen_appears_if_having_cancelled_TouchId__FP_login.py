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
class Test_C44870427_Verify_that_the_standard_login_screen_appears_if_having_cancelled_TouchId__FP_login(Common):
    """
    TR_ID: C44870427
    NAME: Verify that the standard login screen appears if having cancelled TouchId / FP login
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
