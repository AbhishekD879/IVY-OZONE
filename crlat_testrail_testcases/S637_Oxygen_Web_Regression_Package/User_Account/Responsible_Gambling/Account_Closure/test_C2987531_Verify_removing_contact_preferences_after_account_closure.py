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
class Test_C2987531_Verify_removing_contact_preferences_after_account_closure(Common):
    """
    TR_ID: C2987531
    NAME: Verify removing contact preferences after account closure
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
