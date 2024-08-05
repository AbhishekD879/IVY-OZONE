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
class Test_C10469348_To_Archive_from_1012_and_1005_Verify_events_filtering_on_the_Competitions_tab(Common):
    """
    TR_ID: C10469348
    NAME: [To Archive from 101.2 and 100.5] Verify events filtering on the 'Competitions' tab
    DESCRIPTION: This test case verifies that only events with a condition of an event start time being more than 48h from the current time appear within 'Competitions' tab
    DESCRIPTION: **Should be archived from 101.2 Coral and 100.5 Ladbrokes**
    PRECONDITIONS: 1) No upcoming events with a 'Start Time' value >= 'Current Time' + 48H:01M.
    PRECONDITIONS: 2) Load Oxygen app
    PRECONDITIONS: 3) Navigate to a selected 'Tier 2' Sports Landing Page
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - 'Competitions' tab is available in CMS for Tier 1 & Tier 2 types
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Competitions availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    """
    keep_browser_open = True

    def test_001_verify_that_competitions_tab_is_not_shown(self):
        """
        DESCRIPTION: Verify that 'Competitions' tab is not shown
        EXPECTED: Only 'Matches' and 'Outrights' tabs are shown, with a 'Matches' being opened by default
        EXPECTED: (in case the data is available for tabs mentioned above)
        """
        pass

    def test_002_create_an_event_within_the_ti_with_following_settings__start_time_value__current_time_plus_48h01m__is_off_value_is_set_to_no__bet_in_playlist_is_set_to_false(self):
        """
        DESCRIPTION: Create an event within the TI, with following settings:
        DESCRIPTION: - 'Start Time' value >= 'Current Time' + 48H:01M
        DESCRIPTION: - 'is Off' value is set to 'No'
        DESCRIPTION: - 'Bet in Playlist' is set to 'false'
        EXPECTED: Event is successfully created, but 'Competitions' tab doesn't appear
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Competitions' tab appears
        """
        pass

    def test_004_switch_to_competitions_tab(self):
        """
        DESCRIPTION: Switch to Competitions' tab
        EXPECTED: 'Competitions' tab contains the event created in step 2
        """
        pass

    def test_005_wait_5_minutes_and_refresh_the_page(self):
        """
        DESCRIPTION: Wait 5 minutes and refresh the page
        EXPECTED: 'Competitions' tab is no longer shown
        EXPECTED: 'Matches' tab is opened
        EXPECTED: Event from step 2 is now shown in the 'Matches' tab
        """
        pass
