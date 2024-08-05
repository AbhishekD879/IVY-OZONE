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
class Test_C16408225_Tier_1_Verify_Outright_tab_displaying_based_on_enabled_disabled_Check_Events_checkbox_in_CMS(Common):
    """
    TR_ID: C16408225
    NAME: [Tier 1] Verify 'Outright' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS
    DESCRIPTION: This test case verifies 'Outright' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS
    DESCRIPTION: "Check Events" checkbox is unticked and disabled in CMS by default for 'Outrights' tab for Tier 1 types. It means that particular tab will be displayed without any dependency on the availability of data on SS and value received in 'hasEvents' parameter.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 1 Sport Landing page where 'Outright' tab is enabled in CMS ('checkEvents: 'false' set by default and cannot be edited)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Outright' tab is available in CMS for all Tier types
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: - To verify Outright availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2019-03-04T22:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2019-03-05T16:01:00.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:XX&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    """
    keep_browser_open = True

    def test_001_verify_outright_tab_displaying_if_check_events_is_false_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Outright' tab displaying if 'Check Events' is false and data is received from SS
        EXPECTED: * 'Outright' tab is present on Sports Landing page
        EXPECTED: * 'Outright' tab is received in <sport-config> response with **'hidden: false'** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * List of Outrights received from SS is displayed
        """
        pass

    def test_002_verify_outright_tab_displaying_if_check_events_is_false_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Outright' tab displaying if 'Check Events' is false and data is NOT received from SS
        EXPECTED: * 'Outright' tab is present on Sports Landing page
        EXPECTED: * 'Outright' tab is received in <sport-config> response with **'hidden: false'** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * 'No events found' message is displayed on the page
        """
        pass
