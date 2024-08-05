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
class Test_C9726294_Featured_verify_undisplaying_of_the_last_event_module(Common):
    """
    TR_ID: C9726294
    NAME: Featured: verify undisplaying of the last event/module
    DESCRIPTION: This test case verifies undisplaying of the last event/module
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have only 1 active module (e.g Quick Links, Highlights Carousel etc.) on in CMS > Sport Pages > Homepage with only 1 active event
    PRECONDITIONS: - You should be on a Home page > Featured tab in application
    """
    keep_browser_open = True

    def test_001___in_cms__sport_pages__homepage_deactivate_the_last_active_module__in_application_verify_displaying_of_module_on_home_page_and_response_in_console__network__ws(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage deactivate the last active module
        DESCRIPTION: - In application verify displaying of module on Home page and response in Console > Network > WS
        EXPECTED: - Module is undisplayed in application
        EXPECTED: - 'FEATURED_STRUCTURE_CHANGED' with empty array of modules is received in WS
        """
        pass

    def test_002___in_cms__sport_pages__homepage_active_the_module_again__refresh_the_page_in_application__in_cms__sport_pages__homepage__your_module_eg_quick_links_highlights_carousel_etc_deactivate_the_last_active_submodule_exact_highlights_carousel_quick_link_etc__in_application_verify_displaying_of_module_on_home_page_and_response_in_console__network__ws(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage active the module again
        DESCRIPTION: - Refresh the page in application
        DESCRIPTION: - In CMS > Sport Pages > Homepage > [Your_Module] (e.g. Quick Links, Highlights Carousel etc.) deactivate the last active submodule (exact Highlights Carousel, Quick Link etc.)
        DESCRIPTION: - In application verify displaying of module on Home page and response in Console > Network > WS
        EXPECTED: - Module is undisplayed in application
        EXPECTED: - 'FEATURED_STRUCTURE_CHANGED' with empty array of modules is received in WS
        """
        pass

    def test_003___in_cms__sport_pages__homepage__your_module_eg_quick_links_highlights_carousel_etc_activate_the_submodule_exact_highlights_carousel_surface_bet_etc__refresh_the_page_in_application__in_ti_tool_undisplay_all_the_events_in_the_displayed_module__in_application_verify_displaying_of_module_on_home_page_and_response_in_console__network__ws(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > [Your_Module] (e.g. Quick Links, Highlights Carousel etc.) activate the submodule (exact Highlights Carousel, Surface Bet etc.)
        DESCRIPTION: - Refresh the page in application
        DESCRIPTION: - In TI tool undisplay all the events in the displayed module
        DESCRIPTION: - In application verify displaying of module on Home page and response in Console > Network > WS
        EXPECTED: - Module is undisplayed in application
        EXPECTED: - 'FEATURED_STRUCTURE_CHANGED' with empty array of modules is received in WS
        """
        pass
