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
class Test_C10359227_Verify_Jackpot_tab_displaying_based_on_enabled_disabled_Check_Events_checkbox_in_CMS_For_Football_only(Common):
    """
    TR_ID: C10359227
    NAME: Verify 'Jackpot' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS (For Football only)
    DESCRIPTION: This test case verifies 'Jackpot' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS and availability of data from SS
    DESCRIPTION: "Check Events" checkbox is ticked and disabled in CMS by default for 'Jackpot' tab. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Jackpot' tab is enabled in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Jackpot' tab is available in CMS for Football only
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776323 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-tabs/<CategoryID>
    PRECONDITIONS: - To verify Jackpot availability on SS use the next link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?translationLang=en&simpleFilter=pool.type:equals:XXX&simpleFilter=pool.isActive
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXX - typeName
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/XXXXXXX,?simpleFilter=event.isStarted:isFalse&translationLang=en
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXXXX - market Id
    """
    keep_browser_open = True

    def test_001_verify_jackpot_tabs_displaying_if_check_events_checkbox_is_enabled_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Jackpot' tabs displaying if 'Check Events' checkbox is enabled and data is received from SS
        EXPECTED: * 'Jackpot' tab is present on Sports Landing page
        EXPECTED: * 'Jackpot' tab is received in <sport-tabs> response
        EXPECTED: * Data received from SS is displayed on the page
        """
        pass

    def test_002_verify_jackpot_tabs_displaying_if_check_events_checkbox_is_enabled_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Jackpot' tabs displaying if 'Check Events' checkbox is enabled and data is NOT received from SS
        EXPECTED: * 'Jackpot' tab is NOT present on Sports Landing page
        EXPECTED: * 'Jackpot' tab is NOT received in <sport-tabs> response
        """
        pass
