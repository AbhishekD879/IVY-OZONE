import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C59499229_Verify_that_New_Tag_is_not_displayed_within_Horse_Racing_Bet_Filter_page(Common):
    """
    TR_ID: C59499229
    NAME: Verify that New Tag is not displayed within Horse Racing Bet Filter page
    DESCRIPTION: Test case verify if "New" tag isn't displayed on Horse Racing Bet Filter.
    PRECONDITIONS: * User is logged into Oxygen application.
    PRECONDITIONS: **NOTE:** Will be implemented for Ladbrokes after OX 108
    """
    keep_browser_open = True

    def test_001_go_to_horse_racing_page_and_open_any_of_existing_event_details_page(self):
        """
        DESCRIPTION: Go to Horse Racing page and open any of existing event details page.
        EXPECTED: Event details page with selections is present.
        """
        pass

    def test_002_verify_if_new_tag_isnt_displayed_next_to_the_button_bet_filter(self):
        """
        DESCRIPTION: Verify if "New" tag isn't displayed next to the button "Bet filter".
        EXPECTED: Tag "New" isn't displayed next to the button "Bet filter".
        """
        pass
