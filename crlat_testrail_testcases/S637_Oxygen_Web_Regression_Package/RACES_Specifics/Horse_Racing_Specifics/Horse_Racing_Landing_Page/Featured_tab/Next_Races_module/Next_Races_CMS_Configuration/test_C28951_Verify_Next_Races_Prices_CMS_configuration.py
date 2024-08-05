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
class Test_C28951_Verify_Next_Races_Prices_CMS_configuration(Common):
    """
    TR_ID: C28951
    NAME: Verify 'Next Races' Prices CMS configuration
    DESCRIPTION: This test case verifies Next Races Events with prices configuration in CMS
    DESCRIPTION: Story Tickets:
    DESCRIPTION: **BMA-6572 **CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 1. In order to get a list of **Next Races** events and check **priceTypeCodes**
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

    def test_003_expand_nextraces_section(self):
        """
        DESCRIPTION: Expand 'NEXTRACES' section
        EXPECTED: NEXTRACES section expanded
        """
        pass

    def test_004_in_show_prices_only_field_set_yes_option___press_submityes_option_should_be_set_by_default(self):
        """
        DESCRIPTION: In '**Show prices only**' field set 'Yes' option -> Press 'Submit'
        DESCRIPTION: ('Yes' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_006_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: *   <Horse Racing> landing page is opened
        EXPECTED: *   'Next 4 Races' module is displayed
        """
        pass

    def test_007_verify_next_races_price_type(self):
        """
        DESCRIPTION: Verify 'Next Races' price type
        EXPECTED: *   Only 'LP' prices/odd buttons are displayed  in Next Races widget
        EXPECTED: *   Events with **'priceTypeCode'**='SP, LP, ' and **'priceTypeCodes'** = 'LP, ' are present in Next Races
        """
        pass

    def test_008_go_to_cms__in_show_prices_only_field_set_no_option___press_submit(self):
        """
        DESCRIPTION: Go to CMS -> In '**Show prices only**' field set 'No' option -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_009_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps #5-6
        EXPECTED: 
        """
        pass

    def test_010_verifynext_races_price_type(self):
        """
        DESCRIPTION: Verify** **'Next Races' price type
        EXPECTED: *   Both 'LP' and 'SP' prices/odd buttons are displayed in Next Races widget
        EXPECTED: *   Events with **'priceTypeCode'**='SP, LP, ', **'priceTypeCodes'** = 'SP' and **'priceTypeCodes'** = 'LP, ' are present in Next Races
        EXPECTED: *   LP pricetype is displayed over SP if both are available
        """
        pass
