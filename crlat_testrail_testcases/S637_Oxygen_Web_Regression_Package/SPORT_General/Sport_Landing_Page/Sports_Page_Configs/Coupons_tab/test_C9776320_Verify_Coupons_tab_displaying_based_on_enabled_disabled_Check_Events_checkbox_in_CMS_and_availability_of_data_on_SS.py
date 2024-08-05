import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C9776320_Verify_Coupons_tab_displaying_based_on_enabled_disabled_Check_Events_checkbox_in_CMS_and_availability_of_data_on_SS(Common):
    """
    TR_ID: C9776320
    NAME: Verify 'Coupons' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS and availability of data on SS
    DESCRIPTION: This test case verifies 'Coupons' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS and availability of data on SS
    DESCRIPTION: "Check Events" checkbox is ticked and greyed out in CMS by default for 'Coupons' tab for all Tier types. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
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
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Coupons' tab is enabled in CMS and data is received from SS
    """
    keep_browser_open = True

    def test_001_verify_coupons_tabs_displaying_when_check_events_checkbox_is_enabled_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Coupons' tabs displaying when 'Check Events' checkbox is enabled and data is received from SS
        EXPECTED: * 'Coupons' tab is present on Sports Landing page
        EXPECTED: * 'Coupons' tab is received in <sport-config response with **hidden: false** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * List of Coupons received from SS is displayed
        """
        pass

    def test_002_verify_coupons_tabs_displaying_when_check_events_checkbox_is_enabled_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Coupons' tabs displaying when 'Check Events' checkbox is enabled and data is NOT received from SS
        EXPECTED: * 'Coupons' tab is NOT present on Sports Landing page
        EXPECTED: * 'Coupons' tab is received in <sport-config response with **hidden: true** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass
