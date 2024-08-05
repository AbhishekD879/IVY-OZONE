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
class Test_C713686_Verify_B_icon_is_not_displayed_on_Football_Competitions(Common):
    """
    TR_ID: C713686
    NAME: Verify '+B' icon is not displayed on Football Competitions
    DESCRIPTION: This test case verifies logic of displaying of +B icons (BuildYourBet) on Сompetitions tab on Football page
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues (competitions) are added and turned on in YourCall page in CMS
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS and/or
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded and Сompetitions tab on Football page is opened
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    """
    keep_browser_open = True

    def test_001_within_expanded_class_accordions_observe_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Within expanded class accordions observe league (competition), that is added and enabled in CMS and is returned from DS
        EXPECTED: * '+B' icon is NOT displayed for appropriate competition on the right
        EXPECTED: * BYB icon is not present on type level only on event level (event card)
        EXPECTED: ![](index.php?/attachments/get/110996876)
        """
        pass

    def test_002_click_on_any_league_competition(self):
        """
        DESCRIPTION: Click on any league (competition)
        EXPECTED: 
        """
        pass

    def test_003_click_change_competition(self):
        """
        DESCRIPTION: Click 'Change Competition'
        EXPECTED: 
        """
        pass

    def test_004_select_a_competition_groupclass_from_the_list_that_contain_league_competition_from_step_1(self):
        """
        DESCRIPTION: Select a competition group(class) from the list that contain league (competition) from step #1
        EXPECTED: * List of leagues (competitions) within this group are shown
        EXPECTED: * '+B' icon is displayed for appropriate competition on the right
        EXPECTED: ![](index.php?/attachments/get/110996877)
        """
        pass

    def test_005_repeat_steps_1_4_for_league_competition_that_is_added_and_enabled_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Repeat steps #1-4 for league (competition), that is added and enabled in CMS and is NOT returned from DS
        EXPECTED: '+B' icon is NOT displayed
        """
        pass

    def test_006_repeat_steps_1_4_for_league_competition_that_is_not_added_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Repeat steps #1-4 for league (competition), that is NOT added in CMS and is returned from DS
        EXPECTED: '+B' icon is NOT displayed
        """
        pass

    def test_007_repeat_steps_1_4_for_league_competition_that_is_not_added_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Repeat steps #1-4 for league (competition), that is NOT added in CMS and is NOT returned from DS
        EXPECTED: '+B' icon is NOT displayed
        """
        pass

    def test_008_navigate_to_cms_and_disable_any_league_competition_that_is_returned_from_ds(self):
        """
        DESCRIPTION: Navigate to CMS and disable any league (competition), that is returned from DS
        EXPECTED: 
        """
        pass

    def test_009__navigate_back_to_competitions_tab_refresh_page_repeat_steps_1_4_for_league_competition_that_is_added_and_disabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: * Navigate back to Competitions tab
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Repeat steps #1-4 for league (competition), that is added and disabled in CMS and is returned from DS
        EXPECTED: '+B' icon is NOT displayed
        """
        pass

    def test_010_navigate_to_cms_and_uncheck_enableicon_checkbox_in_system_configuration___yourcalliconsandtabs(self):
        """
        DESCRIPTION: Navigate to CMS and uncheck 'enableIcon' checkbox in System-configuration -> YOURCALLICONSANDTABS
        EXPECTED: 
        """
        pass

    def test_011__navigate_back_to_competitions_tab_refresh_page_repeat_steps_1_4_for_league_competition_that_is_added_and_enabled_in_cms(self):
        """
        DESCRIPTION: * Navigate back to Competitions tab
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Repeat steps #1-4 for league (competition), that is added and enabled in CMS
        EXPECTED: '+B' icon is NOT displayed
        """
        pass

    def test_012_repeat_steps_1_11_for_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_banach(self):
        """
        DESCRIPTION: Repeat Steps #1-11 for league (competition), that is added and enabled in CMS and is returned from Banach
        EXPECTED: --
        """
        pass

    def test_013_within_expanded_class_accordions_observe_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_both_ds_and_banach_example_premier_league_etc(self):
        """
        DESCRIPTION: Within expanded class accordions observe league (competition), that is added and enabled in CMS and is returned from both DS and Banach (Example: Premier League etc)
        EXPECTED: '+B' icon is NOT displayed for appropriate competition on the right.
        EXPECTED: ![](index.php?/attachments/get/110996884)
        EXPECTED: ![](index.php?/attachments/get/110996885)
        """
        pass
