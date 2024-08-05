import { QuickbetUpdateService } from './quickbet-update.service';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { ISuspendedOutcomeError } from '@betslip/models/suspended-outcome-error.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';

describe('QuickbetUpdateService', () => {
  let pubSubService;
  let fracToDecService;
  let quickbetNotificationService;
  let localeService;
  let service;
  let userService;

  const statusMock = {
    multipleWithDisableSingle: false,
    disableBet: true,
    msg: 'error'
  };

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish')
    };

    fracToDecService = {
      fracToDec: jasmine.createSpy('fracToDec'),
      getDecimal: jasmine.createSpy('getDecimal'),
      getFormattedValue: jasmine.createSpy('getFormattedValue')
    };

    localeService = {
      getString: jasmine.createSpy('getString')
    };

    quickbetNotificationService = {
      saveErrorMessage: jasmine.createSpy('saveErrorMessage'),
      clear: jasmine.createSpy('clear')
    };

    userService = {
      status: true,
      oddsFormat: 'dec'
    };

    service = new QuickbetUpdateService(
      pubSubService,
      fracToDecService,
      quickbetNotificationService,
      localeService,
      userService
    );
  });

  it('saveSelectionData', () => {
    spyOn(service, 'getUpdatedData');
    service.saveSelectionData({});
    expect(service.getUpdatedData).toHaveBeenCalled();
  });

  it('saveSelectionData: should clear messages if selection is not disabled', () => {
    spyOn(service, 'getUpdatedData');
    service.saveSelectionData({ disabled: false } as IQuickbetSelectionModel);
    expect(service.quickbetNotificationService.clear).toHaveBeenCalled();
  });

  it('saveSelectionData: should Not clear messages if selection already disabled(initial data)', () => {
    spyOn(service, 'getUpdatedData');
    service.saveSelectionData({ disabled: true } as IQuickbetSelectionModel);
    expect(service.quickbetNotificationService.clear).not.toHaveBeenCalled();
  });

  it('fillDisableMap', () => {
    service.fillDisableMap({test: 1});
    expect(service.disableMap).toEqual({test: 1});
  });

  it('@getEventSuspension, should return eventSuspension', () => {
    expect(service.getEventSuspension()).toEqual(service['eventSuspension']);
  });

  it('@getPriceChange, should return priceChange', () => {
    expect(service.getPriceChange()).toEqual(service['priceChange']);
  });

  describe('call getUpdatedData', () => {
    it('should call isDisable and applyUpdate', () => {
      const update = {
        subChannel: true
      };
      service.selection = true;
      service.applyUpdate = jasmine.createSpy('applyUpdate');
      service.isDisabled = jasmine.createSpy('isDisabled');
      pubSubService.subscribe = jasmine.createSpy().and.callFake((a, b, cb) => {
        cb && cb(null, update);
      });
      service.getUpdatedData();
      expect(service.applyUpdate).toHaveBeenCalled();
      expect(service.isDisabled).toHaveBeenCalled();
    });

    it('should not call isDisable and applyUpdate', () => {
      const update = {
        subChannel: false
      };
      service.selection = true;
      service.applyUpdate = jasmine.createSpy('applyUpdate');
      service.isDisabled = jasmine.createSpy('isDisabled');
      pubSubService.subscribe = jasmine.createSpy().and.callFake((a, b, cb) => {
        cb && cb(null, update);
      });
      service.getUpdatedData();
      expect(service.applyUpdate).not.toHaveBeenCalled();
      expect(service.isDisabled).not.toHaveBeenCalled();
    });
  });
  describe('@updateOutcomePrice', () => {
    let payload;

    beforeEach(() => {
      payload = {
        priceNum: 3,
        priceDen: 1,
        priceType: 'LP',
        isPriceChanged: true,
        priceDec: 1.1
      };
      service.selection = {
        price: {
          priceNum: 2,
          priceDen: 1,
          priceType: 'LP'
        },
        newOddsValue: 1.1,
        onStakeChange: jasmine.createSpy('onStakeChange'),
        hasSPLP: true,
        oddsSelector: [{value: 1.1}],
        isPriceChanged: true,
        isPriceUp: true,
        outcomeStatusCode: 'A'
      };
    });


    it('should not update when selection.priceDec === undefined', () => {
      service.selection.price = {
        priceNum: '3',
        priceDen: '1',
        priceType: 'LP',
        priceDec: undefined
      };

      service.updateOutcomePrice(payload);
      expect(service.fracToDecService.getDecimal).not.toHaveBeenCalled();
    });
    it('should update outcome isPriceChangeDown', () => {
      service.selection.outcomeId = '1';
      service.localeService.getString.and.returnValue('price is changed');
      service.selection.price = {
        priceNum: '4',
        priceDen: '1',
        priceType: 'LP'
      };
      service.fracToDecService.getDecimal = (n) => n;
      service.selection.isBoostActive = true;

      service.updateOutcomePrice(payload);
      expect(service.selection.price).toEqual(payload);
      expect(service.selection.isPriceChanged).toBeTruthy();
      expect(service.selection.reboost).toBeTruthy();
      expect(service.quickbetNotificationService.saveErrorMessage)
        .toHaveBeenCalledWith('price is changed', 'warning', 'bet-status');
      expect(service.selection.onStakeChange).toHaveBeenCalled();
      expect(service.selection.price.isPriceDown).toBeTruthy();
      expect(pubSubService.publish).toHaveBeenCalledWith('SELECTION_PRICE_UPDATE_1', {
        priceDen: payload.priceDen,
        priceNum: payload.priceNum
      });
    });

    it('should update outcome isPriceChangeUp', () => {
      service.localeService.getString.and.returnValue('price is changed');
      service.selection.price = {
        priceNum: '2',
        priceDen: '1',
        priceTypeRef: {
          id: 'LP'
        }
      };
      service.fracToDecService.getDecimal = (n) => n;
      service.selection.isBoostActive = true;

      service.updateOutcomePrice(payload);
      expect(service.selection.reboost).toBeTruthy();
      expect(service.selection.price.isPriceUp).toBeTruthy();
    });

    it('should call getDecimal with 4 digits after comma', () => {
      service.selection.price = {
        priceNum: '2',
        priceDen: '1',
        priceType: 'LP',
        priceDec: undefined
      };

      service.updateOutcomePrice(payload);
      expect(service.fracToDecService.getDecimal).toHaveBeenCalledWith(3, 1, 4);
    });

    it('should update price in oddsSelector if SP and LP are available', () => {
      service.fracToDecService.getFormattedValue.and.returnValue(1.1);

      service.updateOutcomePrice(payload);
      expect(service.selection.newOddsValue).toEqual(1.1);
      expect(service.selection.oddsSelector[0].value).toEqual(
        service.selection.newOddsValue
      );
    });

    it('should reset oldPrice if the price was updated before', () => {
      service.fracToDecService.getFormattedValue.and.returnValue(1.1);

      service.updateOutcomePrice(payload);
      expect(service.selection.oldPrice).toEqual({
        priceNum: 2,
        priceDen: 1,
        priceType: 'LP'
      });
      expect(service.selection.oldOddsValue).toEqual(
        service.selection.newOddsValue
      );
    });

    it('should not reset price if the price was not updated before', () => {
      service.selection.newOddsValue = undefined;
      service.updateOutcomePrice(payload);
      expect(service.selection.oldOddsValue).toBeUndefined();
    });

    it('should not update price when SP and LP are not available', () => {
      service.selection.hasSPLP = false;
      service.selection.oddsSelector = undefined;
      service.updateOutcomePrice(payload);

      expect(service.selection.oddsSelector).toBeUndefined();
    });

    it('should update price when it was increased', () => {
      service.selection.isPriceUp = true;
      service.selection.isPriceDown = undefined;
      service.updateOutcomePrice(payload);

      expect(service.selection.isPriceUp).toBe(true);
      expect(service.selection.isPriceDown).toBeUndefined();
    });

    it('should update price when it was decreased', () => {
      service.selection.isPriceDown = true;
      service.selection.isPriceUp = undefined;
      service.updateOutcomePrice(payload);

      expect(service.selection.isPriceDown).toBe(true);
      expect(service.selection.isPriceUp).toBeUndefined();
    });

    it('should not update price if update is not available', () => {
      payload = undefined;
      expect(
        service.quickbetNotificationService.saveErrorMessage
      ).not.toHaveBeenCalled();
    });

    it('should not change price if prices are the same', () => {
      const priceDen = 1;
      const priceNum = 2;
      const payloadWithSamePrice = { priceDen, priceNum };

      service.selection.price = { priceDen, priceNum };
      service.updateOutcomePrice(payloadWithSamePrice);

      expect(fracToDecService.getDecimal).not.toHaveBeenCalled();
    });
  });

  describe('@_updateHandicap', () => {
    const newHandicapVal = '5.0';

    beforeEach(() => {
      service.selection = {
        handicapValue: '6.0',
        formatHandicap: jasmine.createSpy('formatHandicap'),
        updateHandicapValue: jasmine.createSpy('updateHandicapValue')
      };
      service.selection.formatHandicap.and.returnValue(newHandicapVal);
    });

    it('should update handicap if handicap updates are available', () => {
      const errMsg = 'error';
      localeService.getString.and.returnValue(errMsg);
      service['handlePriceOrHandicapChange'] = jasmine.createSpy('handlePriceOrHandicapChange');

      service.updateHandicap(newHandicapVal);

      expect(service.selection.updateHandicapValue).toHaveBeenCalledWith(
        jasmine.any(String)
      );
      expect(
        service.quickbetNotificationService.saveErrorMessage
      ).toHaveBeenCalledWith(errMsg, 'warning');
      expect(service['handlePriceOrHandicapChange']).toHaveBeenCalledWith(errMsg);
    });

    it('should not update handicap', () => {
      service.selection.handicapValue = '5.0';

      service.updateHandicap(newHandicapVal);
      expect(service.selection.updateHandicapValue).not.toHaveBeenCalled();
    });

    it('should update handicap but doesn"t show message', () => {
      const errMsg = 'error';
      service.disabled = true;
      localeService.getString.and.returnValue(errMsg);

      service.updateHandicap(newHandicapVal);
      expect(service.selection.updateHandicapValue).toHaveBeenCalledWith(
        jasmine.any(String)
      );
      expect(
        service.quickbetNotificationService.saveErrorMessage
      ).not.toHaveBeenCalled();
    });
  });

  describe('@applyUpdate', () => {
    let update;
    beforeEach(() => {
      update = {
        hcap_values: {
          A: true
        },
        message: {
          lp_num: 1,
          lp_den: 1
        },
        subChannel: {
          type: 'sPRICE'
        }
      };
      service.selection = {
        isUnnamedFavourite: false,
        outcomeMeaningMinorCode: 'A',
        price: {
          priceType: 'LP'
        }
      };
      service['updateOutcomePrice'] = jasmine.createSpy('updateOutcomePrice');
      service['updateHandicap'] = jasmine.createSpy('updateHandicap');
    });
    it('delta', () => {
      service['deltaObject'] = jasmine.createSpy('deltaObject').and.returnValue({
        hcap_values: {
          A: ''
        }
      });
      service.applyUpdate(update);
      expect(service['deltaObject']).toHaveBeenCalledWith(update);
    });
    it('should call updateOutcomePrice', () => {
      service.applyUpdate(update);
      expect(service['updateOutcomePrice']).toHaveBeenCalled();
    });
    it('should not call updateOutcomePrice', () => {
      service.selection.isUnnamedFavourite = true;
      service.applyUpdate(update);
      expect(service['updateOutcomePrice']).not.toHaveBeenCalled();
    });
    it('should not call updateHandicap', () => {
      service.applyUpdate(update);
      expect(service['updateHandicap']).not.toHaveBeenCalled();
    });
    it('should call updateHandicap', () => {
      update.subChannel.type = 'sMHCAP';
      service['deltaObject'] = jasmine.createSpy('deltaObject').and.returnValue({
        hcap_values: {
          A: true
        }
      });
      service.applyUpdate(update);
      expect(service['deltaObject']).toHaveBeenCalledWith(update);
      expect(service['updateHandicap']).toHaveBeenCalled();
    });
    it('should not call updateHandicap', () => {
      update.subChannel.type = 'sMHCAP';
      service['deltaObject'] = jasmine.createSpy('deltaObject').and.returnValue({
        hcap_values: {
          A: false
        }
      });
      service.applyUpdate(update);
      expect(service['updateHandicap']).not.toHaveBeenCalled();
    });
    it('should publish the eachway flag updated if eachWayFlagUpdated true', () => {
      update.subChannel.type = 'sEVMKT';
      update.message['ew_avail'] = 'N';
      service['eachWayFlagUpdated'] = jasmine.createSpy('deltaObject').and.returnValue(true);
      service['deltaObject'] = jasmine.createSpy('deltaObject').and.returnValue({
        hcap_values: {
          A: false
        },
        ew_avail: 'N'
      });
      service.applyUpdate(update);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EACHWAY_FLAG_UPDATED, ['N']);
    });
    it('should not publish the eachway flag updated if eachWayFlagUpdated false', () => {
      update.subChannel.type = 'sEVMKT';
      service['eachWayFlagUpdated'] = jasmine.createSpy('deltaObject').and.returnValue(false);
      service['deltaObject'] = jasmine.createSpy('deltaObject').and.returnValue({
        hcap_values: {
          A: false
        },
        ew_avail: 'Y'
      });
      service.applyUpdate(update);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.EACHWAY_FLAG_UPDATED, 'N');
    });
  });

  describe('@_deltaObject', () => {
    let update, delta;

    beforeEach(() => {
      update = {
        message: {
          lp_num: 1,
          lp_den: 1
        },
        subChannel: {
          type: 'sPRICE'
        }
      };
      delta = {
        priceDec: 1,
        priceDen: 1,
        priceNum: 1,
        priceType: 'LP'
      };
      service.selection = {
        price: {
          priceType: 'LP',
          priceTypeRef: {
            id: 'test'
          }
        }
      };
    });

    it('should set delta object with priceType if outcome price was updated', () => {
      service.fracToDecService.getDecimal.and.returnValue(1);
      service.suspensionPlace = '';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual(delta);
      expect(actResult.priceType).toBeDefined();
      expect(service.suspensionPlace).toBeFalsy();
    });

    it('should set delta object without priceType if outcome price was updated', () => {
      service.fracToDecService.getDecimal.and.returnValue(1);
      service.selection.price = null;
      service.suspensionPlace = '';
      const actResult = service.deltaObject(update);
      expect(actResult.priceType).not.toBeDefined();
      expect(actResult).not.toEqual(delta);

      expect(service.suspensionPlace).toBeFalsy();
    });

    it('should set delta object if selection was updated with price Type: price, suspension, dispalying', () => {
      service.fracToDecService.getDecimal.and.returnValue(1);
      update.subChannel.type = 'sSELCN';

      service.suspensionPlace = 'selection';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual(delta);
      expect(service.suspensionPlace).toEqual('selection');
    });
    it('should set delta object if selection was updated without priceType: price, suspension, dispalying', () => {
      service.fracToDecService.getDecimal.and.returnValue(1);
      update.subChannel.type = 'sSELCN';
      service.selection.price = null;
      service.suspensionPlace = 'selection';

      const actResult = service.deltaObject(update);
      expect(actResult).not.toEqual(delta);
      expect(actResult.priceType).not.toBeDefined();
      expect(service.suspensionPlace).toEqual('selection');
    });

    it('should set delta object if market was updated: suspension, dispaly', () => {
      update.subChannel.type = 'sEVMKT';

      service.suspensionPlace = 'market';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual({});
      expect(service.suspensionPlace).toEqual('market');
    });

    it('should set delta object with new handicup if handicap values were updated', () => {
      update.subChannel.type = 'sEVMKT';
      const mockHandicapValue = {
        hcap_values: {
          A: '-1.0',
          H: '+1.0',
          L: '+1.0'
        },
        ew_avail: 'Y'
      };
      update.message['hcap_values'] = mockHandicapValue.hcap_values;
      update.message['ew_avail'] = mockHandicapValue.ew_avail;
      service.suspensionPlace = 'market';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual(mockHandicapValue);
      expect(service.suspensionPlace).toEqual('market');
    });

    it('should set delta object if event was updated: suspension, dispaly', () => {
      update.subChannel.type = 'sEVENT';

      service.suspensionPlace = 'event';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual({});
      expect(service.suspensionPlace).toEqual('event');
    });
    it('should set delta object to empty', () => {
      update.subChannel.type = 'default';

      service.suspensionPlace = 'event';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual({});
      expect(service.suspensionPlace).toEqual('event');
    });

    it('should set delta object if handicap values were updated', () => {
      update.message['hcap_values'] = {
        A: '-1.0',
        H: '+1.0',
        L: '+1.0'
      };
      update.subChannel.type = 'sMHCAP';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual({
        hcap_values: {
          A: '-1.0',
          H: '+1.0',
          L: '+1.0'
        }
      });
    });
    it('should set delta object hcap_values L to hcap_values H if handicap values were updated', () => {
      update.message['hcap_values'] = {
        A: '-1.0',
        H: '+1.0'
      };
      update.subChannel.type = 'sMHCAP';

      const actResult = service.deltaObject(update);
      expect(actResult).toEqual({
        hcap_values: {
          A: '-1.0',
          H: '+1.0'
        }
      });
    });
    it('should not set delta object if handicap values were updated', () => {
      update.message['hcap_values'] = undefined;
      update.subChannel.type = 'sMHCAP';

      const actResult = service.deltaObject(update);
      expect(actResult).toBeUndefined();
    });
  });

  describe('@_filterGlobalDisable', () => {
    it('should check is bet suspended or undisplayed on every level of event', () => {
      const obj = {},
        result = service.filterGlobalDisable(obj);
      expect(result).toBe(false);
    });
    it('should check is bet suspended or undisplayed on every level of event true', () => {
      const obj = {value: true},
        result = service.filterGlobalDisable(obj);
      expect(result).toBe(true);
    });
  });

  describe('@fillDisableMap', () => {
    it('should fill map for multiple suspension', () => {
      const map = {
        event: false,
        market: false,
        outcome: true,
        selection: false
      };

      service.fillDisableMap(map);
      expect(service.disableMap).toEqual(map);
    });
  });

  describe('@isDisabled', () => {
    beforeEach(() => {
      service.update = {
        message: {
          displayed: 'Y',
          status: 'A'
        }
      };
      service['eventSuspension'] = {
        observers: [1],
        next: jasmine.createSpy()
      };
      service.suspensionPlace = 'selection';
      service.disabled = false;
      service.selection = {
        price: {
          isPriceChanged: true,
          priceType: 'LP'
        }
      };
      const errMsg = 'error';
      localeService.getString.and.returnValue(errMsg);
    });

    it('should check if bet is suspended or undisplayed', () => {
      service.update = {
        message: {
          displayed: 'N',
          status: 'S'
        }
      };
      service.suspensionPlace = 'selection';
      service.disabled = true;
      service.disableMap = {
        outcome: true
      };
      quickbetNotificationService.saveErrorMessage.and.returnValue(
        'some string'
      );

      service.isDisabled();

      expect(service.disabled).toBe(true);
      expect(service.disableMap.outcome).toBe(true);
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith('error', 'warning', 'bet-status');
      expect(localeService.getString).toHaveBeenCalledWith(
        'quickbet.singleDisabled',
        ['selection']
      );
      expect(service['eventSuspension'].next).toHaveBeenCalledWith(statusMock);
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.GET_QUICKBET_SELECTION_STATUS,
        [service.disabled, service.suspensionPlace]
      );
    });

    it('should clear notification message', () => {
      spyOn(service, 'filterGlobalDisable').and.returnValue(false);
      statusMock.disableBet = false;
      statusMock.msg = '';

      service.isDisabled();
      expect(service.disableMap.selection).toBe(false);
      expect(service.quickbetNotificationService.clear).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.GET_QUICKBET_SELECTION_STATUS,
        [service.disabled, service.suspensionPlace]
      );
      expect(service['eventSuspension'].next).toHaveBeenCalledWith(statusMock);
    });

    it('should check if bet is suspended and show error message', () => {
      spyOn(service, 'filterGlobalDisable').and.returnValue(true);
      statusMock.disableBet = true;
      statusMock.msg = 'error';

      service.isDisabled();

      expect(service.disableMap[service.suspensionPlace]).toBe(false);
      expect(
        service.quickbetNotificationService.saveErrorMessage
      ).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(
        pubSubService.API.GET_QUICKBET_SELECTION_STATUS,
        [false, 'selection']
      );
      expect(service['eventSuspension'].next).toHaveBeenCalledWith(statusMock);
    });

    it('should not check if bet is suspended or undisplayed', () => {
      service.update = undefined;
      service.suspensionPlace = undefined;

      service.isDisabled();
      expect(
        service.quickbetNotificationService.saveErrorMessage
      ).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should change isPriceChanged only if selection has price', () => {
      service.selection.price = null;
      service.isDisabled();

      expect(service['disableMap'][service.suspensionPlace]).toBeFalsy();
    });

    it('should show price change error message after unsuspend selection when price was changed before', () => {
      spyOn(service, 'showPriceChange');
      service.isDisabled();

      expect(service.showPriceChange).toHaveBeenCalled();
    });

    it('should not show price change error message after unsuspend selection when no price were found', () => {
      spyOn(service, 'showPriceChange');
      service.selection.price = null;
      service.isDisabled();

      expect(service.showPriceChange).not.toHaveBeenCalled();
    });

    it('should not show price change error message after unsuspend selection when isPriceChanged is false', () => {
      spyOn(service, 'showPriceChange');
      service.selection.price = {
        isPriceChanged: null
      };
      service.isDisabled();

      expect(service.showPriceChange).not.toHaveBeenCalled();
    });

    it('should not show price change error message after unsuspend selection when bet is still suspended', () => {
      spyOn(service, 'showPriceChange');
      service.selection.price = {
        isPriceChanged: null
      };
      service.disableMap = { event: true };
      service.isDisabled();

      expect(service.showPriceChange).not.toHaveBeenCalled();
    });
  });

  describe('@handleEventSuspension', () => {
    it('should return to the subscriber a fake status', () => {
      const fakeStatus: ISuspendedOutcomeError = { multipleWithDisableSingle: false, disableBet: true, msg: 'msg' };
      service.getEventSuspension().subscribe((status: ISuspendedOutcomeError) => {
        expect(status).toEqual(fakeStatus);
      });
      service['handleEventSuspension'](fakeStatus);
    });

    it('should not be called, because there are no subscribers', () => {
      const fakeStatus: ISuspendedOutcomeError = { multipleWithDisableSingle: false, disableBet: true, msg: 'msg' };
      service['eventSuspension'] = {
        observers: [],
        next: jasmine.createSpy()
      };
      service['handleEventSuspension'](fakeStatus);
      expect(service['eventSuspension'].next).not.toHaveBeenCalled();
    });
  });

  describe('@handlePriceChange', () => {
    it('should return to the subscriber a fake status', () => {
      const fakeMsg = 'msg';
      service.getPriceChange().subscribe((msg: string) => {
        expect(msg).toEqual(fakeMsg);
      });
      service['handlePriceOrHandicapChange'](fakeMsg);
    });

    it('should not be called with a fake status', () => {
      const fakeMsg = 'msg';
      service['priceChange'] = {
        observers: [],
        next: jasmine.createSpy()
      };
      service['handlePriceOrHandicapChange'](fakeMsg);
      expect(service['priceChange'].next).not.toHaveBeenCalled();
    });
  });

  describe('showPriceChange', () => {
    it('should use price when showing message', () => {
      const price = {
        id: 2312323,
        priceDec: '2.75',
        priceDen: 7,
        priceNum: 4,
        priceType: 'LP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };

      fracToDecService.getDecimal.and.returnValue('2.75');
      localeService.getString.and.callFake((v, p) => [v, p]);
      service.selection = { price };
      service['handlePriceOrHandicapChange'] = jasmine.createSpy('handlePriceOrHandicapChange');

      service['showPriceChange']();

      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(['quickbet.priceIsChanged', ['2.75', '2.75']],
        'warning', 'bet-status');
      expect(service['handlePriceOrHandicapChange']).toHaveBeenCalledWith(['quickbet.priceIsChanged', ['2.75', '2.75']]);
      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(4, 7);
    });

    it('should use oldPrice when showing message', () => {
      const price = {
        id: 2312323,
        priceDec: '2.75',
        priceDen: 7,
        priceNum: 4,
        priceType: 'LP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };
      const oldPrice = {
        id: 2312323,
        priceDec: '2.75',
        priceDen: 11,
        priceNum: 5,
        priceType: 'LP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };

      fracToDecService.getDecimal.and.returnValue('2.75');
      localeService.getString.and.callFake((v, p) => [v, p]);
      service.selection = { price, oldPrice };
      service['handlePriceOrHandicapChange'] = jasmine.createSpy('handlePriceOrHandicapChange');

      service['showPriceChange']();

      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalledWith(['quickbet.priceIsChanged', ['2.75', '2.75']],
        'warning', 'bet-status');
      expect(service['handlePriceOrHandicapChange']).toHaveBeenCalledWith(['quickbet.priceIsChanged', ['2.75', '2.75']]);
      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(4, 7);
      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(5, 11);
    });
  });

  describe('getOdds', () => {
    beforeEach(() => {
      fracToDecService.getDecimal.and.returnValues('1.25', '1.20');
    });

    it('should return odds in correct format', () => {
      const price = {
        id: 2312323,
        priceDec: '2.75',
        priceDen: 7,
        priceNum: 4,
        priceType: 'LP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };

      fracToDecService.getDecimal.and.returnValue('2.75');

      const response = service.getOdds(price);
      expect(response).toBe('2.75');
    });

    it('should return odds in dec format', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        priceType: 'LP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };
      userService.oddsFormat = 'frac';
      expect(service.getOdds(price, 'dec')).toBe('1.25');
    });

    it('should return empty string if no price', () => {
      const response = service.getOdds();
      expect(response).toBe('');
    });

    it('getOdds (price.priceType: undefined)', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: { id: '' },
        handicapValueDec: ''
      };
      userService.oddsFormat = 'frac';
      expect(service.getOdds(price, 'dec')).toBe('1.25');
    });

    it('getOdds (price.priceType: undefined, priceTypeRef.id: undefined)', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: {},
        handicapValueDec: ''
      };

      userService.oddsFormat = 'frac';
      expect(service.getOdds(price, 'dec')).toBe('1.25');
    });

    it('getOdds (price.priceType: undefined, priceTypeRef: undefined)', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        handicapValueDec: ''
      };

      userService.oddsFormat = 'frac';
      expect(service.getOdds(price, 'dec')).toBe('1.25');
    });

    it('should return SP in case of priceType is SP', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        priceType: 'SP',
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: {},
        handicapValueDec: ''
      };

      expect(service.getOdds(price, 'dec')).toBe('SP');
    });

    it('should return SP in case of id of priceTypeRef is SP', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 1,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: {
          id: 'SP'
        },
        handicapValueDec: ''
      };

      expect(service.getOdds(price, 'dec')).toBe('SP');
    });

    it('should return frac format if userService has no dec format', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 3,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: {},
        handicapValueDec: ''
      };

      userService.oddsFormat = 'frac';
      expect(service.getOdds(price, undefined)).toEqual('1/3');
    });

    it('should return frac format if passed format type if frac', () => {
      const price = {
        id: 2312323,
        priceDec: '',
        priceDen: 3,
        priceNum: 1,
        isPriceChanged: false,
        isPriceUp: false,
        isPriceDown: false,
        priceTypeRef: {},
        handicapValueDec: ''
      };

      userService.oddsFormat = '';
      expect(service.getOdds(price, 'frac')).toEqual('1/3');
    });
  });

  describe('isHandicapChanged', () => {
    const selection = {
      price: {
        priceNum: 2,
        priceDen: 1,
        priceType: 'LP'
      },
      newOddsValue: 1.1,
      onStakeChange: jasmine.createSpy('onStakeChange'),
      hasSPLP: true,
      oddsSelector: [{value: 1.1}],
      isPriceChanged: true,
      isPriceUp: true,
      outcomeStatusCode: 'A'
    } as any;


    it('should check if handicap value was changed(when no selection were found)', () => {
      const actualResult = service.isHandicapChanged(null);

      expect(actualResult).toBeFalsy();
    });

    it('should check if handicap value was changed(negative case)', () => {
      const actualResult = service.isHandicapChanged(selection);

      expect(actualResult).toBeFalsy();
    });

    it('should check if handicap value was changed: negative case - handicap value was changed but selection was used again', () => {
      selection.oldHandicapValue = '+1.0';
      selection.handicapValue = '+1.0';
      const actualResult = service.isHandicapChanged(selection);

      expect(actualResult).toBeFalsy();
    });

    it('should check if handicap value was changed(positive case)', () => {
      selection.oldHandicapValue = '-1.0';
      selection.handicapValue = '+1.0';
      const actualResult = service.isHandicapChanged(selection);

      expect(actualResult).toBeTruthy();
    });
  });
  describe('#isEachWayFlagUpdated', () => {
    it('should return true if both the update and selection.isEachWayAvailable are not equal', () => {
      const selection = {
        isEachWayAvailable: true
      } as any;
      expect(service['isEachWayFlagUpdated']('N', selection)).toBeTruthy();
    });
    it('should return false if both the update and selection.isEachWayAvailable  are equal', () => {
      const selection = {
        isEachWayAvailable: true
      } as any;
      expect(service['isEachWayFlagUpdated']('Y', selection)).toBeFalsy();
    });
  });
});
