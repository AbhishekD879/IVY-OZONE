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
class Test_C9836606_Tier_1_Verify_Matches_tab_displaying_based_on_received_data_from_SS_and_state_of_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C9836606
    NAME: [Tier 1] Verify 'Matches' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Matches' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    DESCRIPTION: **NOTE:**
    DESCRIPTION: 'Matches' tab must be enabled all the time for Tier 1 Sports.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 1 Sport Landing page where 'Matches' tab is enabled in CMS ('checkEvents: false' is set by default for Tier 1 and can not be edited)
    PRECONDITIONS: 3. No sport modules should be created (i.e. Inplay module, Quick Links, Highlight Carousel, etc) for that Tier 1 sport
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Matches' tab is available in CMS for all Tier types
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: - To verify Matches availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXXXX?&simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&existsFilter=event:simpleFilter:market.dispSortName:intersects:MR&simpleFilter=event.suspendAtTime:greaterThan:2019-03-21T13:32:30.000Z&translationLang=en&count=event:market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    PRECONDITIONS: - XXXXX - Class Id
    """
    keep_browser_open = True

    def test_001_verify_matches_tab_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tab displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * List of events received from SS is displayed
        EXPECTED: * Response with available data for 'Matches' tab is received from SS
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002_verify_matches_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * Response is received from SS with no data for 'Matches' tab
        EXPECTED: * 'No events found' message is present
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_003_verify_matches_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Matches' tab is NOT present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: true'** parameter
        EXPECTED: * Response with available data for 'Matches' tab is NOT received from SS
        EXPECTED: * The first tab is selected by default instead of 'Matches'
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        EXPECTED: **For Desktop:**
        EXPECTED: 'Matches' tab is present on Sports Landing page all the time regardless of cms settings or data availability
        """
        pass
