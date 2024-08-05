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
class Test_C44870383_Verify_that_user_is_displayed_Crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_this_ink_opens_another_window(Common):
    """
    TR_ID: C44870383
    NAME: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover): and this ink opens another window
    DESCRIPTION: This TC is to verify all footer links are navigating accordingly.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application.
        EXPECTED: Application is opened.
        """
        pass

    def test_002_verify_that_user_is_displayed_crosslinks_that_navigates_to_respective_pages_as_per_mouseover_display_on_the_bottom_when_user_hoover_and_this_ink_opens_another_windowgam_stop___httpswwwgamstopcoukgamcare___httpswwwgamcareorgukgambling_commission___httpwwwgamblingcommissiongovukhomeaspxibas___httpswwwibas_ukcom18plus___httpswwwcoralcoukenp18plus(self):
        """
        DESCRIPTION: "Verify that user is displayed Crosslinks that navigates to respective pages (as per mouseover display on the bottom, when user hoover): and this ink opens another window
        DESCRIPTION: Gam stop - https://www.gamstop.co.uk/
        DESCRIPTION: GamCare - https://www.gamcare.org.uk/
        DESCRIPTION: Gambling Commission - http://www.gamblingcommission.gov.uk/home.aspx
        DESCRIPTION: IBAS - https://www.ibas-uk.com/
        DESCRIPTION: 18+ - https://www.coral.co.uk/en/p/18plus
        EXPECTED: When clicked on, user is navigated to appropriate links.
        EXPECTED: Gam stop - https://www.gamstop.co.uk/
        EXPECTED: GamCare - https://www.gamcare.org.uk/
        EXPECTED: Gambling Commission - http://www.gamblingcommission.gov.uk/home.aspx
        EXPECTED: IBAS - https://www.ibas-uk.com/
        EXPECTED: 18+ - https://www.coral.co.uk/en/p/18plus
        """
        pass
