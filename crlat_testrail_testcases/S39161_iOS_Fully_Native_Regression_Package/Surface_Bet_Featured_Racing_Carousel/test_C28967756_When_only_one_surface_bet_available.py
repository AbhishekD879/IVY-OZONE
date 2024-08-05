import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C28967756_When_only_one_surface_bet_available(Common):
    """
    TR_ID: C28967756
    NAME: When only one surface bet available
    DESCRIPTION: This test case verifies that 1 surface bet is displayed as per the design WHEN there is only one surface bet available to be displayed
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is navigated to home page on featured tab
    PRECONDITIONS: 3. the surface bet  is available (bet has been configured in CMS for this page)
    PRECONDITIONS: 4. there are more than 1 surface bet to be displayed
    """
    keep_browser_open = True

    def test_001_emulate_1_surface_bet_displaying(self):
        """
        DESCRIPTION: emulate 1 surface bet displaying
        EXPECTED: one surface bet is displayed as per the design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3077392)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/3077393)
        """
        pass
