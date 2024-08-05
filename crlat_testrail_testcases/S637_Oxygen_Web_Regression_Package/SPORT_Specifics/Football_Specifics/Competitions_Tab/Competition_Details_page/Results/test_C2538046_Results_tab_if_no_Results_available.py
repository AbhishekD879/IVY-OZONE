import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C2538046_Results_tab_if_no_Results_available(Common):
    """
    TR_ID: C2538046
    NAME: Results tab if no Results available
    DESCRIPTION: This test case verifies 'Results' tab displayed on Football competition details page depends on results availability
    PRECONDITIONS: Competitions tab on Football is opened
    """
    keep_browser_open = True

    def test_001_verifyresults_pagewidget_if_there_is_no_result_available_for_particular_competition(self):
        """
        DESCRIPTION: Verify 'Results' page/widget if there is no result available for particular Competition
        EXPECTED: * 'Results' tab is NOT present if results are not available
        EXPECTED: * 'Results' widget is NOT present on Desktop
        """
        pass
