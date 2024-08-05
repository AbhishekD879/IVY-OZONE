import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2601279_Verify_Correct_Score_Coupon_Details_page(Common):
    """
    TR_ID: C2601279
    NAME: Verify Correct Score Coupon Details page
    DESCRIPTION: 
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Coupon is added to Football > Coupons / ACCAS  > Some particular section.
    PRECONDITIONS: 2. Correct Score Coupon is opened
    PRECONDITIONS: Create a coupon with 'Correct Score' market template & displaySortName as COR* another coupon with any market template but displaySortName as "CS"
    """
    keep_browser_open = True

    def test_001_verify_the_cs_coupon_page_header(self):
        """
        DESCRIPTION: Verify the CS Coupon page header
        EXPECTED: Header contains:
        EXPECTED: * 'Back' button
        EXPECTED: * 'Coupons' header name
        """
        pass

    def test_002_verify_the_cs_coupon_page_sub_header(self):
        """
        DESCRIPTION: Verify the CS Coupon page sub-header
        EXPECTED: * Coupons sub-header is located below Coupons header
        EXPECTED: * "Name of selected coupon" is displayed at the left side of Coupons sub-header
        EXPECTED: * "Change Coupon" link and image is displayed at the right side of Coupons sub-header (Only for Coral Brand)
        """
        pass

    def test_003_verify_the_cs_coupon_page_content(self):
        """
        DESCRIPTION: Verify the CS Coupon page content
        EXPECTED: Content is the table of events, those added to the coupon. Each row of the table contains
        EXPECTED: * In the first column
        EXPECTED: * Time and date of the match
        EXPECTED: * Home and Away teams names (Home in the top)
        EXPECTED: * In the Home column: Score switcher for Home Team, default score: 0
        EXPECTED: * In the Away column: Score switcher for Away Team, default score: 0
        EXPECTED: * Price button that displays the odd of the selection
        """
        pass

    def test_004_verify_the_events_ordering(self):
        """
        DESCRIPTION: Verify the Events ordering
        EXPECTED: Event are ordered by date/time and alphabetically:
        EXPECTED: * Soonest go first
        EXPECTED: * In alphabet order if date and time are the same, by Home team name
        """
        pass
