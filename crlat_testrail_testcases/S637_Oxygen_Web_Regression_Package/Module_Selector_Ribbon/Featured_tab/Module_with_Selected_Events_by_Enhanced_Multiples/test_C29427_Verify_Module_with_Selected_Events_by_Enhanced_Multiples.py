import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29427_Verify_Module_with_Selected_Events_by_Enhanced_Multiples(Common):
    """
    TR_ID: C29427
    NAME: Verify Module with Selected Events by Enhanced Multiples
    DESCRIPTION: This test case verifies Events Retrieving by Enhanced Multiples type ID and configured module itself.
    DESCRIPTION: Note: Test Case should cover all supporting Sports (Football for now)
    DESCRIPTION: **Jira tickets:** BMA-5106
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) Go to CMS -> Featured Tab Modules -> Tap 'Create Feature Tab Module' button -> Fill in all required fields with valid data -> Go to 'Select Events by' field and select **Enhanced Multiples** -> Set valid Type ID of Enhanced Multiples -> Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
    PRECONDITIONS: **NOTE: **Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: **NOTE:** Configured event should have only one selection!!
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: Created module with Enhanced Multiples outcomes which have same TypeId is displayed:
        EXPECTED: *   Just outcomes of events with attribute **typeName="Enhanced Multiples****" **are shown
        EXPECTED: *   Just outcomes of events with **NO isStarted="true"** attribute are shown
        EXPECTED: *   **Each outcome is shown separately **(of events with more then one market and more than one outcome, of  events one market and more than one outcome, of  events with one market and one outcome)
        """
        pass

    def test_002_expandcollapse_module_and_verify_header_name_and_selection_name(self):
        """
        DESCRIPTION: Expand/Collapse Module and verify Header Name and Selection Name
        EXPECTED: *   Header name is collapsible
        EXPECTED: *   Selection name corresponds to '**name**' attribute on Outcome level OR to <name> set in CMS if name was overridden
        """
        pass

    def test_003_verify_outcome_start_time(self):
        """
        DESCRIPTION: Verify Outcome Start Time
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown below Sport icon
        EXPECTED: *   For outcomes that occur Today date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (but NOT over 24 hours) date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (over 24 hours away) date format is 'DD Month HH:MM' AM/PM
        """
        pass

    def test_004_tapanywhere_on_outcome_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Outcome section (except for price buttons)
        EXPECTED: Outcome section is not clickable
        """
        pass

    def test_005_verify_data_of_priceodds_button_for_verified_outcome_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button for verified outcome in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        pass

    def test_006_verify_data_of_priceodds_for_verified_outcome_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified outcome in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        pass

    def test_007_add_selection_to_the_betslip_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Add selection to the Betslip from Module Selector Ribbon
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_009_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_010_repeat_steps_1_7___triggerwait_until_for_verified_event_isstartedtrue_attribute_will_be_set__refresh_page(self):
        """
        DESCRIPTION: Repeat steps 1-7 -> Trigger/wait until for verified event '**isStarted="true"**' attribute will be set -> Refresh page
        EXPECTED: All outcomes of verified event are no more shown within 'Featured' tab
        """
        pass
