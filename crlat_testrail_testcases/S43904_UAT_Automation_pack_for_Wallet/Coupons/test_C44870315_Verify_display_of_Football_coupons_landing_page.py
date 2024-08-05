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
class Test_C44870315_Verify_display_of_Football_coupons_landing_page(Common):
    """
    TR_ID: C44870315
    NAME: "Verify display of Football coupons landing page
    DESCRIPTION: "Verify display of Coupons landing page
    DESCRIPTION: -Hover over an accordion  and verify colour change
    DESCRIPTION: -Verify accordion is clickable
    DESCRIPTION: - Verify user can navigate to coupons page and user has been shown all available coupons types
    DESCRIPTION: - Verify user can navigate to selected coupon detail page
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: 'Coupons' tab is selected and highlighted
        """
        pass

    def test_004_hover_over_an_accordion__and_verify_colour_change(self):
        """
        DESCRIPTION: Hover over an accordion  and verify colour change
        EXPECTED: Accordion colour change to grey
        """
        pass

    def test_005_verify_list_of_coupons(self):
        """
        DESCRIPTION: Verify list of coupons
        EXPECTED: List of coupons are displayed
        EXPECTED: eg:* UK Coupon
        EXPECTED: *Odds on Coupon
        EXPECTED: * European Coupon
        EXPECTED: * Euro Elite Coupon
        EXPECTED: * Televised Matches
        EXPECTED: * Top Leagues Coupon
        EXPECTED: * International Coupon
        EXPECTED: * Rest of the World Coupon
        EXPECTED: * Goalscorer Coupon
        """
        pass

    def test_006__verify_events_order_in_the_accordions_and_accordion_is_clickable(self):
        """
        DESCRIPTION: -Verify events order in the accordions and accordion is clickable
        EXPECTED: Accordion expands on click and
        EXPECTED: Events are ordered in the following way:
        EXPECTED: startTime - chronological order in the first instance
        EXPECTED: Event displayOrder in ascending
        EXPECTED: Alphabetical order in ascending (in case of the same 'startTime')
        """
        pass

    def test_007_repeat_step_6_7_for_different_list_of_coupons_in_5(self):
        """
        DESCRIPTION: Repeat step #6 #7 for different list of coupons in #5
        EXPECTED: 
        """
        pass
