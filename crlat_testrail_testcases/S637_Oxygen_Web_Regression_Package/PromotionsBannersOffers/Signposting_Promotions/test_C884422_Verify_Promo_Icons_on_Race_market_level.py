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
class Test_C884422_Verify_Promo_Icons_on_Race_market_level(Common):
    """
    TR_ID: C884422
    NAME: Verify Promo Icons on <Race> market level
    DESCRIPTION: This test case verifies promo icons on <Race> event detail pages for the following promotions:
    DESCRIPTION: * Faller’s Insurance (available only for Horse Racing)
    DESCRIPTION: * Beaten by a Length (available for Horse Racing and Greyhounds) - not implemented for Ladbrokes
    DESCRIPTION: * Extra Place Race (available only for Horse Racing)
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: * There have to be <Race> events with each promotion from the list:
    PRECONDITIONS: * Faller’s Insurance (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Beaten by a Length (available for Horse Racing **AND** Greyhounds) - not implemented for Ladbrokes
    PRECONDITIONS: * Extra Place Race (available **ONLY** for Horse Racing)
    PRECONDITIONS: * Make sure that there are promotion created in CMS and linked to active signposting promotions (by Market Flags)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * Information about promotions, available for the event, is received in <drilldownTagNames> attribute in SiteServer response for the event
    PRECONDITIONS: **Parameters:**
    PRECONDITIONS: * **MKTFLAG_FI** - Faller's Insurance
    PRECONDITIONS: * **MKTFLAG_BBAL** - Beaten by a Length - not implemented for Ladbrokes
    PRECONDITIONS: * **MKTFLAG_EPR**  - Extra Place Race
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    PRECONDITIONS: For **Ladbrokes**: "Faller’s Insurance" and "Beaten by a Length" promotions should be turned off in CMS (Promotions)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_race_edp_page_with_fallers_insurance_promotion_available(self):
        """
        DESCRIPTION: Navigate to the <Race> EDP Page with **Faller’s Insurance** promotion available
        EXPECTED: * Promo icon is shown on the same level as 'Each Way: 1/4 Odds - Places 1-2-3-4' (for ex.) placed on the right
        EXPECTED: * Promo icon is shown after CashOut icon (if available)
        EXPECTED: * Promo icon is shown before BPG icon (if BPG is available for current event)
        """
        pass

    def test_002_tap_on_the_fallers_insurance_promo_icon(self):
        """
        DESCRIPTION: Tap on the Faller’s Insurance promo icon
        EXPECTED: Promo pop-up is shown after tapping the icon
        """
        pass

    def test_003_repeat_this_test_case_for_a_race_event_for_which_2_promo_icons_are_available_at_the_same_time(self):
        """
        DESCRIPTION: Repeat this test case for a <Race> event, for which 2 promo icons are available at the same time
        EXPECTED: * Two icons are shown next to each other
        EXPECTED: * Corresponding promo pop up is shown after tapping on each icon
        """
        pass

    def test_004_repeat_steps_1_3_for_fallers_insurance_promo_on_hr_beaten_by_a_length_promo_on_hr_beaten_by_a_length_promo_on_greyhounds_extra_place_race_promo_on_hr(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: * **Faller’s Insurance** promo on **HR**
        DESCRIPTION: * **Beaten by a Length** promo on **HR**
        DESCRIPTION: * **Beaten by a Length** promo on **Greyhounds**
        DESCRIPTION: * **Extra Place Race** promo on **HR**
        EXPECTED: Icons are placed on same areas as described above
        """
        pass
