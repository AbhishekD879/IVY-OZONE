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
class Test_C9618072_Races_displaying_cash_out_icon_on_landing_page(Common):
    """
    TR_ID: C9618072
    NAME: <Races>: displaying 'cash out' icon on landing page
    DESCRIPTION: This test case verifies that 'cash out' icons are not displayed on <Race> landing page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have <Race> events with cash out enabled on event and primary market levels
    PRECONDITIONS: - You should be on <Race> landing page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_cash_out_icon(self):
        """
        DESCRIPTION: Verify displaying of 'cash out' icon
        EXPECTED: Cash out icon is not displayed on landing page
        """
        pass
