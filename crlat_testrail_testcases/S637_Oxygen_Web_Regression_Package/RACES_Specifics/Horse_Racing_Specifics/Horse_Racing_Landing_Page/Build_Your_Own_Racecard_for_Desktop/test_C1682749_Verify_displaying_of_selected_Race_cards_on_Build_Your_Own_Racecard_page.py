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
class Test_C1682749_Verify_displaying_of_selected_Race_cards_on_Build_Your_Own_Racecard_page(Common):
    """
    TR_ID: C1682749
    NAME: Verify displaying of selected Race cards on 'Build Your Own Racecard' page
    DESCRIPTION: This test case verifies displaying of selected Race cards on 'Build Your Own Racecard' page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'Horse Racing' Landing page -> 'Featured' tab
    PRECONDITIONS: 3. Click on 'Build a Racecard' button in 'Build Your Own Racecard' section that is located at the top of the main view below tabs
    PRECONDITIONS: 4. Tick at least one checkbox before 'Event off time' tab
    PRECONDITIONS: 5. Click at 'Build Your Own Racecard' button
    PRECONDITIONS: To get info about event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYY?translationLang=en&racingForm=outcome&racingForm=event
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - event ID
    """
    keep_browser_open = True

    def test_001_verify_build_your_own_racecard_page(self):
        """
        DESCRIPTION: Verify 'Build Your Own Racecard' page
        EXPECTED: * 'Build Your Own Racecard' page is opened
        EXPECTED: * Selected Race card is displayed below Market tabs
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        pass

    def test_002_verify_each_way_terms(self):
        """
        DESCRIPTION: Verify 'Each way' terms
        EXPECTED: * 'Each way' terms are displayed if **'isEachWayAvailable' = 'true'** attribute is present from SiteServer response
        EXPECTED: * 'Each way' terms are displayed above the list of selection
        EXPECTED: * 'Each way' terms are displayed in the following format:
        EXPECTED: "Each Way: x/y odds - places z,j,k"
        EXPECTED: where:
        EXPECTED: x = eachWayFactorNum
        EXPECTED: y= eachWayFactorDen
        EXPECTED: z,j,k = eachWayPlaces
        """
        pass

    def test_003_verify_class_of_race(self):
        """
        DESCRIPTION: Verify 'Class' of Race
        EXPECTED: * 'Class' of Race parameter is displayed next to 'Each way' terms/places
        EXPECTED: * 'Class' of Race value corresponds to the SS response (see attribute **'class'** within **'racingFormEvent'** section)
        """
        pass

    def test_004_verify_bpg_icon(self):
        """
        DESCRIPTION: Verify 'BPG' icon
        EXPECTED: * BPG icon is displayed in the same line as the Each-way terms (but on the right-hand side)
        EXPECTED: * BPG icon is displayed for all markets where it is available (**'isGpAvailable' = 'true'** attribute is present on market level in SS response)
        """
        pass

    def test_005_verify_cash_out_icon(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon
        EXPECTED: * 'CASH OUT' icon is displayed in the same line as 'Each way' terms from the right side (next to BPG icon if available)
        EXPECTED: * 'CASH OUT' icon is displayed if **'cashoutAvail' = 'Y'** attribute is present on Market level
        """
        pass

    def test_006_verify_promotion_icons(self):
        """
        DESCRIPTION: Verify promotion icons
        EXPECTED: * Promotion icons are available if this promotion is enabled on Market level (flag is checked for 'Faller’s Insurance', 'Beaten by a Length' or 'Extra Place Race')
        EXPECTED: * Promotion icon is shown on the same line as 'Each way' terms, on the right side, next to BPG/CashOut icons
        """
        pass

    def test_007_verify_selectionoutcome(self):
        """
        DESCRIPTION: Verify selection/outcome
        EXPECTED: Selection/outcome contains the following info:
        EXPECTED: * Correct silks are displayed for mapped selections (**'silkName'** attribute within **'racingFormEvent'** section)
        EXPECTED: * Generic silks are displayed for missed selections
        EXPECTED: * 'Runner number' and 'Draw' are correct and displayed only if not = '0' and are present in response (**'runnerNumber'**, **'draw'** attributes). 'Draw' number is shown in brackets
        EXPECTED: * Horse name (**'name'** attribute on outcome level)
        EXPECTED: * 'Jockey'/'Trainer' (**'Jockey'** and **'Trainer'** attributes)
        EXPECTED: * Form (**'formGuide'** attribute)
        """
        pass

    def test_008_click_on_downward_facing_arrow_next_to_priceodds_buttons(self):
        """
        DESCRIPTION: Click on downward facing arrow next to price/odds buttons
        EXPECTED: Horse information is expanded showing details about the runner:
        EXPECTED: * OR (**'officialRating'** attribute within **'racingFormOutcome'** section)
        EXPECTED: * Age (**'age'** attribute within the same section)
        EXPECTED: * Weight (**'weight'** attribute within the same section)
        EXPECTED: * 'Spotlight' section: information corresponds to the one in **'overview'** attribute within **'racingFormEvent'** section)
        """
        pass

    def test_009_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify 'Price/odds' buttons
        EXPECTED: * 'SP' or ‘LP’ price / odd button are displayed depending on configurations in TI tool and could be:
        EXPECTED: - SP
        EXPECTED: - LP
        EXPECTED: - SUSP
        EXPECTED: * Price / odds buttons are shown near each selection
        """
        pass

    def test_010_verify_previous_priceodds(self):
        """
        DESCRIPTION: Verify 'Previous price/odds'
        EXPECTED: * 'Previous price/odds' are displayed for LP price/odds only
        EXPECTED: * 'Previous price/odds' are displayed only after price change
        EXPECTED: * 'Previous price/odds' are displayed under 'Price/odds' button
        EXPECTED: * 'Previous price/odds' correspond to **'historicPrice'** attribute on outcome level
        """
        pass

    def test_011_verify_unnamed_favourite_selections(self):
        """
        DESCRIPTION: Verify 'Unnamed favourite' selections
        EXPECTED: * Unnamed Favourite is displayed in the end of the list
        EXPECTED: * Name corresponds to **'name'** attribute and attribute **'outcomeMeaningMinorCode'='1'** for this selection
        EXPECTED: * No associated data is displayed next to name
        """
        pass

    def test_012_verify_non_runner_selections(self):
        """
        DESCRIPTION: Verify 'Non-Runner' selections
        EXPECTED: * 'Non-Runner' is a selection which contains 'N/R' text next to it's name
        EXPECTED: * Non-Runner horses are displayed in the last positions on the racecard (above the 'UNNAMED FAVOURITE'/UNNAMED 2nd FAVOURITE' sections)
        EXPECTED: * For those selections **'outcomeStatusCode'='S'**- those selections are always suspended.
        """
        pass

    def test_013_repeat_steps_1_12_for_other_markets(self):
        """
        DESCRIPTION: Repeat steps 1-12 for other markets
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_from_preconditions_and_verify_that_build_your_own_racecard_page_is_opened_but_tick_several_checkboxes_before_event_off_time_tab(self):
        """
        DESCRIPTION: Repeat steps from preconditions and verify that 'Build Your Own Racecard' page is opened but tick several checkboxes before 'Event off time' tab
        EXPECTED: * 'Build Your Own Racecard' page is opened
        EXPECTED: * Selected Race cards are displayed
        """
        pass

    def test_015_repeat_steps_1_12(self):
        """
        DESCRIPTION: Repeat steps 1-12
        EXPECTED: 
        """
        pass
