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
class Test_C10474863_Verify_upcoming_events_filtering_on_Matches_tab(Common):
    """
    TR_ID: C10474863
    NAME: Verify upcoming events filtering on Matches tab
    DESCRIPTION: This test case verifies events displaying on 'Matches' tab in case start time is less than Current time + 48H
    PRECONDITIONS: 1) No events with a 'Start Time' value <= Current time + 48H. Should be set for the selected 'Tier 2' sport; No 'Live' events are set for the selected 'Tier 2' sport.
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

    def test_001_verify_that_matches_tab_is_shown(self):
        """
        DESCRIPTION: Verify that 'Matches' tab is shown
        EXPECTED: 'Matches' Tab is shown
        EXPECTED: 'No events found' label is shown below the tabs lane
        EXPECTED: FROM OX100:
        EXPECTED: In case no available events for particular Sport, user navigates to the Homepage when tapping on Sport icon from Sports Menu Ribbon.
        """
        pass

    def test_002_create_an_event_within_the_tifor_this_sport_with_following_settings__start_time_value__current_time_plus_48h__is_off_value_is_set_to_no__bet_in_playlist_is_set_to_false(self):
        """
        DESCRIPTION: Create an event within the TI(for this sport), with following settings:
        DESCRIPTION: - 'Start Time' value <= Current time + 48H
        DESCRIPTION: - 'is Off' value is set to 'No'
        DESCRIPTION: - 'Bet in Playlist' is set to 'false'
        EXPECTED: Event is successfully created
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Event is shown in the 'Matches' tab
        """
        pass
