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
class Test_C721279_Displaying_of_yourcall_or_BYB_icons_on_Sport_landing_page(Common):
    """
    TR_ID: C721279
    NAME: Displaying of yourcall or BYB icons on <Sport> landing page
    DESCRIPTION: This test case verifies logic of displaying of #yourcall or +B (BuildYourBet for Football only) icons on Sport Landing pages **for Coral only**
    PRECONDITIONS: * Pre-match sport events with different start times of leagues with and without DS/Banach events available are created in OpenBet
    PRECONDITIONS: * In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableIcon' is checked
    PRECONDITIONS: * YourCall and/or Banach leagues leagues (competitions) are added and turned on in YourCall page in CMS https://invictus.coral.co.uk/keystone/yc-leagues
    PRECONDITIONS: * leagues.json response from Digital Sports (DS) returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * buildyourbet leagues response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: * Coral app is loaded
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    """
    keep_browser_open = True

    def test_001_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to Sport landing page
        EXPECTED: 'Matches/Events/Fights' -> 'TODAY' page is opened by default (for desktop)
        EXPECTED: 'Matches/Events/Fights' page is opened by default (for mobile)
        """
        pass

    def test_002_observe_section_headeraccordion_of_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that is added and enabled in CMS and is returned from DS
        EXPECTED: - '#' (yourcall icon) is displayed on the right of module accordion/header
        EXPECTED: - in case cash out icon is displayed, yourcall icon is displayed before it
        EXPECTED: - 'Build your bet' icon is not present on League level, only on event card
        """
        pass

    def test_003_observe_section_headeraccordion_of_league_competition_that_is_added_and_enabled_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that is added and enabled in CMS and is NOT returned from DS
        EXPECTED: - '#' (yourcall icon) is NOT displayed
        """
        pass

    def test_004_observe_section_headeraccordion_of_league_competition_that_is_not_added_in_cms_and_is_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that is NOT added in CMS and is returned from DS
        EXPECTED: - '#' (yourcall icon) is NOT displayed
        """
        pass

    def test_005_observe_section_headeraccordion_of_league_competition_that_is_not_added_in_cms_and_is_not_returned_from_ds(self):
        """
        DESCRIPTION: Observe section header/accordion of league (competition), that is NOT added in CMS and is NOT returned from DS
        EXPECTED: - '#' (yourcall icon) is NOT displayed
        """
        pass

    def test_006_navigate_to_cms_and_disable_any_league_competition_that_is_returned_from_ds(self):
        """
        DESCRIPTION: Navigate to CMS and disable any league (competition), that is returned from DS
        EXPECTED: 
        """
        pass

    def test_007__navigate_back_to_matcheseventsfights___today_tab_for_desktop_navigate_back_to_matcheseventsfightsfor_mobile_refresh_page_observe_section_headeraccordion_of_league_competition_that_is_added_and_disabled_in_cms(self):
        """
        DESCRIPTION: * Navigate back to 'Matches/Events/Fights' -> 'TODAY' tab (for desktop)
        DESCRIPTION: * Navigate back to 'Matches/Events/Fights'(for mobile)
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe section header/accordion of league (competition), that is added and disabled in CMS
        EXPECTED: - '#' (yourcall icon) is NOT displayed
        """
        pass

    def test_008_navigate_to_cms_and_uncheck_enableicon_checkbox_in_system_configuration___yourcalliconsandtabs(self):
        """
        DESCRIPTION: Navigate to CMS and uncheck 'enableIcon' checkbox in System-configuration -> YOURCALLICONSANDTABS
        EXPECTED: 
        """
        pass

    def test_009__navigate_back_to_matcheseventsfights___today_tab_for_desktop_navigate_back_to_matcheseventsfights_for_mobile_refresh_page_observe_section_headeraccordion_of_league_competition_that_is_added_and_enabled_in_cms(self):
        """
        DESCRIPTION: * Navigate back to 'Matches/Events/Fights' -> 'TODAY' tab (for desktop)
        DESCRIPTION: * Navigate back to 'Matches/Events/Fights' (for mobile)
        DESCRIPTION: * Refresh page
        DESCRIPTION: * Observe section header/accordion of league (competition), that is added and enabled in CMS
        EXPECTED: '#' (yourcall icon) is NOT displayed
        """
        pass

    def test_010_football_only_repeat_steps_2_11_for_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_banach(self):
        """
        DESCRIPTION: Football only: Repeat Steps 2-11 for league (competition), that is added and enabled in CMS and is returned from Banach
        EXPECTED: Results are the same as in same steps above
        """
        pass

    def test_011_football_only_observe_section_headeraccrodion_of_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_both_ds_and_banach_example_premier_league_etc(self):
        """
        DESCRIPTION: Football only: Observe section header/accrodion of league (competition), that is added and enabled in CMS and is returned from both DS and Banach (Example: Premier League etc)
        EXPECTED: '+B' icon (BYB) is not displayed on league level, only in event card for appropriate competition and only ONCE.
        """
        pass
