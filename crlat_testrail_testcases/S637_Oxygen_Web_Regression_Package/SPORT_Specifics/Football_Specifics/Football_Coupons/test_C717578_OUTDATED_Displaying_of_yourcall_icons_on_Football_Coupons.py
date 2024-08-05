import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C717578_OUTDATED_Displaying_of_yourcall_icons_on_Football_Coupons(Common):
    """
    TR_ID: C717578
    NAME: [OUTDATED] Displaying of yourcall icons on Football Coupons
    DESCRIPTION: This test case verifies logic of displaying of +B icons (BuildYourBet) on Competition accordions on Coupon Details page
    DESCRIPTION: **OUTDATED** as yourcall icons were removed from Coupons page
    DESCRIPTION: Refer to https://jira.egalacoral.com/browse/BMA-38676
    PRECONDITIONS: * Coupon with and without YourCall and/or Banach leagues is created https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues leagues (competitions) are added and turned on in YourCall page in CMS
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS and/or
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded and Coupons tab on Football page is opened
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_navigate_to_coupon_details_page_of_coupon_from_preconditions(self):
        """
        DESCRIPTION: Navigate to Coupon Details page of coupon from preconditions
        EXPECTED: 
        """
        pass

    def test_002_observe_accordionheader_of_competition_league_that_is_added_and_enabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition (league), that is added and enabled in CMS and is returned from DS
        EXPECTED: For mobile/tablet view:
        EXPECTED: '#Yourcall' icon is displayed on the right of module accordion/header
        EXPECTED: in case cash out icon is displayed, yourcall icon is displayed before it
        EXPECTED: For desktop view:
        EXPECTED: #Yourcall icon is displayed on the right side of module accordion/header before cash out icon
        """
        pass

    def test_003_observe_accordionheader_of_competitionleague_that_is_added_and_enabled_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is added and enabled in CMS and is NOT returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        pass

    def test_004_observe_accordionheader_of_competitionleague_that_is_not_added_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is NOT added in CMS and is returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        pass

    def test_005_observe_accordionheader_of_competitionleague_that_is_not_added_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe accordion/header of competition(league), that is NOT added in CMS and is NOT returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        pass

    def test_006_navigate_to_cms_and_disable_any_competitionleague_that_is_returned_from_ds(self):
        """
        DESCRIPTION: Navigate to CMS and disable any competition(league), that is returned from DS
        EXPECTED: 
        """
        pass

    def test_007__navigate_back_to_coupon_details_page_of_coupon_from_preconditions_refresh_page_observe_accordionheader_of_competitionleague_that_is_added_and_disabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: * Navigate back to Coupon Details page of coupon from preconditions
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe accordion/header of competition(league), that is added and disabled in CMS and is returned from DS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        pass

    def test_008_navigate_to_cms_and_uncheck_enableicon_checkbox_in_system_configuration___yourcalliconsandtabs(self):
        """
        DESCRIPTION: Navigate to CMS and uncheck 'enableIcon' checkbox in System-configuration -> YOURCALLICONSANDTABS
        EXPECTED: 
        """
        pass

    def test_009__navigate_back_to_coupon_details_page_of_coupon_from_preconditions_refresh_page_observe_accordionheader_of_competitionleague_that_is_added_and_enabled_in_cms(self):
        """
        DESCRIPTION: * Navigate back to Coupon Details page of coupon from preconditions
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe accordion/header of competition(league), that is added and enabled in CMS
        EXPECTED: '#Yourcall' icon is NOT displayed
        """
        pass

    def test_010_repeat_steps_2_9_for_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_banach(self):
        """
        DESCRIPTION: Repeat Steps 2-9 for league (competition), that is added and enabled in CMS and is returned from Banach
        EXPECTED: --
        """
        pass

    def test_011_navigate_to_coupon_details_page_of_coupon_from_preconditions_and_observe_accordionheader_of_competition_league_that_is_added_and_enabled_in_cms_and_is_returned_from_both_ds_and_banach_example_premier_league_etc(self):
        """
        DESCRIPTION: Navigate to Coupon Details page of coupon from preconditions and observe accordion/header of competition (league), that is added and enabled in CMS and is returned from both DS and Banach (Example: Premier League etc)
        EXPECTED: '+B' icon (BYB) is displayed for appropriate competition on event card only ONCE.
        """
        pass
