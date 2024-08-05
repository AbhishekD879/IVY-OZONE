import re
import pytest
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_test import vtest
import tests
import json
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
import voltron.environments.constants as vec
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.my_stable
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C66037544_Verify_the_GA_tracking_for_various_actions_performed_on_the_My_Stable_page(BaseDataLayerTest, BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C66037544
    NAME: Verify the GA tracking for various actions performed on the My Stable page.
    DESCRIPTION: This test case evaluates the various actions performed on the My Stable screen are GA tracked.
    DESCRIPTION: 1. On load of My Stable page.
    DESCRIPTION: 2. When user clicks on expand/collapse of horses in My Stable page.
    DESCRIPTION: 3. When user clicks on sort My Stable page.
    DESCRIPTION: 4. When user clicks on edit/save notes.
    DESCRIPTION: 5. When user clicks on edit stable.
    DESCRIPTION: 6. When user saves the edited stable.
    DESCRIPTION: 7. When user adds bet from My Stable.
    DESCRIPTION: 8. When user place bet from My Stable.
    DESCRIPTION: 9. When user clicks on view today races in empty stable.
    PRECONDITIONS: CMS configurations
    PRECONDITIONS: My Stable Menu item
    PRECONDITIONS: My Stable Configurations
    PRECONDITIONS: Checkbox against Active Mystable - Should be checked in
    PRECONDITIONS: Checkbox against Mystable Horses Running Today Carousel - Should be checked in
    PRECONDITIONS: Checkbox against Active Antepost - Should be checked in
    PRECONDITIONS: Checkbox against Active My Bets (Phase 2)
    PRECONDITIONS: My Stable Entry Point
    PRECONDITIONS: Entry Point SVG Icon - (Mystable-Entry-Point-White)
    PRECONDITIONS: Entry Point Label  - Ladbrokes (Stable Mates)/ Coral (My Stable)
    PRECONDITIONS: Edit Or Save My Stable
    PRECONDITIONS: Edit Stable Svg Icon - (Mystable-Entry-Point-Dark)
    PRECONDITIONS: Edit Stable Label - (Edit Stable)
    PRECONDITIONS: Save Stable Svg Icon - ( Mystable-Entry-Point-White)
    PRECONDITIONS: Save Stable Label -(Done)
    PRECONDITIONS: Edit Note Svg Icon - (Mystable-Edit-Note)
    PRECONDITIONS: Bookmark Svg Icon -(bookmarkfill)
    PRECONDITIONS: InProgress Bookmark Svg icon -(Mystable-Inprogress-Bookmark)
    PRECONDITIONS: Unbookmark Svg Icon -(bookmark)
    PRECONDITIONS: Empty My Stable
    PRECONDITIONS: Empty Stable Sag Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Empty Stable Header Label - Empty Stable
    PRECONDITIONS: Empty Stable Message Label - Tap on Edit Stable on the Race Card to add a horse
    PRECONDITIONS: Empty Stable CTA Label - View my horses
    PRECONDITIONS: My Stable Signposting
    PRECONDITIONS: Signposting Svg Icon - Mystable-Stable-Signposting
    PRECONDITIONS: Notes Signposting Svg Icon-Mystable-Note-Signposting
    PRECONDITIONS: Your Horses Running Today Carousel
    PRECONDITIONS: Carousel Icon - Mystable-Entry-Point-Dark
    PRECONDITIONS: Carousel Name - Your horses running today!
    PRECONDITIONS: Error Message Popups
    PRECONDITIONS: Maximum Horses Exceed Message - Maximum number of  selections reached. To add more, remove horses from your stable.
    """
    keep_browser_open = True
    headers = {'Content-Type': 'application/json'}
    bet_amount = 0.1
    enable_bs_performance_log = True

    def verify_GA_tracking(self, EventDetails: str, ActionEvent: str, PositionEvent: str ):
        expected_resp = {
            'event': "Event.Tracking",
            'component.ActionEvent': ActionEvent,
            'component.CategoryEvent': 'horse racing',
            'component.ContentPosition': 'not applicable',
            'component.EventDetails': EventDetails,
            'component.LabelEvent': 'my stable',
            'component.LocationEvent': 'my stable',
            'component.PositionEvent': PositionEvent,
            'component.URLClicked': 'not applicable'
        }
        wait_for_haul(10)
        actual_resp = self.get_data_layer_specific_object(object_key='event', object_value='Event.Tracking',timeout=20)
        self.compare_json_response(actual_resp, expected_resp)

    def verify_GA_tracking_after_bet_place(self, category_id, selection_id, type_id, bet_id, odds, market_name, event_name, location,
                                            belongs_inplay=0):

        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='betslip')
        event_id = actual_response[u'ecommerce'][u'purchase'][u'products'][0]['dimension60']
        self.assertTrue(re.match(r'[0-9]+', event_id),
                        msg='Event id "%s" has incorrect format.\nExpected format: "xxxxxxx"' % event_id)

        expected_response = {
            'ecommerce': {
                'purchase': {
                    'actionField': {
                        'id': bet_id + ':1',
                        'revenue': self.bet_amount
                    },
                    'products': [
                        {
                            'brand': market_name,
                            'category': str(category_id),
                            'dimension60': str(event_id),
                            'dimension61': str(selection_id),
                            'dimension62': belongs_inplay,
                            'dimension63': 0,
                            'dimension64': 'my stable',
                            'dimension65': 'my stable',
                            'dimension66': 1,
                            'dimension67': odds,
                            'dimension86': 0,
                            'dimension166': 'normal',
                            'dimension180': 'normal',
                            'dimension87': 0,
                            'dimension88': None,
                            'metric1': 0,
                            'id': bet_id,
                            'name': event_name,
                            'price': self.bet_amount,
                            'variant': int(type_id),
                            'quantity': 1
                        }
                    ]
                }
            },
            'event': 'trackEvent',
            'eventAction': 'place bet',
            'eventCategory': 'betslip',
            'eventLabel': 'success',
            'location': location
        }
        self.compare_json_response(actual_response, expected_response)

    def get_outcome_details(self):
        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            price = sports_leg.get('price')
            self.assertTrue(price, msg='No price found in placeBet request')
            price_type_ref = price.get('priceTypeRef')
            self.assertTrue(price_type_ref, msg='No priceTypeRef found in placeBet request')
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=self.headers)
        outcome_details = req['outcomeDetails']
        return outcome_details

    def test_000_preconditions(self):
        """
        DESCRIPTION: checking MY STABLE is enabled in CMS
        """
        my_stable = self.cms_config.get_my_stable_config().get('active')
        if not my_stable:
            raise CmsClientException('My stable Page is not active in CMS')
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        self.assertTrue(events, f'UK and Irish Events are unavailable')
        event_id = next((event['event']['id'] for event in events if
                                        'UK' in event['event']['typeFlagCodes'] and 'SP' not in event['event'][
                                            'typeFlagCodes']))
        self.site.login()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        self.assertTrue(self.site.horse_racing.has_my_stable_icon(expected_result=True), msg=f'My stable is not display in FE')
        self.site.horse_racing.my_stable_link.click()
        if not self.site.my_stable.has_view_todays_races():
            self.assertTrue(self.site.my_stable.edit_stable.is_displayed(),msg=f'Edit my stable link is not display in my stable page' )
            self.site.my_stable.edit_stable.click()
            race_cards = self.site.my_stable.items_as_ordered_dict
            for race_name, race in list(race_cards.items()):
                race.clear_bookmark()
        else:
            wait_for_haul(10)
            self.site.back_button.click()
        # clicking one UK & IRISH event
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        if self.device_type == 'mobile':
            if self.site.wait_for_stream_and_bet_overlay(timeout=10):
                overlay = self.site.stream_and_bet_overlay
                try:
                    if overlay and overlay.is_displayed():
                        overlay.close_button.click()
                except StaleElementReferenceException:
                    pass
            if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

        if self.device_type == 'mobile':
            if self.site.wait_for_my_stable_onboarding_overlay():
                self.site.my_stable_onboarding_overlay.close_button.click()

        self.assertTrue(self.site.racing_event_details.edit_stable.is_displayed(),
                        msg=f'edit stable link is not display in FE ')
        self.site.racing_event_details.edit_stable.click()
        outcomes = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict.get(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB).items_as_ordered_dict

        for outcome_name, outcome in list(outcomes.items())[:2]:
            if not outcome.is_bookmark_filled:
                outcome.fill_bookmark()

    def test_001_verify_ga_tracking_on_load_of_my_stable_page(self):
        """
        DESCRIPTION: Verify GA tracking On load of My Stable page.
        EXPECTED: When user loads the My Stable page this action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'contentView',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'load',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: 'my stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.racing_event_details.my_stable_link.click()
        wait_for_haul(10)
        expected_resp = {
            'event': "contentView",
            'component.ActionEvent': 'load',
            'component.CategoryEvent': 'horse racing',
            'component.ContentPosition': 'not applicable',
            'component.EventDetails': 'my stable',
            'component.LabelEvent': 'my stable',
            'component.LocationEvent': 'my stable',
            'component.PositionEvent': 'not applicable',
            'component.URLClicked': 'not applicable'
        }
        actual_resp = self.get_data_layer_specific_object(object_key='event', object_value='contentView', timeout=20)
        self.compare_json_response(actual_resp, expected_resp)

    def test_002_verify_ga_tracking_when_user_clicks_on_expandcollapse_of_horses_in_my_stable_page(self):
        """
        DESCRIPTION: Verify GA tracking when user clicks on expand/collapse of horses in My Stable page.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: '{expand/collapse}',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: '{selected horse}',//ex:shining start
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        sections = self.site.my_stable.items_as_ordered_dict
        for section_name, section in list(sections.items())[:1]:
            self.assertTrue(section.chevron_arrow.is_displayed(), msg = f'chevron arrow is not display')
            section.chevron_arrow.click()
            self.verify_GA_tracking(ActionEvent='collapse',EventDetails=section_name, PositionEvent='not applicable')
            self.assertTrue(section.chevron_arrow.is_displayed(), msg=f'chevron arrow is not display')
            section.chevron_arrow.click()
            self.verify_GA_tracking(ActionEvent='expand', EventDetails=section_name, PositionEvent='not applicable')

    def test_003_verify_ga_tracking_when_user_clicks_on_sort_my_stable_page(self):
        """
        DESCRIPTION: Verify GA tracking when user clicks on sort My Stable page.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: '{sort-recently added | sort-alphabetical}',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.assertTrue(self.site.my_stable.sort_by.is_displayed(), msg=f'Sort By drop down is not display in My Stable page')
        self.site.my_stable.sort_by.chevron.click()
        wait_for_result(lambda: self.site.my_stable.sort_by.drop_down.is_displayed())
        drop_down = self.site.my_stable.sort_by.drop_down.items_as_ordered_dict
        for selected_name, select in drop_down.items():
            select.click()
            wait_for_result(lambda: selected_name.lower() == self.site.my_stable.sort_by.selected_option.lower())
            self.assertEqual(selected_name.lower(), self.site.my_stable.sort_by.selected_option.lower(),
                                 f' sort_by drop down {selected_name.lower()} option is not selected Actual option : "{self.site.my_stable.sort_by.selected_option.lower()}"')
            self.verify_GA_tracking(EventDetails=f'sort - {selected_name.lower() if selected_name == "Recently Added" else "alphabetical"}',ActionEvent='click',
                                    PositionEvent='not applicable')
            self.site.my_stable.sort_by.chevron.click()
        self.site.my_stable.sort_by.chevron.click()

    def test_004_verify_ga_tracking_when_user_clicks_on_editsave_notes(self):
        """
        DESCRIPTION: Verify GA tracking when user clicks on edit/save notes.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'notes',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: '{selected horse-edit|selected horse-save}',//ex: 'dazzling star-edit
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.__class__.race_cards = self.site.my_stable.items_as_ordered_dict
        for race_name, race in list(self.race_cards.items())[:1]:
            self.__class__.name = race.event_name
            race.add_notes_button.click()
            race.notes.input_notes.value = 'MY NOTES'
            race.notes.save.click()
            self.verify_GA_tracking(EventDetails=f'{race_name} - save', PositionEvent='notes', ActionEvent='click')
            race.edit_notes_button.click()
            self.verify_GA_tracking(EventDetails=f'{race_name} - edit', PositionEvent='notes', ActionEvent='click')
            race.notes.cancel.click()

    def test_005_verify_ga_tracking_when_user_clicks_on_edit_stable(self):
        """
        DESCRIPTION: Verify GA tracking when user clicks on edit stable.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'my stable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: 'edit stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.assertTrue(self.site.my_stable.edit_stable.is_displayed(), msg= f'Edit stable link is not display in My stable page')
        self.site.my_stable.edit_stable.click()
        self.verify_GA_tracking(EventDetails='edit stable', ActionEvent='click', PositionEvent='my stable')

    def test_006_verify_ga_tracking_when_user_saves_the_edited_stable(self):
        """
        DESCRIPTION: Verify GA tracking when user saves the edited stable.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'my stable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: 'save stable',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.my_stable.edit_stable.click()
        self.verify_GA_tracking(EventDetails='save stable', ActionEvent='click', PositionEvent='my stable')

    def test_007_verify_ga_tracking_when_user_adds_bet_from_my_stable_add_selection_from_the_my_stable_screen_to_the_betslip(self):
        """
        DESCRIPTION: Verify GA tracking when user adds bet from My Stable. Add selection from the My Stable screen to the betslip.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: "betslip",
        EXPECTED: eventAction: "add to betslip",
        EXPECTED: eventLabel: "success",
        EXPECTED: ecommerce: {
        EXPECTED: add: {
        EXPECTED: products: [
        EXPECTED: {
        EXPECTED: dimension86: 0,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension88: null,
        EXPECTED: quantity: 1,
        EXPECTED: name: "11:27 EPSOM - THE AMATEURS&rsquo; DERBY HANDICAP STAKES",
        EXPECTED: category: "39",
        EXPECTED: variant: "126986",
        EXPECTED: brand: "WIN",
        EXPECTED: dimension60: "26347379",
        EXPECTED: dimension61: "2075879871",
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64: ,
        EXPECTED: dimension65: "my stable",
        EXPECTED: dimension177: "No show",
        EXPECTED: dimension180: "virtual"
        EXPECTED: }]
        EXPECTED: });
        """
        for self.__class__.race_name, race in list(self.race_cards.items())[:1]:
            self.assertTrue(race.has_bet_button(), msg=f'bet button is not display in race:{self.race_name}')
            race.bet_button.click()
            if self.device_type == 'mobile':
                self.site.wait_for_quick_bet_panel()
                self.site.quick_bet_panel.add_to_betslip_button.click()
                self.site.open_betslip()
            wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                               timeout=1,
                                               name='Betslip sections to load')
            wait_for_haul(15)
            outcome_details = self.get_outcome_details()
            for outcome in outcome_details:
                if self.race_name == outcome['name']:
                    self.__class__.type_id = outcome['typeId']
                    self.__class__.category_Id = outcome['categoryId']
                    self.__class__.selection_id = outcome['id']
                    self.__class__.event_name = outcome['eventDesc']
                    self.__class__.event_id = outcome['eventId']
                    self.__class__.market_name = outcome['marketDesc']
                    self.__class__.price_num = outcome['priceNum']
                    self.__class__.price_den = outcome['priceDen']
                    break
        if self.device_type == 'mobile':
            self.verify_ga_tracking_record(brand=self.market_name,
                                           category=self.category_Id,
                                           event_id=self.event_id,
                                           selection_id=self.selection_id,
                                           inplay_status=0, customer_built=0,
                                           location='my stable',
                                           stream_active=False,
                                           stream_ID=None,
                                           module='my stable',
                                           name=self.event_name,
                                           variant=self.type_id,
                                           event='trackEvent',
                                           event_action='add to betslip',
                                           event_category='quickbet',
                                           event_label='success',
                                           dimension86=0,
                                           dimension87=0,
                                           dimension88=None,
                                           dimension177="No show",
                                           dimension166="normal",
                                           dimension180="normal",
                                           metric1=0
                                           )
        else:
            self.verify_ga_tracking_record(brand=self.market_name,
                                           category=self.category_Id,
                                           event_id=self.event_id,
                                           selection_id=self.selection_id,
                                           inplay_status=0, customer_built=0,
                                           location='my stable',
                                           stream_active=False,
                                           stream_ID=None,
                                           module='my stable',
                                           name=self.event_name,
                                           variant=self.type_id,
                                           event='trackEvent',
                                           event_action='add to betslip',
                                           event_category='betslip',
                                           event_label='success',
                                           dimension86=0,
                                           dimension87=0,
                                           dimension88=None,
                                           dimension177="No show",
                                           dimension180="normal",
                                           quantity=1
                                           )

    def test_008_verify_ga_tracking_when_user_places_bet_from_my_stable(self):
        """
        DESCRIPTION: Verify GA tracking when user places bet from My Stable.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: "betslip",
        EXPECTED: eventAction: "place bet",
        EXPECTED: eventLabel: "success",
        EXPECTED: location: "/horse-racing/featured",
        EXPECTED: ecommerce: {
        EXPECTED: purchase: {
        EXPECTED: actionField: {
        EXPECTED: id: "O/24751062/0000235:1",
        EXPECTED: revenue: 1
        EXPECTED: },
        EXPECTED: products: [
        EXPECTED: {
        EXPECTED: name: "Newton Abbot",
        EXPECTED: id: "O/24751062/0000235",
        EXPECTED: price: 1,
        EXPECTED: dimension60: "26331676",
        EXPECTED: dimension61: "2074767046",
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64: ,
        EXPECTED: dimension65: "my stable",
        EXPECTED: dimension66: 1,
        EXPECTED: dimension67: 3.5,
        EXPECTED: dimension86: 0,
        EXPECTED: dimension166: "normal",
        EXPECTED: metric1: 0,
        EXPECTED: category: "21",
        EXPECTED: variant: 1956,
        EXPECTED: brand: "Win or Each Way",
        EXPECTED: quantity: 1,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension88: null
        EXPECTED: }]
        EXPECTED: });
        """
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in list(singles_section.items()):
            if self.race_name == stake_name:
                stake.amount_form.input.value = self.bet_amount
                self.get_betslip_content().bet_now_button.click()
                self.check_bet_receipt_is_displayed()
        current_url = self.device.get_current_url()
        prefix = f'https://{tests.HOSTNAME}'
        index = current_url.find(prefix)
        # Remove the prefix if found
        if index != -1:
            location = current_url[index + len(prefix):]
        bet_receipt_id = self.site.bet_receipt.bet_id
        odds_value = int(self.price_num) / int(self.price_den)
        float_num = float(odds_value) + 1
        odds_in_float = round(float_num, 2)
        if odds_in_float.is_integer():
            odds = int(odds_in_float)
        else:
            odds = odds_in_float
        self.verify_GA_tracking_after_bet_place(market_name=self.market_name,
                                                category_id=self.category_Id,
                                                selection_id=self.selection_id,
                                                bet_id=bet_receipt_id,
                                                type_id=self.type_id,
                                                belongs_inplay=0,
                                                event_name=self.name,
                                                location=location,
                                                odds=odds)
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()

    def test_009_verify_ga_tracking_when_user_clicks_on_view_today_races_in_empty_stable(self):
        """
        DESCRIPTION: Verify GA tracking when user clicks on view today races in empty stable.
        EXPECTED: This action should be GA tracked.
        EXPECTED: Open the Dev tools -&amp;gt; Console -&amp;gt; Datalayer
        EXPECTED: Evaluate the details given below:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'horse racing',
        EXPECTED: component.LabelEvent: 'my stable',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent:'my stable',
        EXPECTED: component.EventDetails: 'view today races',
        EXPECTED: component.URLClicked: 'not applicable' ,
        EXPECTED: component.ContentPosition:'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        if not self.site.my_stable.has_view_todays_races():
            self.assertTrue(self.site.my_stable.edit_stable.is_displayed(),msg=f'Edit my stable link is not display in my stable page' )
            self.site.my_stable.edit_stable.click()
            race_cards = self.site.my_stable.items_as_ordered_dict
            for race_name, race in list(race_cards.items()):
                race.clear_bookmark()
        self.assertTrue(self.site.my_stable.has_view_todays_races(), msg = f'View Todays Races are not display in My stable page')
        self.site.my_stable.view_todays_races.click()
        self.verify_GA_tracking(EventDetails='view today races',ActionEvent='click', PositionEvent='not applicable')
