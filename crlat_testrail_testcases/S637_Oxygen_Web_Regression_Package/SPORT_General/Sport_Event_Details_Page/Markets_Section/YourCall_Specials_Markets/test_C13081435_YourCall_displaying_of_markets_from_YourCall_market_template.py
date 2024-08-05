import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C13081435_YourCall_displaying_of_markets_from_YourCall_market_template(Common):
    """
    TR_ID: C13081435
    NAME: #YourCall: displaying of markets from 'YourCall' market template
    DESCRIPTION: This test case verifies that YourCall markets are grouped within #YourCall markets accordion
    DESCRIPTION: Note: #YourCall - Coral
    DESCRIPTION: #GetAPrice - Ladbrokes
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have a Football event with couple markets added from market templates with "YourCall" word within the name
    PRECONDITIONS: - You should be on the event details page
    """
    keep_browser_open = True

    def test_001_verify_yourcall_markets_presence(self):
        """
        DESCRIPTION: Verify #YourCall markets presence
        EXPECTED: #YourCall markets are displayed according to Display Order setting in TI;
        """
        pass

    def test_002_expand_yourcall_market_accordion_and_verify_displaying_of_selections(self):
        """
        DESCRIPTION: Expand #YourCall market accordion and verify displaying of selections
        EXPECTED: - All active YourCall markets added from market templates with "YourCall" word within the name are displayed with "#YourCall" prefix
        EXPECTED: - All active YourCall markets are displayed under separate accordions
        EXPECTED: - All active selections added to the markets above are displayed under respective markets
        """
        pass

    def test_003_go_to_yourcall_tab_and_verify_displaying_of_markets_and_selections(self):
        """
        DESCRIPTION: Go to YourCall tab and verify displaying of markets and selections
        EXPECTED: - All active YourCall markets added from market templates with "YourCall" word within the name are displayed with "#YourCall" prefix
        EXPECTED: - All active YourCall markets are displayed under separate accordions
        EXPECTED: - All active selections added to the markets above are displayed under respective markets
        """
        pass
