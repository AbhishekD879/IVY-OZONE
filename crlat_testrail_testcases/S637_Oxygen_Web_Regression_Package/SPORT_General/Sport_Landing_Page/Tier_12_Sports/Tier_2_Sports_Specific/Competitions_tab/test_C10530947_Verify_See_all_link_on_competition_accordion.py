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
class Test_C10530947_Verify_See_all_link_on_competition_accordion(Common):
    """
    TR_ID: C10530947
    NAME: Verify 'See all' link on competition accordion
    DESCRIPTION: This test case verifies when 'See all' link appears on competition accordion and redirection to Competition details page
    PRECONDITIONS: 1. Make sure that the following events are created in TI for any Tier 2 Sport:
    PRECONDITIONS: - events are within the same competition
    PRECONDITIONS: - events count is at least 4
    PRECONDITIONS: 2. Make sure that the Events Limit is configured in CMS and equal '3' by default (System Configuration -> Structure -> SportCompetitionsTab)
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Navigate to the Sport Landing page
    PRECONDITIONS: 5. Click/Tap on 'Competitions' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    """
    keep_browser_open = True

    def test_001_verify_number_of_events_displayed(self):
        """
        DESCRIPTION: Verify number of events displayed
        EXPECTED: * First 3 events are displayed
        EXPECTED: * 4th event is not shown
        EXPECTED: * 'See all' link is present on expanded accordion
        """
        pass

    def test_002_click_on_see_all_link(self):
        """
        DESCRIPTION: Click on 'See all' link
        EXPECTED: * Redirection to respective Competition details page occur
        EXPECTED: * All events that belong to that competition are displayed
        """
        pass

    def test_003__in_ti_undisplay_one_of_created_4_events_in_app_navigate_to_sport_landing_page_under_test__competitions_tab_verify_number_of_events_displayed(self):
        """
        DESCRIPTION: * In TI undisplay one of created 4 events
        DESCRIPTION: * In app navigate to Sport Landing page under test > 'Competitions' tab
        DESCRIPTION: * Verify number of events displayed
        EXPECTED: * 3 events are displayed
        EXPECTED: * 'See all' link is NOT present on expanded accordion
        """
        pass

    def test_004__in_ti_display_undisplayed_in_step_3_event_in_cms_increase_limit_of_events_to_4_system_configuration___structure___sportcompetitionstab_in_app_navigate_to_sport_landing_page_under_test__competitions_tab_verify_number_of_events_displayed(self):
        """
        DESCRIPTION: * In TI display undisplayed in 'Step 3' Event
        DESCRIPTION: * In CMS increase limit of Events to 4 (System Configuration -> Structure -> SportCompetitionsTab)
        DESCRIPTION: * In app navigate to Sport Landing page under test > 'Competitions' tab
        DESCRIPTION: * Verify number of events displayed
        EXPECTED: * 4 events are displayed
        EXPECTED: * 'See all' link is NOT present on expanded accordion
        """
        pass
