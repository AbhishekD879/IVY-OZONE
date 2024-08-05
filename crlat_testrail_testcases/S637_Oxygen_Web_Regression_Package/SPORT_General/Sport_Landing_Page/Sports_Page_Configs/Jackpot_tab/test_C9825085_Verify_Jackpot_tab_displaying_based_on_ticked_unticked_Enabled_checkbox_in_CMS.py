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
class Test_C9825085_Verify_Jackpot_tab_displaying_based_on_ticked_unticked_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C9825085
    NAME: Verify 'Jackpot' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Jackpot' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page where 'Jackpot' tab is enabled in CMS and 'CheckEvents' checkbox is ticked
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Jackpot' tab is available in CMS for Football only
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-tabs/<CategoryID>
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: - To verify Jackpot availability on SS use the next link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?translationLang=en&simpleFilter=pool.type:equals:XXX&simpleFilter=pool.isActive
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXX - typeName
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/XXXXXXX,?simpleFilter=event.isStarted:isFalse&translationLang=en
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXXXX - market Id
    """
    keep_browser_open = True

    def test_001_verify_jackpot_tab_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Jackpot' tab displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Jackpot' tab is present on Sports Landing page
        EXPECTED: * 'Jackpot' tab is received in <sport-tabs> response
        EXPECTED: * Data received from SS is displayed
        EXPECTED: * Response with available data for 'Jackpot' tab is received from SS
        """
        pass

    def test_002_verify_jackpot_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Jackpot' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Jackpot' tab is NOT present on Football Landing page
        EXPECTED: * 'Jackpot' tab is NOT received in <sport-tabs> response
        EXPECTED: * Response is NOT received from SS
        """
        pass

    def test_003_verify_jackpot_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Jackpot' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Jackpot' tab is NOT present on Football Landing page
        EXPECTED: * 'Jackpot' tab is NOT received in <sport-tabs> response
        EXPECTED: * Response with available data for 'Jackpot' tab is NOT received from SS
        """
        pass
