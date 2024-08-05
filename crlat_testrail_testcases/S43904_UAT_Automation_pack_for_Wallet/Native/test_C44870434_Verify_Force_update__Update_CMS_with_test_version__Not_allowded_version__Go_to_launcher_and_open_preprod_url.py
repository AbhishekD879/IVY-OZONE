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
class Test_C44870434_Verify_Force_update__Update_CMS_with_test_version__Not_allowded_version__Go_to_launcher_and_open_preprod_url(Common):
    """
    TR_ID: C44870434
    NAME: "Verify Force update - Update CMS with test version -> Not allowded version - Go to launcher and open preprod url"
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
