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
class Test_C44870426_Verify_TouchId__FP_login(Common):
    """
    TR_ID: C44870426
    NAME: Verify TouchId / FP login
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
