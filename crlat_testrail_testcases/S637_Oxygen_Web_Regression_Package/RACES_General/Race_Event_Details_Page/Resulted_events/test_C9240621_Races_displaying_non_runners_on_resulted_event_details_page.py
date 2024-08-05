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
class Test_C9240621_Races_displaying_non_runners_on_resulted_event_details_page(Common):
    """
    TR_ID: C9240621
    NAME: <Races>: displaying non runners on resulted event details page
    DESCRIPTION: This test case verifies displaying of non runners
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 3 resulted <Race> events:
    PRECONDITIONS: 1) With non runners without information received about trainers, jokeys etc. (non runners have 'N/R' in title, e.g. |18:30 Steepledowns N/R|)
    PRECONDITIONS: 2) With non runners with information received about trainers, jokeys etc.
    PRECONDITIONS: 3) Without non runners
    PRECONDITIONS: - You should be on a <Race> details page with non runners without information received about trainers, jokeys etc.
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_non_runners_displaying(self):
        """
        DESCRIPTION: Verify non runners displaying
        EXPECTED: "NON RUNNERS" section is displayed
        EXPECTED: UI elements"
        EXPECTED: For Horse Races:
        EXPECTED: - Section name is 'NON RUNNERS'
        EXPECTED: - All silks of non runners are grey and left aligned (if applicable)
        EXPECTED: - Runner number and name is displayed next to the silk (e.g. "3 - Sharkaholic")
        EXPECTED: - Ladbrokes only: Trainer and Jokey are displayed under the runner number and name (e.g. "T: W Buick / J: C Appleby)
        EXPECTED: - 'V' icons under ODDS column are displayed next to the each non runner
        EXPECTED: - Section name, runner number and name, T: and J: abbreviations are displayed in bold
        EXPECTED: For Greyhounds:
        EXPECTED: - Section name is 'NON RUNNERS'
        EXPECTED: - Traps silks are left aligned
        EXPECTED: - Greyhounds names are displayed next to the silk (e.g. "Sharkaholic")
        EXPECTED: - Ladbrokes only: Trainer is displayed under the runner name (e.g. "T: W Buick")
        EXPECTED: - 'V' icons under ODDS column are displayed next to the each non runner
        EXPECTED: - Section name, greyhound name and T: abbreviation are displayed in bold
        """
        pass

    def test_002_go_to_race_event_without_information_received_about_trainers_jokeys_etc(self):
        """
        DESCRIPTION: Go to <Race> event without information received about trainers, jokeys etc.
        EXPECTED: "NON RUNNERS" section is displayed
        EXPECTED: UI elements:
        EXPECTED: For Horse Races:
        EXPECTED: - Section name is 'NON RUNNERS'
        EXPECTED: - All silks of non runners are grey and left aligned (if applicable)
        EXPECTED: - Runner number and name is displayed next to the silk (e.g. "3 - Sharkaholic")
        EXPECTED: - 'V' icons under ODDS column are displayed next to the each non runner
        EXPECTED: - Section name, runner number and name, T: and J: abbreviations are displayed in bold
        EXPECTED: For Greyhounds:
        EXPECTED: - Section name is 'NON RUNNERS'
        EXPECTED: - Traps silks are left aligned
        EXPECTED: - Greyhounds names are displayed next to the silk (e.g. "Sharkaholic")
        EXPECTED: - 'V' icons under ODDS column are displayed next to the each non runner
        EXPECTED: - Section name, greyhound name and T: abbreviation are displayed in bold
        """
        pass

    def test_003_go_to_race_details_page_without_non_runners(self):
        """
        DESCRIPTION: Go to <Race> details page without non runners
        EXPECTED: For Horse Races and Greyhounds:
        EXPECTED: "NON RUNNERS" section and non runners respectively are not displayed
        """
        pass
