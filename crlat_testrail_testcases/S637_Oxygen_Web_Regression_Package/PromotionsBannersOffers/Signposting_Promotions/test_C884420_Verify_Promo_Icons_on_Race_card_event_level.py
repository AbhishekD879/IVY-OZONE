import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C884420_Verify_Promo_Icons_on_Race_card_event_level(Common):
    """
    TR_ID: C884420
    NAME: Verify Promo Icons on <Race> card event level
    DESCRIPTION: This test case verifies promo icons on <Race> odds cards for the following promotions:
    DESCRIPTION: * Faller’s Insurance (available only for Horse Racing)
    DESCRIPTION: * Extra Place Race (available only for Horse Racing)
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: * There have to be <Race> events with each promotion from the list:
    PRECONDITIONS: * Faller’s Insurance (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Extra Place Race (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Make sure that there are promotion created in CMS and linked to active signposting promotions (by Event Flags)
    PRECONDITIONS: **NOTE:** Information about promotions, available for the event, is received in <drilldownTagNames> attribute in SiteServer response for the event.
    PRECONDITIONS: In order for the icons to appear on the Race cards, they should be turned on **on the Event level**.
    PRECONDITIONS: **Parameters:**
    PRECONDITIONS: *  **EVFLAG_FIN** - Faller's Insurance
    PRECONDITIONS: *  **EVFLAG_BBL** - Beaten by a Length - not implemented for Ladbrokes
    PRECONDITIONS: *  **EVFLAG_EPR**  - Extra Place Race
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    PRECONDITIONS: For **Ladbrokes**: "Faller’s Insurance" and "Beaten by a Length" promotions should be turned off in CMS (Promotions)
    """
    keep_browser_open = True

    def test_001_verify_event_with_fallers_insurance_promotion_in_the_races_grid_on_featured_tab_on_race_landing_page(self):
        """
        DESCRIPTION: Verify event with **Faller’s Insurance** promotion in the races grid on "Featured" tab on <Race> landing page
        EXPECTED: **Coral:** Promo icon is shown next to the event start time in the races grid
        EXPECTED: **Ladbrokes:** Promo icon is not shown next to the event start time in the races grid
        """
        pass

    def test_002_tap_on_the_fallers_insurance_promo_icon(self):
        """
        DESCRIPTION: Tap on the Faller’s Insurance promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        pass

    def test_003_verify_the_event_with_fallers_insurance_promotion_on_the_next_races_module(self):
        """
        DESCRIPTION: Verify the event with **Faller’s Insurance** promotion on the "Next Races" module
        EXPECTED: * Promo icon is shown on the race card header at the right side
        EXPECTED: * In case if both cashout and a promotion are available for the event, both icons are shown
        """
        pass

    def test_004_tap_on_the_fallers_insurance_promo_icon(self):
        """
        DESCRIPTION: Tap on the Faller’s Insurance promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        pass

    def test_005_verify_the_event_with_fallers_insurance_promotion_on_featured_tab_of_the_homepage_for_module_by_race_type_id(self):
        """
        DESCRIPTION: Verify the event with **Faller’s Insurance** promotion on "Featured" tab of the Homepage:
        DESCRIPTION: * for module by Race Type ID
        EXPECTED: * Promo icon is shown on the race card at the left side
        EXPECTED: * In case if both cashout and a promotion are available for the event, both icons are properly shown
        """
        pass

    def test_006_tap_on_the_fallers_insurance_promo_icon(self):
        """
        DESCRIPTION: Tap on the **Faller’s Insurance** promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        pass

    def test_007_for_tabletdesktop_verify_the_event_with_fallers_insurance_promotion_on_next_races_widgetnot_valid_for_coral(self):
        """
        DESCRIPTION: (For tablet/desktop) Verify the event with **Faller’s Insurance** promotion on Next Races widget
        DESCRIPTION: **(Not valid for Coral?)**
        EXPECTED: * Promo icon is shown on the race card header at the right side
        EXPECTED: * In case if both cashout and a promotion are available for the event, both icons are shown
        """
        pass

    def test_008_tap_on_the_fallers_insurance_promo_icon(self):
        """
        DESCRIPTION: Tap on the **Faller’s Insurance** promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        pass

    def test_009_repeat_this_test_case_for_a_race_event_for_which_2_icons_are_available_at_the_same_time(self):
        """
        DESCRIPTION: Repeat this test case for a <Race> event, for which 2 icons are available at the same time
        EXPECTED: * In all listed locations, two icons are shown next to each other
        EXPECTED: * Corresponding promo pop up is opened after tapping on each of them
        """
        pass

    def test_010_repeat_steps_1_11_for_fallers_insurance_promo_on_hr_extra_place_race_promo_on_hr(self):
        """
        DESCRIPTION: Repeat steps 1-11 for:
        DESCRIPTION: * **Faller’s Insurance** promo on **HR**
        DESCRIPTION: * **Extra Place Race** promo on **HR**
        EXPECTED: 
        """
        pass
