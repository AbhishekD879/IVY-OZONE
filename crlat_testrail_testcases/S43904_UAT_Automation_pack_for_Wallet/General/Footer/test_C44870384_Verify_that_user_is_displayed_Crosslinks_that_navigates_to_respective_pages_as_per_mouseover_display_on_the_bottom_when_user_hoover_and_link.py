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
class Test_C44870384_Verify_that_user_is_displayed_Crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_link_opens_another_window__Be_Gamble_Aware__https_wwwbegambleawareorg__GamStop_https_wwwgamstop(Common):
    """
    TR_ID: C44870384
    NAME: "Verify that user is displayed  Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover) and link opens another window - Be Gamble Aware:   https://www.begambleaware.org/ - GamStop: https://www.gamstop.
    DESCRIPTION: This TC is verify navigation from Footer to respective links available.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Application is opened and scroll to the bottom on the Homepage
        """
        pass

    def test_002_verify_that_user_is_displayed_crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_link_opens_another_window__when_the_fun_stops_be_gamble_aware__httpswwwbegambleawareorg__gambling_commission_________________httpwwwgamblingcommissiongovukhomeaspx__gamstop_httpswwwgamstopcouk(self):
        """
        DESCRIPTION: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover) and link opens another window
        DESCRIPTION: - When the fun stops (Be Gamble Aware)  (https://www.begambleaware.org/)
        DESCRIPTION: - Gambling Commission:                 http://www.gamblingcommission.gov.uk/home.aspx
        DESCRIPTION: - Gamstop: https://www.gamstop.co.uk/
        EXPECTED: When clicked on user is able to navigate to following links.
        EXPECTED: - When the fun stops (Be Gamble Aware)  (https://www.begambleaware.org/)
        EXPECTED: - Gambling Commission:                 http://www.gamblingcommission.gov.uk/home.aspx
        EXPECTED: - Gamstop:  https://www.gamstop.co.uk/
        """
        pass
