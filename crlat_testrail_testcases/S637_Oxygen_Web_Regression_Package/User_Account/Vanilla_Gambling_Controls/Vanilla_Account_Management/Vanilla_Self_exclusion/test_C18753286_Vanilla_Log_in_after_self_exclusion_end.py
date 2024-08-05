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
class Test_C18753286_Vanilla_Log_in_after_self_exclusion_end(Common):
    """
    TR_ID: C18753286
    NAME: [Vanilla] Log in after self-exclusion end
    DESCRIPTION: This one would be hard to test - still waiting for access to the page where we can revert the self-exclusion - Will update in the future.
    PRECONDITIONS: 
    """
    keep_browser_open = True
