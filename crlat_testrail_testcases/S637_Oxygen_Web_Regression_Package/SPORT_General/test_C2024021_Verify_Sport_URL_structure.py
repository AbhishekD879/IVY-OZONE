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
class Test_C2024021_Verify_Sport_URL_structure(Common):
    """
    TR_ID: C2024021
    NAME: Verify <Sport> URL structure
    DESCRIPTION: This test case verifies <Sport> URL structure
    PRECONDITIONS: * Openbet Systems: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Go to <Sport> landing page
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_003_verify_url_structure(self):
        """
        DESCRIPTION: Verify URL structure
        EXPECTED: URL structure of Event Details page is:
        EXPECTED: https://{domain}/category/{tab}
        EXPECTED: where
        EXPECTED: category - OB category name
        """
        pass

    def test_004_verify_url_structure_format(self):
        """
        DESCRIPTION: Verify URL structure format
        EXPECTED: * All text within URL is in lower case
        EXPECTED: * Space between worlds is replaced by "-" symbol
        EXPECTED: * The next specials characters "%", "-", ":" are replaced by "-" symbol
        """
        pass

    def test_005_select_matches_competitions_coupons_outrights_specialstabs_one_by_one_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Select
        DESCRIPTION: * Matches
        DESCRIPTION: * Competitions
        DESCRIPTION: * Coupons
        DESCRIPTION: * Outrights
        DESCRIPTION: * Specials
        DESCRIPTION: tabs one by one and repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_006_go_to_event_details_page_fromsport_landing_page_in_play_module_matches_module_competitions_coupons_outrights_specialshomepage_featured_tab_by_type_id_in_play_tab_streaming_tab(self):
        """
        DESCRIPTION: Go to Event Details page from:
        DESCRIPTION: <Sport> landing page
        DESCRIPTION: * In-play module
        DESCRIPTION: * Matches module
        DESCRIPTION: * Competitions
        DESCRIPTION: * Coupons
        DESCRIPTION: * Outrights
        DESCRIPTION: * Specials
        DESCRIPTION: Homepage
        DESCRIPTION: * Featured tab by Type Id
        DESCRIPTION: * In-play tab
        DESCRIPTION: * Streaming tab
        EXPECTED: Event Details page is opened
        """
        pass

    def test_007_verify_url_structure_format_on_edp_for_each_redirection_area(self):
        """
        DESCRIPTION: Verify URL structure format on EDP for each redirection area
        EXPECTED: URL structure of Event Details page is:
        EXPECTED: https://{domain}/category/class/type/event/event_id
        EXPECTED: where
        EXPECTED: category - OB category name
        EXPECTED: class - OB class name
        EXPECTED: type - OB type name
        EXPECTED: event_name - OB event name
        EXPECTED: eventID - OB event id
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_009_repeat_step_2_8_for_any_type_of_sport_that_contain_matches_events_or_fights_exclude_races(self):
        """
        DESCRIPTION: Repeat Step #2-8 for any type of <Sport> that contain matches, events or fights (exclude races)
        EXPECTED: 
        """
        pass
