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
class Test_C9332775_Races_displaying_favorites_labels_on_resulted_event_details_page(Common):
    """
    TR_ID: C9332775
    NAME: <Races>: displaying favorites labels on resulted event details page
    DESCRIPTION: This test case verifies displaying of favorites labels
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have 4 resulted <Race> events:
    PRECONDITIONS: 1) With lowest SP prices within won runners
    PRECONDITIONS: 2) With lowest SP prices within lost runners (lost runners don't have place provided)
    PRECONDITIONS: 3) With 2 the same lowest SP prices within won runners
    PRECONDITIONS: 4) With 2 the same lowest SP prices within won and lost runner at the same time (e.g. runner 1 won, and runner 5 lost, but both have the same SP price)
    PRECONDITIONS: - You should be on a <Race> details page with lowest SP prices within won runners
    PRECONDITIONS: F/2F (Favorite / Second Favorite) are identified by the lowest SP prices
    PRECONDITIONS: JF/2JF (Join Favorite / Second Joint Favorite) are identified by the lowest SP prices in 2 runners
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_favorites_labels_displaying(self):
        """
        DESCRIPTION: Verify favorites labels displaying
        EXPECTED: For Horse Races and Greyhounds:
        EXPECTED: Ladbrokes:
        EXPECTED: - f label is displayed next to the prise against the runner with the lowest price
        EXPECTED: - 2f label is displayed next to the prise against the runner with the second lowest price
        EXPECTED: Coral:
        EXPECTED: - F label is displayed next to the runner name against the runner with the lowest price
        EXPECTED: - 2F label is displayed next to the runner name against the runner with the second lowest price
        """
        pass

    def test_002_go_to_the_race_event_with_lowest_sp_prices_within_lost_runners(self):
        """
        DESCRIPTION: Go to the <Race> event with lowest SP prices within lost runners
        EXPECTED: For Horse Races and Greyhounds:
        EXPECTED: - F/2F labels are nod displayed as runners with lowest PS prices are not displayed
        """
        pass

    def test_003_go_to_the_race_event_with_the_same_lowest_sp_prices_within_2_won_runners(self):
        """
        DESCRIPTION: Go to the <Race> event with the same lowest SP prices within 2 won runners
        EXPECTED: For Horse Races and Greyhounds:
        EXPECTED: Ladbrokes:
        EXPECTED: - jf label is displayed next to the prise against the runners with the same lowest prices
        EXPECTED: - 2jf label is displayed next to the prise against the runners with the second the same lowest price
        EXPECTED: Coral:
        EXPECTED: - JF label is displayed next to the prise against the runners with the same lowest prices
        EXPECTED: - 2JF label is displayed next to the prise against the runners with the second the same lowest price
        """
        pass

    def test_004_go_to_the_race_event_with_the_same_lowest_sp_prices_within_won_and_lost_runners(self):
        """
        DESCRIPTION: Go to the <Race> event with the same lowest SP prices within won and lost runners
        EXPECTED: For Horse Races and Greyhounds:
        EXPECTED: Ladbrokes:
        EXPECTED: - jf label is displayed next to the prise against the won runner with the same lowest prices
        EXPECTED: - 2jf label is displayed next to the prise against the won runner with the second the same lowest price
        EXPECTED: Coral:
        EXPECTED: - JF label is displayed next to the prise against the won runners with the same lowest prices
        EXPECTED: - 2JF label is displayed next to the prise against the won runners with the second the same lowest price
        """
        pass
