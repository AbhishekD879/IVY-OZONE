import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2912226_Trifecta_Pool_current_pool_value(Common):
    """
    TR_ID: C2912226
    NAME: Trifecta Pool current pool value
    DESCRIPTION: Test case verifies Current Pool value for Trifecta pool
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: Request to retrieve current pool value
    PRECONDITIONS: /PoolForEvent/{tote_event_id}?&translationLang=en,
    PRECONDITIONS: where exacta pool has type parameter "UTRI"
    PRECONDITIONS: **International Tote Event Race card is opened and Trifecta pool is selected**
    """
    keep_browser_open = True

    def test_001_verify_currect_pool_value(self):
        """
        DESCRIPTION: Verify Currect pool value
        EXPECTED: Current pool value contains the value from "poolValue" parameter of /PoolForEvent request:
        EXPECTED: - if the value is returned from OB then then Current pool value is displayed with correct value
        """
        pass
