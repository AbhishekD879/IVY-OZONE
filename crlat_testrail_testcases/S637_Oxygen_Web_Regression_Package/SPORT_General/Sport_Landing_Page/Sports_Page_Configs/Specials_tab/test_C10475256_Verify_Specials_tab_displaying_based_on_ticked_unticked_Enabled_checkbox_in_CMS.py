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
class Test_C10475256_Verify_Specials_tab_displaying_based_on_ticked_unticked_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C10475256
    NAME: Verify 'Specials' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Specials' tab displaying based on ticked/unticked 'Enabled' checkbox in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page where 'Specials' tab is enabled in CMS and 'CheckEvents' checkbox is ticked
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Specials' tab is available in CMS for Football only
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-tabs/<Category ID>
    PRECONDITIONS: - To verify Specials availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXXX?simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_SP&simpleFilter=event.suspendAtTime:greaterThan:2019-03-18T16:20:00.000Z&translationLang=en&prune=event&prune=market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXXXX - class ID
    PRECONDITIONS: - XX - category ID
    """
    keep_browser_open = True

    def test_001_verify_specials_tab_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Specials' tab displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Specials' tab is present on Football Landing page
        EXPECTED: * 'Specials' tab is received in <сategory> response
        EXPECTED: * Data received from SS is displayed
        EXPECTED: * Response with available data for 'Specials' tab is received from SS
        """
        pass

    def test_002_verify_specials_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Specials' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Specials' tab is NOT present on Football Landing page
        EXPECTED: * 'Specials' tab is NOT received in <сategory> response
        EXPECTED: * Response is NOT received from SS
        """
        pass

    def test_003_verify_specials_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Specials' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Specials' tab is NOT present on Football Landing page
        EXPECTED: * 'Specials' tab is NOT received in <сategory> response
        EXPECTED: * Response with available data for 'Specials' tab is NOT received from SS
        """
        pass
