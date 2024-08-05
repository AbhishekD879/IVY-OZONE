import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - events can't be created on prod/beta
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C3019573_Verify_Navigation_to_Competition_Page_through_See_all_link_on_Tier_2_Sport_Landing_page(Common):
    """
    TR_ID: C3019573
    NAME: Verify Navigation to Competition Page through 'See all' link on Tier 2 Sport Landing page
    DESCRIPTION: This test case verifies navigation from Matches tab of sport landing page to Competitions page when user clicks on 'SEE ALL (#)' link in the type header within the section with upcoming events.
    DESCRIPTION: The list of sports that are tier I/II/III is available here: https://docs.google.com/spreadsheets/d/1dLDjAkrGpCPRzhVbojt2_tfd8upB82uoU0E-CYojkfY/edit?ts=5c0f928b#gid=0
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 23H:55M
        PRECONDITIONS: 2) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 47H:55M
        PRECONDITIONS: 3) All aforementioned events should be created under the same league (type)
        PRECONDITIONS: Oxygen app is running
        PRECONDITIONS: Upcoming events are available for the chosen TIER_2_SPORT
        """
        start_time_upcoming_for_event1 = self.get_date_time_formatted_string(hours=23, minutes=55)
        self.ob_config.add_snooker_event_to_snooker_all_snooker(start_time=start_time_upcoming_for_event1)
        start_time_upcoming_for_event2 = self.get_date_time_formatted_string(hours=47, minutes=55)
        self.ob_config.add_snooker_event_to_snooker_all_snooker(start_time=start_time_upcoming_for_event2)
        self.ob_config.add_snooker_event_to_snooker_all_snooker()
        self.ob_config.add_snooker_event_to_snooker_all_snooker()
        self.site.wait_content_state('Homepage')

    def test_001_click_on_the_chosen_tier_2_sport_icon_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on the chosen TIER_2_SPORT icon in menu ribbon
        EXPECTED: Sport landing page loads
        """
        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')

    def test_002_click_on_a_see_all_link_for_the_league_within_the_leagues_section_with_upcoming_events(self):
        """
        DESCRIPTION: Click on a 'SEE ALL' link for the League within the League(s) section with upcoming events
        EXPECTED: User is redirected to a Competitions page with a content related to a clicked league:
        EXPECTED: https://#ENVIRONMENT/competitions/#TIER_2_SPORT/#TIER_2_SPORT/#LEAGUE_NAME
        EXPECTED: 'Matches' tab loads by default
        EXPECTED: Tab should contain only upcoming events, divided into lists with Event card(s) header with league date (i.e. Today/Tomorrow/##_Month) and selection names (i.e. home/draw/away)
        """
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        section_name, section = list(sections.items())[0]
        has_see_all_link = section.group_header.has_see_all_link()
        self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
        section.group_header.see_all_link.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No list of available events are present on competition league page')
        self.assertIn('Today' if self.brand == 'bma' else 'TODAY', sections.keys(),
                      msg=f'Event card header: {"Today" if self.brand == "bma" else "TODAY"} is not present in the actual Events cards headers list: "{sections.keys()}"')
        self.assertIn('Tomorrow' if self.brand == 'bma' else 'TOMORROW', sections.keys(),
                      msg=f'Event card header: {"Tomorrow" if self.brand == "bma" else "TOMORROW"} is not present in the actual Events cards headers list: "{sections.keys()}"')
        self.assertGreaterEqual(len(sections), 3,
                                msg=f'Created events for today, tomorrow and next day but events are available only for "{sections.keys()}"')
        for i in range(len(sections)):
            fixture_header = list(sections.values())[i].fixture_header
            self.assertEqual(fixture_header.header1, '1',
                             msg=f'Actual Fixture header: "{fixture_header.header1}" is not same as Expected Fixture header: "1"')
            self.assertEqual(fixture_header.header3, '2',
                             msg=f'Actual Fixture header: "{fixture_header.header3}" is not same as Expected Fixture header: "2"')
