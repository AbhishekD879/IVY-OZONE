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
class Test_C2987415_Highlights_Carousel__cards_displaying_based_on_suspend_option_on_selection_market_event_levels(Common):
    """
    TR_ID: C2987415
    NAME: Highlights Carousel - cards' displaying based on "suspend" option on selection/market/event levels
    DESCRIPTION: This test case verifies displaying of cards based on "suspend" option on selection/market/event levels
    DESCRIPTION: AUTOTEST [C9332784]
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_suspend_one_of_the_selection_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend one of the selection of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective selection is suspended (disabled)
        """
        pass

    def test_002___in_ti_tool_unsuspend_the_selection_from_step_1__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend the selection from step 1
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Selection is unsuspended (enabled)
        """
        pass

    def test_003___in_ti_tool_suspend_a_primary_market_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend a primary market of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are suspended (disabled)
        """
        pass

    def test_004___in_ti_tool_unsuspend_a_primary_market_from_step_3__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend a primary market from step 3
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are unsuspended (enabled)
        """
        pass

    def test_005___in_ti_tool_suspend_one_of_the_events_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool suspend one of the events displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are suspended (disabled)
        """
        pass

    def test_006___in_ti_tool_unsuspend_the_event_from_step_5__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool unsuspend the event from step 5
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: All selection from respective event's card are unsuspended (enabled)
        """
        pass
