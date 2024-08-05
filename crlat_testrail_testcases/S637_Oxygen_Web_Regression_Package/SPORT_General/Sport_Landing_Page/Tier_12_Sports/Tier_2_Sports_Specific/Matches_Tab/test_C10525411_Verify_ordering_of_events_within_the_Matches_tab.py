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
class Test_C10525411_Verify_ordering_of_events_within_the_Matches_tab(Common):
    """
    TR_ID: C10525411
    NAME: Verify ordering of events within the Matches tab
    DESCRIPTION: This test case verifies ordering of events being present on a lists level (Today/Tomorrow) within a league, as well as League ordering - for the League(s) section with upcoming events.
    PRECONDITIONS: 0) No upcoming events with a 'Start Time' value <= '00:00 AM Current Date' + 47H:59M or 23H:59M should be set for the selected 'Tier 2' sport; No 'Live' events are set for the selected 'Tier 2' sport.
    PRECONDITIONS: 1) Load Oxygen app
    PRECONDITIONS: 2) Navigate to a chosen 'Tier 2' Sports Landing Page
    PRECONDITIONS: 3) 'Matches' tab is opened
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

    def test_001_create_an_event_within_the_tifor_this_sport_with_following_settings__league_type_disporder_should_have_the_highestclosest_to_positive_or_positive_valueorname_of_the_league_type_should_start_from_the_letter_that_is_last_within_the_list_of_names__start_time_value__0000_am_current_date_plus_45h55m__is_off_value_is_set_to_no__stream_availablemapped_flags_are_set(self):
        """
        DESCRIPTION: Create an event within the TI(for this sport), with following settings:
        DESCRIPTION: - League (Type) 'Disporder' should have the highest(closest to positive or positive) value
        DESCRIPTION: OR
        DESCRIPTION: Name of the League (Type) should start from the letter, that is last within the list of names.
        DESCRIPTION: - 'Start Time' value = '00:00 AM Current Date' + 45H:55M
        DESCRIPTION: - 'is Off' value is set to 'No'
        DESCRIPTION: - 'Stream available/mapped' flags are set
        EXPECTED: Event is successfully created, but 'No events found' label remains being shown
        """
        pass

    def test_002_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Expanded league created with the event in 'Step 1' is shown
        EXPECTED: Event is shown in the 'Tomorrow' list of events
        EXPECTED: League(Type) is displayed as first in the Tab.
        """
        pass

    def test_003_create_an_event_within_the_tifor_this_sport_with_following_settings__league_should_be_the_same_as_one_from_step_1__start_time_value__0000_am_current_date_plus_23h55m__is_off_value_is_set_to_no__stream_availablemapped_flags_are_set(self):
        """
        DESCRIPTION: Create an event within the TI(for this sport), with following settings:
        DESCRIPTION: - League should be the same as one from 'Step 1'
        DESCRIPTION: - 'Start Time' value = '00:00 AM Current Date' + 23H:55M
        DESCRIPTION: - 'is Off' value is set to 'No'
        DESCRIPTION: - 'Stream available/mapped' flags are set
        EXPECTED: Event is successfully created, but not shown in the existing league
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Expanded league that appeared in 'Step 2' changes its content
        EXPECTED: 'Today' list of events with the event from 'Step 3' is shown above the 'Tomorrow' list of events with the event from 'Step 1'
        """
        pass

    def test_005_create_an_event_within_the_tifor_this_sport_with_following_settings__league_type_disporder_should_have_the_lowestclosest_to_negative_or_negative_valueorname_of_the_league_type_should_start_from_the_letter_that_is_first_within_the_list_of_names__start_time_value__0000_am_current_date_plus_47h55m__is_off_value_is_set_to_no__stream_availablemapped_flags_are_set(self):
        """
        DESCRIPTION: Create an event within the TI(for this sport), with following settings:
        DESCRIPTION: - League (Type) 'Disporder' should have the lowest(closest to negative or negative) value
        DESCRIPTION: OR
        DESCRIPTION: Name of the League (Type) should start from the letter, that is first within the list of names.
        DESCRIPTION: - 'Start Time' value = '00:00 AM Current Date' + 47H:55M
        DESCRIPTION: - 'is Off' value is set to 'No'
        DESCRIPTION: - 'Stream available/mapped' flags are set
        EXPECTED: Event is successfully created, but a new league is not shown
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Expanded league created in 'Step 5' is shown above the league created in 'Step 1'
        EXPECTED: Event is shown in the 'Tomorrow' list of events for the league from 'Step 5'
        """
        pass
