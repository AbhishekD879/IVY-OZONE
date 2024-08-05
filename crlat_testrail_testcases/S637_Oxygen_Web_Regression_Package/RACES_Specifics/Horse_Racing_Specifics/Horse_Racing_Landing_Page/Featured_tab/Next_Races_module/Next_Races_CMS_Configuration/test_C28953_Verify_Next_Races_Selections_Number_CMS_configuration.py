import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28953_Verify_Next_Races_Selections_Number_CMS_configuration(Common):
    """
    TR_ID: C28953
    NAME: Verify 'Next Races' Selections Number CMS configuration
    DESCRIPTION: This test case verifies Selections number configuration in CMS within Next Races
    DESCRIPTION: Story Tickets:
    DESCRIPTION: **BMA-6572 **CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 1. In order to get a list of **Next Races** events and check **typeId**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_type_in_search_field_nextraces(self):
        """
        DESCRIPTION: Type in search field 'NEXTRACES'
        EXPECTED: NEXTRACES section is shown
        """
        pass

    def test_004_in_number_of_selections_enter_some_number___press_submit3_option_should_be_set_by_default(self):
        """
        DESCRIPTION: In '**Number of Selections**' enter some number -> Press 'Submit'
        DESCRIPTION: ('3' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: 
        """
        pass

    def test_006_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: *   <Horse Racing> landing page is opened
        EXPECTED: *   'Next Races' module is displayed
        """
        pass

    def test_007_verify_next_races_selections_number(self):
        """
        DESCRIPTION: Verify 'Next Races' Selections number
        EXPECTED: *   Appropriate number of selections (which was set in CMS) is displayed within Next Races module
        EXPECTED: *   If number of selections is less than was set in CMS -> display the remaining selections
        """
        pass

    def test_008_go_to_cms___in_number_of_selections_enter_some_other_number___press_submit3_option_should_be_set_by_default(self):
        """
        DESCRIPTION: Go to CMS -> In '**Number of Selections**' enter some other number -> Press 'Submit'
        DESCRIPTION: ('3' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED: 
        """
        pass
