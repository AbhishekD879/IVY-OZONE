import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9618065_Races_displaying_switchers_for_future_races_on_landing_page(Common):
    """
    TR_ID: C9618065
    NAME: <Races>: displaying switchers for future races on landing page
    DESCRIPTION: This test case verifies displaying of switchers for future races on <Race> landing page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have at least 7 <Race> events within one sub region configured on different dates starting from yestarday and each next +1 day (e.g. today is Monday then you should have 6 races configured on Sun, Mon, Tue, Wed, Thu, Fri, Sat)
    PRECONDITIONS: - You should have <Race> events within another sub region configured on past and today's dates
    PRECONDITIONS: - You should be on <Race> landing page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_switchers_for_future_races(self):
        """
        DESCRIPTION: Verify displaying of switchers for future races
        EXPECTED: - Days switchers are displayed below the sub region section
        EXPECTED: 1) Sub region with events configured on different dates:
        EXPECTED: - Has 6 day switchers starting from today (e.g. Monday, Tuesday etc.)
        EXPECTED: - Doesn't have switchers on past days
        EXPECTED: 2) Sub region with different amount of switchers (one or more):
        EXPECTED: - Switchers are extended to be displayed on a full screen
        """
        pass
