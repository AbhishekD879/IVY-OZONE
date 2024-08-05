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
class Test_C59499261_Verify_that_New_Tag_is_not_displayed_within_Build_Your_Bet_page(Common):
    """
    TR_ID: C59499261
    NAME: Verify that New Tag is not displayed within Build Your Bet page
    DESCRIPTION: Test case verify if "New" tag isn't displayed on Event Details Page with BYB.
    PRECONDITIONS: User is logged into Oxygen application.
    PRECONDITIONS: At least one event with BYB exist in application.
    """
    keep_browser_open = True

    def test_001_open_event_details_page_with_byb(self):
        """
        DESCRIPTION: Open event details page with BYB.
        EXPECTED: Event details page with selections is present.
        """
        pass

    def test_002_verify_if_new_tag_isnt_displayed_next_to_the_button_bet_filter(self):
        """
        DESCRIPTION: Verify if "New" tag isn't displayed next to the button "Bet filter".
        EXPECTED: Tag "New" isn't displayed next to the button "Bet filter".
        """
        pass
