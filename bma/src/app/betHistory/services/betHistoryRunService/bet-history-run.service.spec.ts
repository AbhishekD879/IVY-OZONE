import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';

import { BetHistoryRunService } from '@app/betHistory/services/betHistoryRunService/bet-history-run.service';
import { BetsIntegrationService } from '@app/betHistory/services/betsIntegration/bets-integration.service';
import { OpenBetsCounterService } from '@app/betHistory/services/openBetsCounter/open-bets-counter.service';

describe('test BetHistoryRunService', () => {
  let service: BetHistoryRunService;
  let commandService;
  let betsIntegrationService;
  let cashoutBetsStreamService;
  let commandsMap;
  let localeService;
  let injector;
  let openBetsCounterService;

  beforeEach(() => {
    commandsMap = {};
    commandService = {
      register: jasmine.createSpy('register').and.callFake((key, fn) => {
        commandsMap[key] = fn;
      }),
      API: {
        OPEN_CASHOUT_STREAM: 'OPEN_CASHOUT_STREAM',
        CLOSE_CASHOUT_STREAM: 'CLOSE_CASHOUT_STREAM',
        GET_CASH_OUT_BETS_ASYNC: 'GET_CASH_OUT_BETS_ASYNC',
        GET_PLACED_BETS_ASYNC: 'GET_PLACED_BETS_ASYNC',
        GET_BETS_FOR_EVENT_ASYNC: 'GET_BETS_FOR_EVENT_ASYNC',
        GET_OPEN_BETS_COUNT: 'GET_OPEN_BETS_COUNT'
      }
    };
    localeService = {
      setLangData: jasmine.createSpy()
    };
    betsIntegrationService = {
      getCashOutBets: jasmine.createSpy('getCashOutBets').and.returnValue(observableOf()),
      getPlacedBets: jasmine.createSpy('getPlacedBets').and.returnValue(observableOf()),
      getBetsForEvent: jasmine.createSpy('getBetsForEvent').and.returnValue(observableOf())
    };
    cashoutBetsStreamService = {
      openBetsStream: jasmine.createSpy('openBetsStream').and.returnValue(observableOf([])),
      closeBetsStream: jasmine.createSpy('closeBetsStream')
    };
    openBetsCounterService = {
      init: jasmine.createSpy('init'),
      unsubscribeBetsCounter: jasmine.createSpy('unsubscribeBetsCounter')
    };
    injector = {
      get(type) {
        if (type === BetsIntegrationService) {
          return betsIntegrationService;
        } else
        if (type === OpenBetsCounterService) {
          return openBetsCounterService;
        }
        return cashoutBetsStreamService;
      }
    };

    service = new BetHistoryRunService(commandService as any, localeService as any, injector as any);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#run should test bethistory initial subscriptions', () => {
    service.run();
    expect(localeService.setLangData).toHaveBeenCalled();
    expect(commandService.register).toHaveBeenCalledTimes(7);
  });

  it('should register "OPEN_CASHOUT_STREAM" command', fakeAsync(() => {
    service.run();
    commandsMap[commandService.API.OPEN_CASHOUT_STREAM]();
    tick();

    expect(commandService.register).toHaveBeenCalledWith(commandService.API.OPEN_CASHOUT_STREAM, jasmine.any(Function));
    expect(cashoutBetsStreamService.openBetsStream).toHaveBeenCalled();
  }));

  it('should register "CLOSE_CASHOUT_STREAM" command', fakeAsync(() => {
    service.run();
    commandsMap[commandService.API.CLOSE_CASHOUT_STREAM]();
    tick();

    expect(commandService.register).toHaveBeenCalledWith(commandService.API.CLOSE_CASHOUT_STREAM, jasmine.any(Function));
    expect(cashoutBetsStreamService.closeBetsStream).toHaveBeenCalled();
  }));
  it('should register "GET_OPEN_BETS_COUNT" command', fakeAsync(() => {
    service.run();
    commandsMap[commandService.API.GET_OPEN_BETS_COUNT]();
    tick();

    expect(commandService.register).toHaveBeenCalledWith(commandService.API.GET_OPEN_BETS_COUNT, jasmine.any(Function));
    expect(openBetsCounterService.init).toHaveBeenCalled();
  }));
  it('should register "UNSUBSCRIBE_OPEN_BETS_COUNT" command', fakeAsync(() => {
    service.run();
    commandsMap[commandService.API.UNSUBSCRIBE_OPEN_BETS_COUNT]();
    tick();

    expect(commandService.register).toHaveBeenCalledWith(commandService.API.UNSUBSCRIBE_OPEN_BETS_COUNT, jasmine.any(Function));
    expect(openBetsCounterService.unsubscribeBetsCounter).toHaveBeenCalled();
  }));
  it('#openBetsCounterService: should inject OpenBetsCounterService', () => {
    injector.get = jasmine.createSpy().and.returnValue(openBetsCounterService);

    expect(service['openBetsCounterService']).toBe(openBetsCounterService);
    expect(injector.get).toHaveBeenCalledWith(OpenBetsCounterService);
  });
});
