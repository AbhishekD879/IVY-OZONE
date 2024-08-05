import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870382__Verify_that_Info_text_is_displayed_font_color_is_grey_when_hoover_are_underlined_and_clickable_navigating_user_to_the_correct_links_that_opens_in_another_window_Gibraltar_Gambling_Commissioner_https_(Common):
    """
    TR_ID: C44870382
    NAME: " Verify that Info text is displayed, font color is grey, when hoover are underlined and clickable, navigating user to the correct links that opens in another window.:  Gibraltar Gambling Commissioner https:/
    DESCRIPTION: " Verify that Info text is displayed, font color is Grey, when hoover are underlined and clickable, navigating user to the correct links that opens in another window.:
    DESCRIPTION: Gibraltar Gambling Commissioner https://www.gibraltar.gov.gi/finance-gaming-and-regulations/remote-gambling
    DESCRIPTION: British Gambling Commission: https://secure.gamblingcommission.gov.uk/PublicRegister/Search/Detail/54743
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is opened
        """
        pass

    def test_002_navigate_to_the_bottom_of_the_page_and_look_for_british_gambling_commission__gibraltar_gambiling_commission_links(self):
        """
        DESCRIPTION: Navigate to the bottom of the page and look for 'British Gambling Commission' & 'Gibraltar Gambiling Commission' links.
        EXPECTED: 'British Gambling Commission' & 'Gibraltar Gambiling Commission' links are available.
        """
        pass

    def test_003_verify_that_info_text_is_displayed_font_colour_is_grey_is_underlined_and_clickable_navigating_user_to_the_correct_links_that_opens_in_another_windowgibraltar_gambling_commissioner_httpswwwgibraltargovgifinance_gaming_and_regulationsremote_gamblingbritish_gambling_commission_httpssecuregamblingcommissiongovukpublicregistersearchdetail54743coral_is_operated_by_lc_international_limited_suite_6_atlantic_suites_gibraltar_and_licensed_ref_54743_and_regulated_by_the_british_gambling_commission_for_persons_gambling_in_great_britain_for_persons_gambling_outside_great_britain_ladbrokes_is_licensed_ref_010_012_by_the_government_of_gibraltar_and_regulated_by_the_gibraltar_gambling_commissioner(self):
        """
        DESCRIPTION: Verify that Info text is displayed, font colour is Grey, is underlined and clickable, navigating user to the correct links that opens in another window.:
        DESCRIPTION: Gibraltar Gambling Commissioner https://www.gibraltar.gov.gi/finance-gaming-and-regulations/remote-gambling
        DESCRIPTION: British Gambling Commission: https://secure.gamblingcommission.gov.uk/PublicRegister/Search/Detail/54743
        DESCRIPTION: Coral is operated by LC International Limited (Suite 6, Atlantic Suites, Gibraltar) and licensed (ref 54743) and regulated by the British Gambling Commission for persons gambling in Great Britain. For persons gambling outside Great Britain, Ladbrokes is licensed (ref 010, 012) by the Government of Gibraltar and regulated by the Gibraltar Gambling Commissioner.
        EXPECTED: When clicked on (ref 54743), the user is navigated to
        EXPECTED: Gambling Commission: https://secure.gamblingcommission.gov.uk/PublicRegister/Search/Detail/54743
        EXPECTED: When clicked on (ref 010, 012), the user is navigated to
        EXPECTED: Gibraltar Gambling Commissioner https://www.gibraltar.gov.gi/finance-gaming-and-regulations/remote-gambling
        """
        pass
