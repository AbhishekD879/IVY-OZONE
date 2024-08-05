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
class Test_C9776603_Verify_Coupons_tab_displaying_based_on_ticked_unticked_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C9776603
    NAME: Verify 'Coupons' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Coupons' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    DESCRIPTION: **Be aware that from 102.2 Ladbrokes and Coral releases 'Coupons' tab should be disabled by default for all Tier types except Tier 1**
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: - To verify Coupons availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2019-03-04T22:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2019-03-05T16:01:00.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:XX&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Coupons' tab is enabled in CMS and 'CheckEvents' checkbox is ticked
    """
    keep_browser_open = True

    def test_001_verify_coupons_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Coupons' tabs displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Coupons' tab is present on Sports Landing page
        EXPECTED: * 'Coupons' tab is received in <sport-config response with **hidden: false** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * List of Coupons received from SS is displayed
        EXPECTED: * Response with available data for 'Coupons' tab is received from SS
        """
        pass

    def test_002_verify_coupons_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Coupons' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Coupons' tab is NOT present on Sports Landing page
        EXPECTED: * 'Coupons' tab is received in <sport-config response with **hidden: true** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Response is NOT received from SS
        """
        pass

    def test_003_verify_coupons_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Coupons' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Coupons' tab is NOT present on Sports Landing page
        EXPECTED: * 'Coupons' tab is received in <sport-config response with **hidden: true** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Response with available data for 'Coupons' tab is NOT received from SS
        """
        pass
