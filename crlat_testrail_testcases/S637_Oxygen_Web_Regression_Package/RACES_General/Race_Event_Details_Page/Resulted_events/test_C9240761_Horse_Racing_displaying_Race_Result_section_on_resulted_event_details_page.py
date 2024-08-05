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
class Test_C9240761_Horse_Racing_displaying_Race_Result_section_on_resulted_event_details_page(Common):
    """
    TR_ID: C9240761
    NAME: Horse Racing: displaying Race Result section on resulted event details page
    DESCRIPTION: This test case verifies displaying Rase Result section
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 resulted Horse Race events:
    PRECONDITIONS: 1) With information received about trainers, jokeys etc.
    PRECONDITIONS: 2) Without information received about trainers, jokeys etc.
    PRECONDITIONS: - You should be on a Horse Race details page with information received about trainer, jokey
    """
    keep_browser_open = True

    def test_001_verify_race_result_section(self):
        """
        DESCRIPTION: Verify Race Result section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section name is "Race Result" displayed in bold and left aligned, and "ODDS" column is right aligned
        EXPECTED: - List of runners in DESC order by Place is displayed (only runners with provided place in TI are shown)
        EXPECTED: - Each runner card contains next elements:
        EXPECTED: 1) Place in bold and left aligned (e.g. 1st, 2nd etc.)
        EXPECTED: 2) Runner silk
        EXPECTED: 3) Runner number and name in bold
        EXPECTED: 4) Trainer and Jokey with T: and J: abbreviations in bold (e.g. "T: W Buick / J: C Appleby) and placed below the runner number and name
        EXPECTED: 5) SP price under "ODDS" column against respective runner
        EXPECTED: 6) F/2F/JF/2JF labels (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: - f/2f/jf/2jf labels placed next to the SP prices in lower case
        EXPECTED: Coral:
        EXPECTED: - F/2F/JF/2JF labels placed next to runner name in upper case
        """
        pass

    def test_002_go_to_horse_race_event_details_page_without_received_information_about_trainer_jokey_etc_and_verify_race_result_section(self):
        """
        DESCRIPTION: Go to Horse Race event details page without received information about trainer, jokey etc. and verify Race Result section
        EXPECTED: Ladbrokes:
        EXPECTED: - Section name is "Race Result" displayed in bold and left aligned, and "ODDS" column is right aligned
        EXPECTED: - List of runners in DESC order by Place is displayed (only runners with provided place in TI are shown)
        EXPECTED: - Each runner card contains next elements:
        EXPECTED: 1) Places in bold and left aligned (e.g. 1st, 2nd etc.)
        EXPECTED: 2) Runners numbers and names are displayed in bold  and centered
        EXPECTED: 3) SP prices under "ODDS" column against respective runner
        EXPECTED: 4) F/2F/JF/2JF labels (if applicable) (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: - f/2f/jf/2jf labels placed next to the SP prices in lower case
        EXPECTED: Coral:
        EXPECTED: - F/2F/JF/2JF labels placed next to runner name in upper case
        """
        pass
