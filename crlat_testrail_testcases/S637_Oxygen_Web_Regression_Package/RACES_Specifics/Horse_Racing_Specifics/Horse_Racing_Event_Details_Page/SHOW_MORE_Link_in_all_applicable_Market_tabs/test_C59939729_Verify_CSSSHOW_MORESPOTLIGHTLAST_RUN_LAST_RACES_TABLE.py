import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59939729_Verify_CSSSHOW_MORESPOTLIGHTLAST_RUN_LAST_RACES_TABLE(Common):
    """
    TR_ID: C59939729
    NAME: Verify CSS:"SHOW MORE",SPOTLIGHT,LAST RUN, LAST RACES TABLE
    DESCRIPTION: Verify the CSS for  "LAST RUN" and Last 5 races information in table
    PRECONDITIONS: 1: Racing Post Verdict should be available for the event
    PRECONDITIONS: 2: SPOTLIGHT and Last Race information should be available for the Horses
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_any_horse_race_event_from_uk__irish_races(self):
        """
        DESCRIPTION: Click on any Horse race event from UK / Irish races
        EXPECTED: User should be navigated to Event details page
        """
        pass

    def test_004_scroll_to_the_selections_horses_and_click_on_show_more_link(self):
        """
        DESCRIPTION: Scroll to the Selections (Horses) and click on "SHOW MORE" link
        EXPECTED: The following information should be displayed
        EXPECTED: 1: SPOTLIGHT
        EXPECTED: 2: LAST RUN
        EXPECTED: "SHOW MORE" text should be replaced with "SHOW LESS" in the expanded view
        """
        pass

    def test_005_verify_the_css_for_the_last_run_label_and_text(self):
        """
        DESCRIPTION: Verify the CSS for the Last Run label and text
        EXPECTED: The last run lable css should be:
        EXPECTED: .LAST-RUN {
        EXPECTED: width: 64px;
        EXPECTED: height: 19px;
        EXPECTED: font-family: HelveticaNeue;
        EXPECTED: font-size: 11px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: -0.27px;
        EXPECTED: color: #2b2b2b;
        EXPECTED: and the text CSS should be:
        EXPECTED: .-\39 -7-Chased-le {
        EXPECTED: width: 351px;
        EXPECTED: height: 42px;
        EXPECTED: font-family: Helvetica;
        EXPECTED: font-size: 12px;
        EXPECTED: font-weight: normal;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: -0.29px;
        EXPECTED: color: #2b2b2b;
        EXPECTED: }
        """
        pass

    def test_006_verifies_the_css_for_the_last_races_table(self):
        """
        DESCRIPTION: Verifies the CSS for the Last races table
        EXPECTED: As per the Design
        """
        pass
