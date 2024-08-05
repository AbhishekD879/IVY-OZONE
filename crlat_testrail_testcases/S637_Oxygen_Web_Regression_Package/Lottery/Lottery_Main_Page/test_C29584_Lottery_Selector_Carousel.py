import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.lotto
@vtest
class Test_C29584_Lottery_Selector_Carousel(Common):
    """
    TR_ID: C29584
    NAME: Lottery Selector Carousel
    DESCRIPTION: This Test Case verifies Lottery Selector Carousel.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA - 2308 (Lottery - Select a lottery)
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    """
    keep_browser_open = True

    def test_001_tap_lotto_icon_from_sportsmenu_ribbonor_a_z_page(self):
        """
        DESCRIPTION: Tap 'Lotto' icon (from Sports Menu Ribbon or A-Z page)
        EXPECTED: 'Lotto' page is opened
        """
        pass

    def test_002_launch_url_from_preconditions_to_verify_lotteries_presence_in_carousel_basing_on_siteserve_response(self):
        """
        DESCRIPTION: Launch URL from Preconditions to verify Lotteries presence in Carousel basing on SiteServe response
        EXPECTED: All lotteries from SiteServe response are available within Lottery Selector Carousel
        """
        pass

    def test_003_verify_lottery_selector_carousel(self):
        """
        DESCRIPTION: Verify Lottery Selector Carousel
        EXPECTED: *   Each Lottery in the Carousel has it's own icon and title
        EXPECTED: *   Lottery with the upcoming Draw should be selected and highlighted by default
        """
        pass

    def test_004_verify_lotteries_order(self):
        """
        DESCRIPTION: Verify Lotteries order
        EXPECTED: Lotteries order should be based on the Draw time (shutAtTime attribute) in ascending order, displaying horizontaly from left to right
        """
        pass

    def test_005_swipe_lottery_selector_carousel(self):
        """
        DESCRIPTION: Swipe Lottery Selector Carousel
        EXPECTED: *   Swipe is supported within the Carousel to browse the available Lotteries
        EXPECTED: *   It is possible to swipe both ways
        """
        pass

    def test_006_verify_lottery_icons(self):
        """
        DESCRIPTION: Verify Lottery icons
        EXPECTED: Lottery icons correspond to "**description**" attribute on the lottery level
        """
        pass

    def test_007_tap_on_any_lotto_icon(self):
        """
        DESCRIPTION: Tap on any 'Lotto' icon
        EXPECTED: Related information to the selected Lottery is loaded below the Carousel
        """
        pass

    def test_008_verify_lottery_name(self):
        """
        DESCRIPTION: Verify Lottery name
        EXPECTED: Lottery name corresponds to "**description**" attribute on the lottery level
        """
        pass
