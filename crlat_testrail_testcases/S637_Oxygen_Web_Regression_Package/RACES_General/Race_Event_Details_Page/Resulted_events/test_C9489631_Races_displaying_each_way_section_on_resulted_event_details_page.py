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
class Test_C9489631_Races_displaying_each_way_section_on_resulted_event_details_page(Common):
    """
    TR_ID: C9489631
    NAME: <Races>: displaying each-way section on resulted event details page
    DESCRIPTION: This test case verifies displaying of each-way section on result page
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 resulted <Race> events:
    PRECONDITIONS: 1) With enabled "Each-way" on market level
    PRECONDITIONS: 2) With disabled "Each-way" on market level
    PRECONDITIONS: - You should be on <Race> result details page with enabled "Each-way"
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_each_way_section_displaying(self):
        """
        DESCRIPTION: Verify Each-way section displaying
        EXPECTED: Horse Races and Greyhounds:
        EXPECTED: - Each-way section with odds and places is displayed (e.g. Each Way 1/5 Places 1-2-3)
        EXPECTED: - Promo icons, cash out icon are displayed within Each-way section (if applicable) and right aligned
        """
        pass

    def test_002_go_to_race_event_with_disabled_each_way_section(self):
        """
        DESCRIPTION: Go to <Race> event with disabled Each-way section
        EXPECTED: Horse Races and Greyhounds:
        EXPECTED: Each-way section is not displayed
        """
        pass
