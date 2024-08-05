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
class Test_C16404249_Tier_1_Verify_Matches_tab_displaying_based_on_the_state_of_Check_Events_checkbox_in_CMS(Common):
    """
    TR_ID: C16404249
    NAME: [Tier 1] Verify 'Matches' tab displaying based on the state of 'Check Events' checkbox in CMS
    DESCRIPTION: This test case verifies 'Matches' tab displaying based on the state of 'Check Events' checkbox in CMS
    DESCRIPTION: "Check Events" checkbox is unticked in CMS by default for 'Matches' tab for Tier 1 type. It means that particular tab will be displayed without any dependency on the availability of data on SS and value received in 'hasEvents' parameter.
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 1 Sport Landing page where 'Matches' tab is enabled in CMS ('checkEvents: false' set by default and can not be edited)
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

    def test_001_verify_matches_tabs_displaying_if_check_events_checkbox_is_disabled_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Check Events' checkbox is disabled and data is received from SS
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * Events received from SS are displayed
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002_verify_matches_tabs_displaying_if_check_events_checkbox_is_disabled_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if 'Check Events' checkbox is disabled and data is NOT received from SS
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * 'No events found' message is displayed on the page
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass
