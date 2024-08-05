import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CashoutErrorMessageService } from '@app/betHistory/services/cashoutErrorMessageService/cashout-error-message.service';
import { BetModelService } from '@app/betHistory/services/betModelService/bet-model.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import {
  CashOutLiveUpdatesSubscribeService
} from '@app/betHistory/services/cashOutLiveUpdatesSubscribeService/cashOutLiveUpdatesSubscribeService';

describe('CashoutMapService', () => {
  let service;
  let betHistoryMainService;
  let localeService;

  const pubSubService: PubSubService = jasmine.createSpyObj('PubSubService', ['subscribe', 'API']);
  const cashOutErrorMessage: CashoutErrorMessageService = jasmine.createSpyObj(['getErrorMessage']);
  const betModelService: BetModelService = jasmine.createSpyObj(['getBetTimeString', 'getPotentialPayout']);
  const cashOutMapIndex: CashoutMapIndexService = jasmine.createSpyObj(['deleteItem']);
  const cashOutLiveUpdatesSubscribeService: CashOutLiveUpdatesSubscribeService = jasmine.createSpyObj(['addWatch']);
  const currencyMock = 'GBP';
  const currencySymbolMock = '£';
  const cashoutBetsArrayMock: any = [
    {
      betId: '111',
    },
    {
      betId: '222'
    },
    {
      betId: '444'
    },
    {
      betId: '555'
    }
  ];

  const regularBetsArray = [
    { id: 'b1', betId: 'b1', betType: {}, leg: [], stake: {}, isConfirmed: false },
    { id: 'b2', betId: 'b2', betType: {}, leg: [], stake: {}, inProgress: false },
    { id: 'b3', betId: 'b3', betType: {}, leg: [], stake: {}, isConfirmed: true },
    { id: 'b4', betId: 'b4', betType: {}, leg: [], stake: {}, inProgress: true }] as any;


  beforeEach(() => {
    betHistoryMainService = {
      getSortCode: jasmine.createSpy('getSortCode'),
      getBetStatus: jasmine.createSpy('getBetStatus'),
      getBetReturnsValue: jasmine.createSpy('getBetReturnsValue').and.returnValue({})
    };
    localeService = {};
    service = new CashOutMapService(
      pubSubService,
      cashOutErrorMessage,
      betModelService,
      cashOutMapIndex,
      cashOutLiveUpdatesSubscribeService,
      betHistoryMainService,
      localeService
    );
  });


  it('should be initialized', () => {
    spyOn(service, 'registerEvents');

    service.init();
    expect(service.registerEvents).toHaveBeenCalled();
    expect(service.cashoutBetsMap).toBeDefined();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(jasmine.any(String), pubSubService.API.SESSION_LOGOUT, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(jasmine.any(String),  pubSubService.API.SUCCESSFUL_LOGIN, jasmine.any(Function));
  });

  describe('createCashoutBetsMap', () => {
    beforeEach(() => {
      spyOn(service.cashoutBetsMap, 'createUpdatedCashoutBetsMap').and.callThrough();
    });
    it('should Create cashoutBetsMap object from bets with Bets IDs for BPP Cashout flow', () => {
      const cashOutBetsMap = service.createCashoutBetsMap(cashoutBetsArrayMock, currencyMock, currencySymbolMock, false);
      expect(service.cashoutBetsMap.createUpdatedCashoutBetsMap).toHaveBeenCalledWith(cashoutBetsArrayMock, 'GBP', '£', false);

      expect(cashOutBetsMap[cashoutBetsArrayMock[0].betId]).toBeDefined();
      expect(cashOutBetsMap[cashoutBetsArrayMock[1].betId]).toBeDefined();
      expect(cashOutBetsMap[cashoutBetsArrayMock[2].betId]).toBeDefined();
      expect(cashOutBetsMap[cashoutBetsArrayMock[3].betId]).toBeDefined();
    });

    describe('should Create cashoutBetsMap object from bets with Bets IDs for WS Cashout flow', () => {
      let fromWS = true;
      beforeEach(() => regularBetsArray.forEach(x => x['updatedValue'] = '10.00'));
      it('(fromWS === true)', () => {});
      it('(default)', () => fromWS = undefined);
      afterEach(() => {
        const cashOutBetsMap = service.createCashoutBetsMap(regularBetsArray, currencyMock, currencySymbolMock, fromWS);
        expect(cashOutLiveUpdatesSubscribeService.addWatch).toHaveBeenCalledWith(cashOutBetsMap);
        expect(service.cashoutBetsMap.createUpdatedCashoutBetsMap).toHaveBeenCalledWith(regularBetsArray, 'GBP', '£', true);
        expect(cashOutBetsMap[regularBetsArray[0].id]['updatedValue']).toEqual('10.00');
        expect(cashOutBetsMap[regularBetsArray[1].id]['updatedValue']).toEqual('10.00');
        expect(cashOutBetsMap[regularBetsArray[2].id]['updatedValue']).toEqual('10.00');
        expect(cashOutBetsMap[regularBetsArray[3].id]['updatedValue']).toEqual('10.00');
      });
    });
  });


  it('should test isEmptyObj method for cashoutBets data with ids', () => {
    expect(service.isEmptyObj({})).toBeTruthy();

    expect(service.isEmptyObj({
      notABetId: 'should have properties as numbers only'
    })).toBeTruthy();

    expect(service.isEmptyObj({
      111: {}
    })).toBeFalsy();
  });
});
