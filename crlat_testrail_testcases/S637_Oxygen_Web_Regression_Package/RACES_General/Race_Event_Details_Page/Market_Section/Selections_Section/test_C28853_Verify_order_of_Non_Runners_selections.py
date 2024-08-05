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
class Test_C28853_Verify_order_of_Non_Runners_selections(Common):
    """
    TR_ID: C28853
    NAME: Verify order of Non-Runners selections
    DESCRIPTION: This test case verifies order of Non-Runners selections.
    DESCRIPTION: AUTOTEST [C2694497]
    PRECONDITIONS: 1. Make sure you have events with Non-Runners selections:
    PRECONDITIONS: 'Non-Runners' is a selection which contains **'N/R'** text next to it's name
    PRECONDITIONS: For those selections 'outcomeStatusCode'='S' - those selections are always suspended.
    PRECONDITIONS: 2. To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: 
        """
        pass

    def test_002_verify_non_runner_selections_within_win_or_each_way_market_sorted_by_price(self):
        """
        DESCRIPTION: Verify Non-Runner selections within 'Win or Each Way' market sorted by Price
        EXPECTED: 1.  'Non-Runners' are displayed at the bottom of the outcomes list (above the 'UNNAMED FAVOURITE'/UNNAMED 2nd FAVOURITE' sections)
        EXPECTED: 2.  'Non-Runners' are ordered by Horse/Greyhound Number in ascending
        """
        pass

    def test_003_verify_non_runner_selections_within_win_or_each_way_market_sorted_by_racecard(self):
        """
        DESCRIPTION: Verify Non-Runner selections within 'Win or Each Way' market sorted by Racecard
        EXPECTED: 1. 'Non-Runners' are ordered by Horse/Greyhound Number in ascending
        """
        pass

    def test_004_verify_non_runner_selections_within_other_markets(self):
        """
        DESCRIPTION: Verify Non-Runner selections within other markets
        EXPECTED: 1.  'Non-Runners' are displayed at the bottom of the outcomes list (below the last selection with a 'Live Price')
        EXPECTED: 2.  'Non-Runners' are ordered by  Horse/Greyhound Number in ascending
        """
        pass
