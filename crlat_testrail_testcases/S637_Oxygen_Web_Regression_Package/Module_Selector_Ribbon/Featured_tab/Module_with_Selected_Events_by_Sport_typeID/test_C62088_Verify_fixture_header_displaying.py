import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62088_Verify_fixture_header_displaying(Common):
    """
    TR_ID: C62088
    NAME: Verify fixture header displaying
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
