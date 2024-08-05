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
class Test_C2601241_Verify_Correct_Score_coupon_displaying_on_the_Coupons_home_page(Common):
    """
    TR_ID: C2601241
    NAME: Verify Correct Score coupon displaying on the Coupons home page
    DESCRIPTION: 
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. There is Correct Score coupon configured in TI tool with available active events.
    PRECONDITIONS: 2. Open Coupons(ACCAS) homepage in application
    """
    keep_browser_open = True

    def test_001_verify_correct_score_coupon_displaying_in_the_appropriate_section_featured_popular_etc_depending_on_cms_configuration(self):
        """
        DESCRIPTION: Verify Correct Score coupon displaying in the appropriate section (Featured, Popular, etc depending on CMS configuration)
        EXPECTED: CS Coupon is displayed in appropriate section
        """
        pass

    def test_002_verify_coupon_ordering_within_the_section(self):
        """
        DESCRIPTION: Verify Coupon ordering within the section
        EXPECTED: Coupon ordered in accordance with the CMS ordering settings
        """
        pass

    def test_003_verify_coupon_isnt_displayed_within_the_other_sections(self):
        """
        DESCRIPTION: Verify Coupon isn't displayed within the other sections
        EXPECTED: CS Coupon is displayed within the defined section and is absent within the other sections
        """
        pass
