import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

import { OddsBoostBetslipHeaderComponent } from './odds-boost-betslip-header.component';

describe('OddsBoostBetslipHeaderComponent', () => {
  let component;
  let oddsBoostService;
  let pubSubService;
  let overAskService;

  beforeEach(() => {
    oddsBoostService = {
      isOddsBoostBetslipHeaderAvailable: jasmine.createSpy('isOddsBoostBetslipHeaderAvailable').and.returnValue(true),
      showInfoDialog: jasmine.createSpy('showInfoDialog'),
      showOddsBoostSpDialog: jasmine.createSpy('showOddsBoostSpDialog'),
      canBoostSelections: jasmine.createSpy('canBoostSelections'),
      showOddsBoostFreeBetDialog: jasmine.createSpy('showOddsBoostFreeBetDialog'),
      sendGTM: jasmine.createSpy('sendGTM'),
      hasSelectionsWithFreeBet: jasmine.createSpy('hasSelectionsWithFreeBet').and.returnValue(false),
      isBoostActive: jasmine.createSpy('isBoostActive').and.returnValue(true),
      sendEventToGTM: jasmine.createSpy('sendEventToGTM'),
      getBoostActiveFromStorage: jasmine.createSpy('getBoostActiveFromStorage').and.returnValue(true)
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb(true)),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };

    overAskService = {};

    component = new OddsBoostBetslipHeaderComponent(
      oddsBoostService,
      pubSubService,
      overAskService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.active).toBeTruthy();
    expect(component.reboost).toBeTruthy();
    expect(oddsBoostService.getBoostActiveFromStorage).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OddsBoostBetslipHeaderComponent', 'ODDS_BOOST_CHANGE', jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OddsBoostBetslipHeaderComponent', 'ODDS_BOOST_REBOOST', jasmine.any(Function)
    );
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('OddsBoostBetslipHeaderComponent');
  });

  it('onBoostClick', () => {
    oddsBoostService.canBoostSelections.and.returnValue(true);
    component.active = true;
    component.onBoostClick();

    expect(oddsBoostService.canBoostSelections).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith(
      'ODDS_BOOST_CHANGE', jasmine.any(Boolean)
    );
    expect(oddsBoostService.sendEventToGTM).toHaveBeenCalledWith('betslip', false);
  });

  it('onBoostClick (freebet dialog)', () => {
    oddsBoostService.hasSelectionsWithFreeBet.and.returnValue(true);
    component.active = false;

    component.onBoostClick();

    expect(oddsBoostService.showOddsBoostFreeBetDialog).toHaveBeenCalledWith(false, 'betslip');
  });

  it('onBoostClick (reboost)', () => {
    component.reboost = true;

    component.onBoostClick();

    expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubApi.BETSLIP_UPDATED);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.ODDS_BOOST_REBOOST_CLICK);
    expect(oddsBoostService.sendEventToGTM).toHaveBeenCalledWith('betslip', true);
  });

  it('onBoostClick (sp dialog)', () => {
    oddsBoostService.canBoostSelections.and.returnValue(false);

    component.onBoostClick();

    expect(oddsBoostService.canBoostSelections).toHaveBeenCalled();
    expect(pubSubService.publish).not.toHaveBeenCalled();
    expect(oddsBoostService.showOddsBoostSpDialog).toHaveBeenCalled();
  });

  it('isAvailable', () => {
    expect(component.isAvailable).toBeTruthy();
    expect(oddsBoostService.isOddsBoostBetslipHeaderAvailable).toHaveBeenCalled();
  });

  it('boostDisabled', () => {
    component.boostDisabled = true;
    component.onBoostClick();
    expect(oddsBoostService.hasSelectionsWithFreeBet).not.toHaveBeenCalled();
  });

  it('showInfoDialog', () => {
    component.showInfoDialog();
    expect(oddsBoostService.showInfoDialog).toHaveBeenCalled();
  });
});
