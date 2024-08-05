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
class Test_C1108083_Verify_Racing_Post_Silks_Form_Information_in_Next_Races_Module(Common):
    """
    TR_ID: C1108083
    NAME: Verify Racing Post Silks/Form Information in 'Next Races' Module
    DESCRIPTION: This test case is for checking of racing post silks information which are displayed in the 'Next Races' module.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: System-Configuration > AGGREGATIONMS
    PRECONDITIONS: If enabled silks will be received in https://aggregation-ms-dev.symphony-solutions.eu/racingpost response
    PRECONDITIONS: If not enabled silks will be received 'https://img.coral.co.uk/' separate files
    PRECONDITIONS: image URL's:
    PRECONDITIONS: CI-TST2: http://img-tst2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-STG: http://img-stg2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-PROD: http://img.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL&responseFormat=json&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of Next events on Horse Racing use the following link
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** on outcome level to see a horse name
    PRECONDITIONS: Check "racingFormOutcome" for the following attributes:
    PRECONDITIONS: - **'jockey'** to see a jockey information
    PRECONDITIONS: **- 'trainer' ** to see trainer name
    PRECONDITIONS: - **'silkName' **to find out a name of file to download needed silk.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: --
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: 'Horse Racing' landing page is opened
        """
        pass

    def test_003_check_site_server___find_event_which_has_racing_post_rp_silks_mapped(self):
        """
        DESCRIPTION: Check Site Server -> find event which has Racing Post (RP) silks mapped
        EXPECTED: 
        """
        pass

    def test_004_on_next_races_verify_horse_silk_icon(self):
        """
        DESCRIPTION: On 'Next Races' verify Horse Silk icon
        EXPECTED: * Horse silk icon corresponds to the image which is downloaded using Image URL's.
        EXPECTED: * The silks are cropped and aligned to the right
        EXPECTED: * Generic silk image is displayed for missed selections
        """
        pass

    def test_005_verify_horse_name(self):
        """
        DESCRIPTION: Verify Horse Name
        EXPECTED: Horse name corresponds to the **name** attribute
        """
        pass

    def test_006_verify_jockeytrainer_information(self):
        """
        DESCRIPTION: Verify jockey/trainer information
        EXPECTED: Jockey information corresponds to the **jockey** attribute
        EXPECTED: Trainer information corresponds to the **trainer** attribute
        EXPECTED: The information is shown in next format: **Jockey/Trainer**
        """
        pass

    def test_007_verify_runner_number_information(self):
        """
        DESCRIPTION: Verify runner number information
        EXPECTED: Runner number corresponds to the **runnerNumber** attribute
        """
        pass

    def test_008_verify_draw_information(self):
        """
        DESCRIPTION: Verify draw information
        EXPECTED: Draw Number is contained within brackets and corresponds to the **draw** attribute
        """
        pass

    def test_009_verify_odds(self):
        """
        DESCRIPTION: Verify odds
        EXPECTED: Price/odds buttons are displayed
        """
        pass

    def test_010_verify_selection_if_some_of_the_racing_post_info_is_absent(self):
        """
        DESCRIPTION: Verify selection if some of the racing post info is absent
        EXPECTED: If some attribute is absent -> it is just not shown in the application
        """
        pass

    def test_011_check_event_for_which_absolutely_no_silks_are_available_for_all_runners_within_a_single_race(self):
        """
        DESCRIPTION: Check event, for which absolutely NO silks are available for all runners within a single race
        EXPECTED: *  Generic silk icons are NOT displayed
        EXPECTED: *  Only runner numbers are displayed
        EXPECTED: *  Horse name corresponds to the **name** attribute
        """
        pass

    def test_012_check_event_for_which_runnernumber_attribute_is_not_available_for_allsome_runners_within_a_single_race(self):
        """
        DESCRIPTION: Check event, for which **runnerNumber** attribute is NOT available for all/some runners within a single race
        EXPECTED: * Runner numbers are NOT displayed and selection (horse) names without **runnerNumber** attribute are aligned with the other horse names
        """
        pass

    def test_013_for_mobile_and_tabletgo_to_the_homepage___tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_014_for_mobile_and_tabletrepeat_steps__3___12(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Repeat steps # 3 - 12
        EXPECTED: 
        """
        pass

    def test_015_for_desktopgo_to_the_desktop_homepage___check_next_races_section_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' section under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_016_for_desktoprepeat_steps__3___12(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 3 - 12
        EXPECTED: 
        """
        pass
