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
class Test_C9608211_Verify_Leagues_Types_ordering_in_Tennis_Competitions_tab_if_more_than_one_class_is_set_in_CMS(Common):
    """
    TR_ID: C9608211
    NAME: Verify Leagues (Types) ordering in Tennis 'Competitions' tab if more than one class is set in CMS
    DESCRIPTION: This test case verifies the Leagues (Types) ordering in Tennis 'Competitions' tab if more than one class is set in CMS
    DESCRIPTION: NOTE: Steps 6 and 7 are invalid, since such changes have been reverted.
    PRECONDITIONS: 0. 'CompetitionsTennis' config should have 'Initial' checkbox being checked in CMS -> 'System Configuration' -> 'Config'
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Leagues (Types) Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: 4. Make sure that at least 2 different Tennis classes with at least one active type and event within them are present in TI
    PRECONDITIONS: 5. 'CompetitionsTennis' field in CMS -> Structure contains a list class IDs from step 4(separated by comma).
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set at least 2 classes in CMS navigate to 'System-configuration' -> 'Competitions Tennis' and put class ID's in 'InitialClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 5. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 6. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_002_verify_leagues_types_ordering_that_belong_to_different_classes(self):
        """
        DESCRIPTION: Verify Leagues (Types) ordering that belong to different classes
        EXPECTED: * Leagues (Types) ordering based on class ordering set in CMS
        EXPECTED: * Leagues (Types) from the class set as first in CMS are displayed in the top of the list
        EXPECTED: (InitialClassIDs field in CMS)
        """
        pass

    def test_003_verify_leagues_types_ordering_that_belong_to_one_class(self):
        """
        DESCRIPTION: Verify Leagues (Types) ordering that belong to one class
        EXPECTED: Leagues (Types) are ordered by OpenBet display order (starting with lowest one)
        """
        pass

    def test_004_in_cms___structure___competitionstennis_change_the_order_of_class_ids_and_save_changes(self):
        """
        DESCRIPTION: In CMS -> Structure -> 'CompetitionsTennis', change the order of class ids and save changes.
        EXPECTED: Changes are successfully saved.
        EXPECTED: Message indicates that changes are saved.
        """
        pass

    def test_005_refresh_the_competitions_page_and_verify_that_leagues_types_ordering_changed(self):
        """
        DESCRIPTION: Refresh the competitions page, and verify that Leagues (Types) ordering changed
        EXPECTED: * Leagues (Types) ordering based on class ordering set in CMS
        EXPECTED: * Leagues (Types) from the class set as first in CMS are displayed in the top of the list
        EXPECTED: (InitialClassIDs field in CMS)
        """
        pass

    def test_006_in_cms___config___competitionstennis_disable_theuncheck_checkbox_for_initial_option_and_save_changes(self):
        """
        DESCRIPTION: In CMS -> Config -> 'CompetitionsTennis', disable the(uncheck checkbox for) 'Initial' option and save changes.
        EXPECTED: Changes are successfully saved.
        EXPECTED: Message indicates that changes are saved.
        """
        pass

    def test_007_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps 4-5
        EXPECTED: E.R. match those from steps 4 and 5.
        """
        pass
