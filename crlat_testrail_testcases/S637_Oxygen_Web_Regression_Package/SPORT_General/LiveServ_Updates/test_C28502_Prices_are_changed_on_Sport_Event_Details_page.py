import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28502_Prices_are_changed_on_Sport_Event_Details_page(Common):
    """
    TR_ID: C28502
    NAME: Prices are changed on <Sport> Event Details page
    DESCRIPTION: Note: colours flashing is not automated
    DESCRIPTION: AUTOTEST C2469306
    PRECONDITIONS: **Updates are received via push notifications**
    """
    keep_browser_open = True

    def test_001_open_sport_event_details_page(self):
        """
        DESCRIPTION: Open <Sport> Event Details page
        EXPECTED: 
        """
        pass

    def test_002_trigger_price_change_for_a_few_selections_from_different_markets_one_by_one(self):
        """
        DESCRIPTION: Trigger price change for a few selections from different markets (one by one)
        EXPECTED: Corresponding 'Price/Odds' buttons should immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: - blue colour if price has decreased
        EXPECTED: - red colour if price has increased
        """
        pass

    def test_003_trigger_price_change_for_a_few_selections_from_combined_market_eg_over_under_total_goals_correct_score_etc(self):
        """
        DESCRIPTION: Trigger price change for a few selections from combined market (e.g. Over Under Total Goals, Correct Score, etc)
        EXPECTED: Corresponding 'Price/Odds' buttons should immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: - blue colour if price has decreased
        EXPECTED: - red colour if price has increased
        """
        pass

    def test_004_trigger_prices_changes_for_markets_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Trigger prices changes for markets sections in a collapsed state
        EXPECTED: If market section is collapsed and price was changed, after expanding the section - updated price will be shown there
        """
        pass

    def test_005_trigger_prices_changes_for_not_opened_markets_collection_tabs_within_one_event(self):
        """
        DESCRIPTION: Trigger prices changes for not opened markets collection tabs within one event
        EXPECTED: If tab with markets is not opened and price was changed, after navigating to the tab - updated price will be shown there
        """
        pass
