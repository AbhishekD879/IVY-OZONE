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
class Test_C44870446_Verify_the_app_behavior_depending_on_country_list_in_CMS_NEW(Common):
    """
    TR_ID: C44870446
    NAME: Verify the app behavior depending on country list in CMS (NEW)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
