import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870407_Verify_header_menu_navigation(Common):
    """
    TR_ID: C44870407
    NAME: Verify header menu navigation
    DESCRIPTION: Verify that the following links are displayed as per GDs and navigates user to respective URLs.
    DESCRIPTION: URLs:
    DESCRIPTION: SPORTS            https://sports.coral.co.uk/
    DESCRIPTION: GAMING            https://www.coral.co.uk/en/games
    DESCRIPTION: CASINO            https://www.coral.co.uk/en/coralcasino
    DESCRIPTION: LIVE CASINO       https://www.coral.co.uk/en/livecasino
    DESCRIPTION: SLOTS             https://www.coral.co.uk/en/games/c/slots
    DESCRIPTION: BINGO             https://bingo.coral.co.uk/en/bingo
    DESCRIPTION: POKER             https://poker.coral.co.uk/en/poker
    DESCRIPTION: OFFERS            https://promo.coral.co.uk/en/promo/offers
    DESCRIPTION: CONNECT           https://sports.coral.co.uk/retail
    PRECONDITIONS: User can view the header menu links in logged in or logged out status.
    """
    keep_browser_open = True

    def test_001_verify_the_all_header_menu_links_functionality_changes_on_hovering_mouse_over_text_on_bottom_navigation___page_opens_in_the_same_window_user_remains_logged_in_and_is_able_to_navigate_back(self):
        """
        DESCRIPTION: Verify the all Header menu links functionality (changes on hovering, mouse over text on bottom, navigation - page opens in the same window, user remains logged in, and is able to navigate back).
        EXPECTED: Respective header menu link displays url at bottom of Chrome when hovered over it. When clicking on link user navigated to respective page in the same window and remains logged in.
        """
        pass
