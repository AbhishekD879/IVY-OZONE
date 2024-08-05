import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.time_league_filters
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64004667_Verify_the_functionality_of_the_See_All_option_in_the_Sports_Landing_Page_Matches_Tab(Common):
    """
    TR_ID: C64004667
    NAME: Verify the functionality of the 'See All' option in the Sports Landing Page (Matches Tab)
    DESCRIPTION: This test case verifies the functionality of the navigation of user from the Matches tab to the Competitions tab using the 'See All' option.
    PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    """
    keep_browser_open = True

    def test_001_navigate_to_any_of_the_tier_1_or_tier_2_sportsmatches_tab(self):
        """
        DESCRIPTION: Navigate to any of the Tier 1 or Tier 2 sports.(Matches Tab)
        EXPECTED: Verify that the user able to navigate to the Matches tab of the specific sport.
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_select_the_see_all_link_which_is_available_on_the_accordion_for_that_specific_sport_on_the_matches_tab(self):
        """
        DESCRIPTION: Select the 'See All' link which is available on the accordion for that specific sport on the Matches tab.
        EXPECTED: The user should be navigated to the respective Competitions page with only the Time filters available.
        Note: 'See All' link is applicable for mobile tablet only
        """
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        section_name, section = list(sections.items())[0]
        has_see_all_link = section.group_header.has_see_all_link()
        self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
        section.group_header.see_all_link.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        filters = self.site.competition_league.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='No filters available on competition league page')
