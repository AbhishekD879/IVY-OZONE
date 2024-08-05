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
class Test_C10475257_Verify_Specials_tab_displaying_based_on_enabled_disabled_Check_Events_checkbox_in_CMS_For_Football_only(Common):
    """
    TR_ID: C10475257
    NAME: Verify 'Specials' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS (For Football only)
    DESCRIPTION: This test case verifies 'Specials' tab displaying based on enabled/disabled 'Check Events' checkbox in CMS and availability of data from SS
    DESCRIPTION: "Check Events" checkbox is ticked and disabled in CMS by default for 'Specials' tab. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page where 'Specials' tab is enabled in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Specials' tab is available in CMS for Football only
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776323 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-tabs/<Category ID>
    PRECONDITIONS: - To verify Specials availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXXX?simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_SP&simpleFilter=event.suspendAtTime:greaterThan:2019-03-18T16:20:00.000Z&translationLang=en&prune=event&prune=market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXXXX - class ID
    PRECONDITIONS: - XX - category ID
    """
    keep_browser_open = True

    def test_001_verify_specials_tabs_displaying_if_check_events_checkbox_is_enabled_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Specials' tabs displaying if 'Check Events' checkbox is enabled and data is received from SS
        EXPECTED: * 'Specials' tab is present on Football Landing page
        EXPECTED: * 'Specials' tab is received in <сategory> response
        EXPECTED: * Data received from SS is displayed on the page
        """
        pass

    def test_002_verify_specials_tabs_displaying_if_check_events_checkbox_is_enabled_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Specials' tabs displaying if 'Check Events' checkbox is enabled and data is NOT received from SS
        EXPECTED: * 'Specials' tab is NOT present on Football Landing page
        EXPECTED: * 'Specials' tab is NOT received in <сategory> response
        """
        pass
