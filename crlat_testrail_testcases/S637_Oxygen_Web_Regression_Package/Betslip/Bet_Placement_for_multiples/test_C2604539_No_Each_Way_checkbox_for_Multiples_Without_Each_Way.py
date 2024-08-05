import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2604539_No_Each_Way_checkbox_for_Multiples_Without_Each_Way(Common):
    """
    TR_ID: C2604539
    NAME: No Each Way checkbox for Multiples Without Each Way
    DESCRIPTION: This test case verifies Each Way option for Multiples
    PRECONDITIONS: 1.  Make sure you have the following selections available:
    PRECONDITIONS: - <Race> selections from markets with Each Way option available from different events
    PRECONDITIONS: - <Sport> selections from markets with Each Way option available from different Outright events
    PRECONDITIONS: 2.  To get information about selected event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: USE *'isEachWayAvailable'* on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True

    def test_001_add_two_or_more_race_and_sport_selections_from_markets_with_each_way_option_available_from_different_events_and_at_least_one_selection_from_any_market_without_each_way_option_available(self):
        """
        DESCRIPTION: Add two or more <Race> and <Sport> selections from markets with Each Way option available from different events and at least ONE selection from any market WITHOUT Each Way option available
        EXPECTED: Selections are added to the betslip
        """
        pass

    def test_002_open_betslip___check_multiple_selections_build_based_on_added_selections(self):
        """
        DESCRIPTION: Open betslip -> Check Multiple selections build based on added selections
        EXPECTED: Each Way check box is NOT available for Multiples if at least one added selection is from market WITHOUT Each Way option available
        """
        pass
