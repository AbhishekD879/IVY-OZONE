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
class Test_C28855_Verify_Price_Odds_Buttons_for_Race_with_SP_price_type(Common):
    """
    TR_ID: C28855
    NAME: Verify Price/Odds Buttons for <Race> with SP price type
    DESCRIPTION: Verify Price/Odds Buttons for <Race> with SP price type
    DESCRIPTION: AUTOTEST C2690230
    PRECONDITIONS: There is <Race> events with SP prices available, no LP prices:
    PRECONDITIONS: (1) event with 'runnerNumber' attribute
    PRECONDITIONS: (2) event without 'runnerNumber' attribute
    """
    keep_browser_open = True

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_open_event_1_from_preconditions(self):
        """
        DESCRIPTION: Open event (1) from preconditions
        EXPECTED: All selections display SP
        """
        pass

    def test_003_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered by '**runnerNumber'** attribute in ascending order
        """
        pass

    def test_004_open_event_2_from_preconditions(self):
        """
        DESCRIPTION: Open event (2) from preconditions
        EXPECTED: All selections display SP
        """
        pass

    def test_005_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED: Selections are ordered alphabetically
        EXPECTED: *   Alphabetically by first letter of Horse name
        EXPECTED: *   If first letter of Outcome name is the same then sort by second letter
        """
        pass
