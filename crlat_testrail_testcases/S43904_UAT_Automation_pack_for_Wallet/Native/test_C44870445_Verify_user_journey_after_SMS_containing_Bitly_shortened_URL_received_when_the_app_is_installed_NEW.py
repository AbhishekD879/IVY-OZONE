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
class Test_C44870445_Verify_user_journey_after_SMS_containing_Bitly_shortened_URL_received_when_the_app_is_installed_NEW(Common):
    """
    TR_ID: C44870445
    NAME: Verify user journey after SMS containing Bitly shortened URL received when the app is installed (NEW)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
