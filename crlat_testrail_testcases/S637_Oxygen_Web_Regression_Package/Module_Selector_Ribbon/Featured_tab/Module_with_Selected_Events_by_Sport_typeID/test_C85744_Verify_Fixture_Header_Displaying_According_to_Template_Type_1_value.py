import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C85744_Verify_Fixture_Header_Displaying_According_to_Template_Type_1_value(Common):
    """
    TR_ID: C85744
    NAME: Verify Fixture Header Displaying According to 'Template Type 1' value
    DESCRIPTION: 
    PRECONDITIONS: Make sure Olympics Sports are included in build of app
    """
    keep_browser_open = True

    def test_001_load_cms_and_go_to_olympic_sports(self):
        """
        DESCRIPTION: Load CMS and go to 'Olympic Sports'
        EXPECTED: 'Olympic Sports' page is opened
        """
        pass

    def test_002_go_to_any_sport_which_primary_market_is_a_3_way_market_eg_football_boxing_etc(self):
        """
        DESCRIPTION: Go to any sport which primary market is a 3 Way market (e.g. Football, Boxing etc.)
        EXPECTED: Page for particular sport is opened
        """
        pass

    def test_003_go_to_template_test_1_field_and_check_the_value(self):
        """
        DESCRIPTION: Go to 'Template Test 1' field and check the value
        EXPECTED: A dropdown with two options is displayed:
        EXPECTED: - Home Draw Away
        EXPECTED: - One Two Type
        EXPECTED: 'Home Draw Away' template is selected by default
        """
        pass

    def test_004_change_the_template_to_one_two_type_and_save_changes(self):
        """
        DESCRIPTION: Change the template to 'One Two Type' and Save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Oxygen app is opened
        """
        pass

    def test_006_go_to_the_sport_page_for_sport_from_step_2(self):
        """
        DESCRIPTION: Go to the sport page for sport from step #2
        EXPECTED: Sport landing page is opened
        """
        pass

    def test_007_verify_fixture_header_displaying_for_primary_market_for_mtch_events(self):
        """
        DESCRIPTION: Verify fixture header displaying for primary market for MTCH events
        EXPECTED: Fixture header '1 2' is shown
        EXPECTED: - 1 corresponds to Home selection
        EXPECTED: - 2 corresponds to Away selection
        """
        pass

    def test_008_go_to_event_details_page_and_check_primary_market(self):
        """
        DESCRIPTION: Go to event details page and check primary market
        EXPECTED: Home Draw and Away selections are shown (nothing is changed on event details page)
        """
        pass

    def test_009_repeat_steps_7___8_for_the_following_areas__featured_tab__in_play_page__in_play_tab_on_module_selector_ribbon__live_stream_tab_on_module_selector_ribbon__tomorrowfuturein_ply_tabs_on_sport_page(self):
        """
        DESCRIPTION: Repeat steps 7 - 8 for the following areas:
        DESCRIPTION: - Featured tab
        DESCRIPTION: - In-Play page
        DESCRIPTION: - In-Play tab on module selector ribbon
        DESCRIPTION: - Live Stream tab on module selector ribbon
        DESCRIPTION: - Tomorrow/Future/In-Ply tabs on sport page
        EXPECTED: 
        """
        pass

    def test_010_go_back_to_cms_and_go_to_the_sport_where_primary_market_is_a_2_way_market_eg_tennis_american_football_etc(self):
        """
        DESCRIPTION: Go back to CMS and go to the sport where primary market is a 2-way market (e.g. Tennis, American Football etc.)
        EXPECTED: Page is loaded
        """
        pass

    def test_011_check_the_template_type_1_field(self):
        """
        DESCRIPTION: Check the 'Template Type 1' field
        EXPECTED: Two options are shown:
        EXPECTED: - Win Draw Win
        EXPECTED: - One Two Type
        EXPECTED: 'One Two Type' is displayed by default
        """
        pass

    def test_012_change_the_template_from_one_two_type_to_home_draw_away_and_save_changes(self):
        """
        DESCRIPTION: Change the template from 'One Two Type' to 'Home Draw Away' and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_013_load_oxygen_and_check_fixtyre_header_on_the_followign_tabs__sport_pages_today_tomorrow_future_in_play__in_play_page__in_play_tab_on_module_selector_ribbon__live_stream_tab_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Load Oxygen and check fixtyre header on the followign tabs:
        DESCRIPTION: - Sport pages (Today, Tomorrow, Future, In-Play)
        DESCRIPTION: - In-Play page
        DESCRIPTION: - In-Play tab on module selector ribbon
        DESCRIPTION: - Live Stream tab on module selector ribbon
        EXPECTED: 'Home Draw Away' fixture header is shown
        EXPECTED: - Home selection is shown under 'Home' column
        EXPECTED: - Away selection is shown under 'Away' column
        EXPECTED: - Draw selection is empty????'
        EXPECTED: NOTE, bear in mind American types of sport (the ordering of home/away selection)
        """
        pass

    def test_014_repeat_step_8(self):
        """
        DESCRIPTION: Repeat step #8
        EXPECTED: 2-Way primary market is displayed
        EXPECTED: Changes are not applied on event details page
        """
        pass
