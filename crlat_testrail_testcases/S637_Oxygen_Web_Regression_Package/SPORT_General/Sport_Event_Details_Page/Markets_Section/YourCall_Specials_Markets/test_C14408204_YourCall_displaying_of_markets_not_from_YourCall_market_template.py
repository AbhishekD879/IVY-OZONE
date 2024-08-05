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
class Test_C14408204_YourCall_displaying_of_markets_not_from_YourCall_market_template(Common):
    """
    TR_ID: C14408204
    NAME: #YourCall: displaying of markets not from 'YourCall' market template
    DESCRIPTION: This test case verifies that markets with 'YourCall' word in market name but created not from 'YourCall' market template are not grouped with YourCall markets
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a Football event with couple markets added from market templates with "YourCall" word within the name and without it
    PRECONDITIONS: - One of the markets not from 'YourCall' market template should have 'YourCall' word in market name
    PRECONDITIONS: - You should be on the event details page
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_with_yourcall_word_in_name_but_not_from_yourcall_market_template(self):
        """
        DESCRIPTION: Verify displaying of the market with 'YourCall' word in name, but not from 'YourCall' market template
        EXPECTED: Market is displayed under the separate accordion and is NOT a 'YourCall' market
        """
        pass
