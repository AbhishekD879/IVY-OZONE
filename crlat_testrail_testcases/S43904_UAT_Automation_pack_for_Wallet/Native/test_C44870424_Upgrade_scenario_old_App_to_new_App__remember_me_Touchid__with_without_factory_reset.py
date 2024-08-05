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
class Test_C44870424_Upgrade_scenario_old_App_to_new_App__remember_me_Touchid__with_without_factory_reset(Common):
    """
    TR_ID: C44870424
    NAME: Upgrade scenario old App to new App - remember me/Touchid - with/without factory reset
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
