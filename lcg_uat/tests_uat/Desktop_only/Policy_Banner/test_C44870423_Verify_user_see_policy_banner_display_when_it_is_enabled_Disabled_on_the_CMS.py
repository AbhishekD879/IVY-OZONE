import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870423_Verify_user_see_policy_banner_display_when_it_is_enabled_Disabled_on_the_CMS(Common):
    """
    TR_ID: C44870423
    NAME: Verify user see policy banner display when it is enabled/Disabled on the CMS
    """
    keep_browser_open = True
