import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2604538_Each_Way_option_for_Outrights_Multiples(Common):
    """
    TR_ID: C2604538
    NAME: Each Way option for Outrights Multiples
    DESCRIPTION: This test case verifies Each Way option for Multiples created from Outrights
    PRECONDITIONS: 1.  Make sure you have the following selections available:
    PRECONDITIONS: - <Sport> selections from markets with Each Way option available from different Outright events
    PRECONDITIONS: 2.  To get information about selected event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: USE *'isEachWayAvailable'* on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True

    def test_001_add_two_or_more_sport_selections_from_markets_with_each_way_option_available_from_different_outright_events(self):
        """
        DESCRIPTION: Add two or more <Sport> selections from markets with Each Way option available from different Outright events
        EXPECTED: Selections are added to the betslip
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 
        """
        pass

    def test_003_verify_multiples_section(self):
        """
        DESCRIPTION: Verify Multiples section
        EXPECTED: - Multiple in 'Place your ACCA' section' (if available) contain 'Each Way' check box if all added selections have 'Each Way' option available ( **From OX99** Place your ACCA' section' was removed. ACCA bet is the first under the 'Multiples' section)
        EXPECTED: - Each Multiple within 'Multiples' section contain 'Each Way' check box if all added selections have 'Each Way' option available
        EXPECTED: - Each Way check box is NOT selected by default for Multiples
        """
        pass

    def test_004_place_a_bet_on_multiple_with_valid_stake_and_each_way_checkbox_selected(self):
        """
        DESCRIPTION: Place a bet on Multiple with valid stake and 'Each Way' checkbox selected
        EXPECTED: - 'Stake' value corresponds to the entered stake
        EXPECTED: - Total Stake for selected Multiple is doubled
        EXPECTED: - Bet is placed successfully
        """
        pass
