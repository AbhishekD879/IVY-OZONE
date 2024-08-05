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
class Test_C49044744_Tier_1_Verify_Competitions_tab_displaying_based_on_data_availability_on_SS(Common):
    """
    TR_ID: C49044744
    NAME: [Tier 1] Verify 'Competitions' tab displaying based on data availability on SS
    DESCRIPTION: This test case verifies 'Competitions' tab displaying based on data availability on SS [Tier 1]
    DESCRIPTION: 'Check Events' status is inactive in CMS by default for the 'Competitions' tab for Tier 1 Sports only. It means that a particular tab will be displayed without any dependency on the availability of data on SS.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Competitions' tab is enabled in CMS and 'CheckEvents' is inactive (Tier 1)
    PRECONDITIONS: **Sports Page Configs documentation:**
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-tab> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-tab/<Category ID>
    PRECONDITIONS: - To verify data availability on SS use the next links:
    PRECONDITIONS: - To get all Classes per Sport:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category ID
    PRECONDITIONS: - To get all available Events per Sport:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXXXX?&simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&existsFilter=event:simpleFilter:market.dispSortName:intersects:HH&simpleFilter=event.suspendAtTime:greaterThan:2019-03-19T10:39:30.000Z&translationLang=en&count=event:market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXX= Class ID
    PRECONDITIONS: - XX - Category ID
    PRECONDITIONS: - To get all available Events, Markets and Outcomes:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXXX?simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&simpleFilter=market.dispSortName:intersects:HH&existsFilter=event:simpleFilter:market.dispSortName:intersects:HH&simpleFilter=market.collectionNames:intersects:|Match%20Betting|&simpleFilter=event.suspendAtTime:greaterThan:2019-03-19T10:39:30.000Z&translationLang=en&prune=event&prune=market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XXXXX= Class ID
    PRECONDITIONS: - XX - Category ID
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking see:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: - Use KIBANA for verifying queries from CMS to SiteServe:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Symphony+Infrastructure+creds
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121568063)
    """
    keep_browser_open = True

    def test_001_verify_competitions_tabs_displaying_when_check_events_status_is_inactive_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying when 'Check Events' status is inactive and data is received from SS
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response
        EXPECTED: * Data received from SS is displayed (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass

    def test_002_verify_competitions_tabs_displaying_when_check_events_is_inactive_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying when 'Check Events' is inactive and data is NOT received from SS
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * 'No markets available' message is displayed on the page
        """
        pass
