import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C24628216_Verify_CMS_configuration_of_expanded_competition_if_0_competition_is_configured(Common):
    """
    TR_ID: C24628216
    NAME: Verify CMS configuration of expanded competition (if 0 competition is configured)
    DESCRIPTION: This test case verifies CMS configuration of expanded competition (if 0 competition is configured)
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. For reaching Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: * CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: * Default 'In Play Competitions Expanded' value is 4 and could be configured in CMS > System Config > Structure > 'In Play Competitions Expanded'
    """
    keep_browser_open = True

    def test_001_verify_the_number_of_expanded_competitions(self):
        """
        DESCRIPTION: Verify the number of expanded competitions
        EXPECTED: The number of expanded competitions accordions is taken from 'In Play Competitions Expanded' value in CMS
        """
        pass

    def test_002_in_cms_change_in_play_competitions_expanded_value_to_0_and_submit_it(self):
        """
        DESCRIPTION: In CMS change 'In Play Competitions Expanded' value to '0' and submit it
        EXPECTED: Changes are submitted successfully
        """
        pass

    def test_003_back_to_oxygen_app__in_play_page_and_verify_changes_made_in_step_2(self):
        """
        DESCRIPTION: Back to Oxygen app > 'In-Play' page and verify changes made in step 2
        EXPECTED: * All of competitions accordions within <Sport> section are collapsed
        """
        pass

    def test_004_repeat_steps_1_3_for_upcoming_events(self):
        """
        DESCRIPTION: Repeat steps 1-3 for upcoming events
        EXPECTED: All competitions accordions are collapsed
        """
        pass

    def test_005_repeat_steps_1_4_on_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 on:
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED: All competitions accordions are collapsed
        """
        pass

    def test_006_repeat_steps_1_4_on_home_page__in_play_tab_for_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-4 on:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        EXPECTED: * All competitions are not shown for each Sports accordion
        EXPECTED: * 'Show All <Sport> (n)' link is displayed for each expanded Sports accordion
        EXPECTED: where n - number of events
        """
        pass

    def test_007_click_on_show_all_sport_n_link_of_some_sport_accordion(self):
        """
        DESCRIPTION: Click on 'Show All <Sport> (n)' link of some Sport accordion
        EXPECTED: * All competitions are shown for this Sport Accordion
        """
        pass
