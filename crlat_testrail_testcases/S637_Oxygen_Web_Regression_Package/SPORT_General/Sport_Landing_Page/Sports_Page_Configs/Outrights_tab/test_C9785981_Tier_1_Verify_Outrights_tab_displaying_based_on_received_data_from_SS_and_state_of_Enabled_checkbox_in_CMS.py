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
class Test_C9785981_Tier_1_Verify_Outrights_tab_displaying_based_on_received_data_from_SS_and_state_of_Enabled_checkbox_in_CMS(Common):
    """
    TR_ID: C9785981
    NAME: [Tier 1] Verify 'Outrights' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    DESCRIPTION: This test case verifies 'Outrights' tab displaying based on received data from SS and state of 'Enabled' checkbox in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tier 1 Sport Landing page where 'Outrights' tab is enabled in CMS ('checkEvents: 'false' set by default for Tier 1)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Outrights' tab is available in CMS for all Tier types
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121534814)
    PRECONDITIONS: - To verify Outrights availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXXX?simpleFilter=event.categoryId:intersects:34&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.eventSortCode:intersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=event.suspendAtTime:greaterThan:2019-03-06T15:15:30.000Z&translationLang=en&prune=event&prune=market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    PRECONDITIONS: - XXXX - Class Id
    """
    keep_browser_open = True

    def test_001_verify_outright_tab_displaying_if_enabled_checkbox_is_ticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Outright' tab displaying if 'Enabled' checkbox is ticked and data is available on SS
        EXPECTED: * 'Outright' tab is present on Sports Landing page
        EXPECTED: * 'Outright' tab is received in <sport-config> response with **'hidden: false'** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * List of Outrights received from SS is displayed
        EXPECTED: * Response with available data for 'Outrights' tab is received from SS
        """
        pass

    def test_002_verify_outrights_tabs_displaying_if_enabled_checkbox_is_ticked_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Outrights' tabs displaying if 'Enabled' checkbox is ticked and data is NOT available on SS
        EXPECTED: * 'Outrights' tab is present on Sports Landing page
        EXPECTED: with 'No events found' message
        EXPECTED: * 'Outright' tab is received in <sport-config> response with **'hidden: false'** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Response from SS regarding 'Outrights' tab content contains no data
        """
        pass

    def test_003_verify_outrights_tabs_displaying_if_enabled_checkbox_is_unticked_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Outrights' tabs displaying if 'Enabled' checkbox is unticked and data is available on SS
        EXPECTED: * 'Outrights' tab is NOT present on Sports Landing page
        EXPECTED: * 'Outright' tab is received in <sport-config> response with **'hidden: true'** parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Response with available data for 'Outrights' tab is NOT received from SS
        """
        pass
