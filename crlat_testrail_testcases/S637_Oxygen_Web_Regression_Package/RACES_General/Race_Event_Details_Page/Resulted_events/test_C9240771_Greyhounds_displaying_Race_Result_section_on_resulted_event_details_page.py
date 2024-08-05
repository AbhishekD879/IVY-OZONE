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
class Test_C9240771_Greyhounds_displaying_Race_Result_section_on_resulted_event_details_page(Common):
    """
    TR_ID: C9240771
    NAME: Greyhounds: displaying Race Result section on resulted event details page
    DESCRIPTION: This test case verifies displaying Rase Result section
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 2 resulted Greyhounds events:
    PRECONDITIONS: 1) With information received about trainers etc.
    PRECONDITIONS: 2) Without information received about trainers etc.
    PRECONDITIONS: - You should be on a Greyhounds details page with information received about trainer, jokey
    """
    keep_browser_open = True

    def test_001_verify_race_result_section(self):
        """
        DESCRIPTION: Verify Race Result section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section name is "Race result" displayed in bold and left aligned, and "ODDS" column is right aligned
        EXPECTED: - List of greyhounds in DESC order by Place
        EXPECTED: - Each greyhound card contains next elements:
        EXPECTED: 1) Place in bold and left aligned (e.g. 1st, 2nd etc.)
        EXPECTED: 2) Greyhounds trap (if applicable)
        EXPECTED: 3) Greyhound name in bold
        EXPECTED: 4) Trainer with T: abbreviation in bold (e.g. "T: W Buick) and placed below the greyhound name
        EXPECTED: 5) SP price under "ODDS" column against respective greyhound
        EXPECTED: 6) F/2F/JF/2JF labels (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: - f/2f/jf/2jf labels placed next to the SP prices in lower case
        EXPECTED: Coral:
        EXPECTED: - F/2F/JF/2JF labels placed next to runner name in upper case
        """
        pass

    def test_002_go_to_greyhounds_event_details_page_without_received_information_about_trainer_etc_and_verify_race_result_section(self):
        """
        DESCRIPTION: Go to Greyhounds event details page without received information about trainer etc. and verify Race Result section
        EXPECTED: Coral and Ladbrokes:
        EXPECTED: - Section name is "Race result" displayed in bold and left aligned, and "ODDS" column is right aligned
        EXPECTED: - List of greyhounds in DESC order by Place
        EXPECTED: - Each greyhound card contains next elements:
        EXPECTED: 1) Place in bold and left aligned (e.g. 1st, 2nd etc.)
        EXPECTED: 2) Greyhounds trap
        EXPECTED: 3) Greyhound name is displayed in bold and centered
        EXPECTED: 4) SP price under "ODDS" column against respective greyhound
        EXPECTED: 5) F/2F/JF/2JF labels (if applicable)
        EXPECTED: Ladbrokes:
        EXPECTED: - f/2f/jf/2jf labels placed next to the SP prices in lower case
        EXPECTED: Coral:
        EXPECTED: - F/2F/JF/2JF labels placed next to runner name in upper case
        """
        pass
