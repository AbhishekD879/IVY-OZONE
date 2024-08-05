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
class Test_C60018008_Verify_Freebets_receiving_according_channel_setting(Common):
    """
    TR_ID: C60018008
    NAME: Verify Freebets receiving according channel setting
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
