import { of as observableOf, throwError } from 'rxjs';
import { CashoutDataProvider } from '@app/betHistory/services/cashoutDataProvider/cashout-data.provider';
import { fakeAsync, tick } from '@angular/core/testing';

describe('CashoutDataProvider', () => {
  let service: CashoutDataProvider;
  let pubSubService, deviceService, bppService, loadByPortionsService, ssService, ssRequestHelperService,
    buildEventsBsService, buildEventsWithScoresAndClockBsService, buildEventsWithScoresBsService;
  let awsService;
  let eventMock;

  beforeEach(() => {
    eventMock = {
      id: 1,
      markets: [{ isMarketBetInRun: 'true' }],
      isStarted: true
    } as any;

    pubSubService = {
        publish: jasmine.createSpy('publish'),
        API: {
          RELOAD_CASHOUT: 'RELOAD_CASHOUT'
        }
      }  as any;
    deviceService = {
      channel: {
        channelRef: {
          id: '6'
        }
      },
      isMobile: true
    } as any;
    bppService = {
      send: jasmine.createSpy().and.returnValue(observableOf({
        response: {
          respTransGetBetDetail: {
            bet: [{}]
          },
          respTransGetBetsPlaced: {
            bets: [{}]
          },
          respTransGetBetDetails: {
            bets: [{}]
          }
        }
      })),
      showErrorPopup: jasmine.createSpy()
    } as any;
    loadByPortionsService = {
      get: jasmine.createSpy().and.returnValue(Promise.resolve([{
        event: {
          id: 1,
          children: [{}]
        }
      }]))
    } as any;
    ssService = {
      getEventsByOutcomeIds: jasmine.createSpy().and.returnValue(Promise.resolve([{x: 1}]))
    } as any;
    ssRequestHelperService = {
      getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve({}))
    } as any;
    buildEventsBsService = {
      build: jasmine.createSpy().and.returnValue(
        [
          eventMock
        ]
      )
    } as any;
    buildEventsWithScoresAndClockBsService = {
      build: jasmine.createSpy().and.returnValue(observableOf([{}]))
    } as any;

    buildEventsWithScoresBsService = {
      build: jasmine.createSpy().and.returnValue(observableOf({
          id: 1,
          markets: [{
          isMarketBetInRun: 'true'
        }],
        isStarted: true
      }))
    } as any;

    awsService = {
      addAction: jasmine.createSpy()
    } as any;

    spyOn(console, 'warn');
    service = new CashoutDataProvider(pubSubService, deviceService, bppService, loadByPortionsService,
      ssService, ssRequestHelperService, buildEventsBsService, buildEventsWithScoresAndClockBsService,
      buildEventsWithScoresBsService, awsService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#getBet: should get some bets with cashOut param by cash out ids', fakeAsync(() => {
    service.getBet(['']).subscribe((response) => {
      expect(bppService.send.calls.first().args[0]).toEqual('getBetDetail');
      expect(response.length).not.toBe(0);
    });
    tick();
  }));

  it('#getBet: should throw error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.getBet(['']).subscribe(() => {
    }, () => {
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
    });
    tick();
  }));

  it('#getBet: should throw error and not show popup', fakeAsync(() => {
    const error = 'err';
    bppService.send = jasmine.createSpy().and.returnValue(throwError(error));

    service.getBet([''], false, false).subscribe(() => {},
      (result) => {
        expect(result).toEqual(error);
        expect(bppService.showErrorPopup).not.toHaveBeenCalledWith('cashOutError');
      });
    tick();
  }));

  it('#getBet: should throw error and not show popup if error not provided', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError(null));

    service.getBet([''], false, true).subscribe(() => {},
      (result) => {
        expect(result).toBeNull();
        expect(bppService.showErrorPopup).not.toHaveBeenCalledWith('cashOutError');
      });
    tick();
  }));

  it('#isScoresAndClockAvailable: should return true if event isStarted is true', () => {
    eventMock = {
      id: 1,
      markets: [{ templateMarketName: 'Match Betting', isMarketBetInRun: 'true' },
      { templateMarketName: 'Build Your Bet BOTH TEAMS TO SCORE IN BOTH HALVES', isMarketBetInRun: 'true' }],
      isStarted: true,
      isFinished: false
    } as any;
    expect(service['isScoresAndClockAvailable'](eventMock)).toBe(true);
  });

  it('#isScoresAndClockAvailable: should return false if event isStarted is not present', () => {
    eventMock = {
      id: 1,
      markets: [{ templateMarketName: 'Match Betting', isMarketBetInRun: 'true' },
      { templateMarketName: 'First Team to Score' }]
    } as any;
    expect(service['isScoresAndClockAvailable'](eventMock)).toBe(false);
  });

  it('#getEventsByOutcomesIds: should get market ids from outcome ids', fakeAsync(() => {
    // three service private functions covered here:
    // getCommentsByEvents and isScoresAndClockAvailable in scope of loadScoresAndClock
     spyOn<any>(service, 'getCommentsByEvents').and.callThrough();

    service.getEventsByOutcomesIds(['1']).subscribe((response) => {
       expect(ssService.getEventsByOutcomeIds).toHaveBeenCalledWith({
        outcomesIds: ['1'],
        includeUndisplayed: true,
        racingFormOutcome: true
      });
      expect(buildEventsBsService.build).toHaveBeenCalledWith([{ x: 1}]);
      expect(buildEventsWithScoresBsService.build).toHaveBeenCalledWith(eventMock);
      expect(service['getCommentsByEvents']).toHaveBeenCalledWith([1]);
      expect(buildEventsWithScoresAndClockBsService.build).toHaveBeenCalled();
      expect(response.length).not.toBe(0);
    });
    tick();
  }));

  it('#getEventsByOutcomesIds: should support custom parameters, which override predefined', () => {
    service.getEventsByOutcomesIds(['1'], { racingFormOutcome: false, somethingElse: true });
    expect(ssService.getEventsByOutcomeIds).toHaveBeenCalledWith({
      outcomesIds: ['1'],
      includeUndisplayed: true,
      racingFormOutcome: false,
      somethingElse: true
    });
  });

  it('#getEventsByOutcomesIds: should throw error', fakeAsync(() => {
    ssService.getEventsByOutcomeIds.and.returnValue(Promise.reject('some error'));
    service.getEventsByOutcomesIds(['1']).subscribe(() => {
    }, () => {
      expect(console.warn).toHaveBeenCalledWith('Error while getting Event from SS (siteServerFactoryBs.getEventsByOutcomesIds)');
    });
    tick();
  }));

  it('#getPlacedBets: should get placed bets', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(observableOf({
      response: {
        respTransGetBetsPlaced: {
          bets: [{}]
        },
      }
    }));
    service.getPlacedBets(1).subscribe((response) => {
      expect(bppService.send).toHaveBeenCalledWith('getBetsPlaced', { eventId: 1 });
      expect(response.length).not.toBe(0);
    });
    tick();
  }));

  it('#getPlacedBets: should get no bets if eventId is falsy', fakeAsync(() => {
    service.getPlacedBets(0).subscribe((response) => {
      expect(response.length).toBe(0);
    });
    tick();
  }));

  it('#getPlacedBets: should throw error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.getPlacedBets(1).subscribe(() => {
    }, () => {
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
    });
    tick();
  }));

  it('#getCashOutBets: should get all bets with cashOut param', fakeAsync(() => {
    service.getCashOutBets().subscribe((response) => {
      expect(bppService.send).toHaveBeenCalledWith('getBetDetails', {
        cashoutBets: 'Y',
        status: 'A',
        returnPartialCashoutDetails: 'Y',
        filter: 'Y'
      });
      expect(response.length).not.toBe(0);
    });
    tick();
  }));

  it('#getCashOutBets: should throw error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.getCashOutBets().subscribe(() => {
    }, () => {
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
    });
    tick();
  }));

  it('#getCashOutBets: should throw error and not show popup', fakeAsync(() => {
    const error = 'err';
    bppService.send = jasmine.createSpy().and.returnValue(throwError(error));

    service.getCashOutBets(false).subscribe(() => {
    }, (result) => {
      expect(result).toEqual(error);
      expect(bppService.showErrorPopup).not.toHaveBeenCalledWith('cashOutError');
    });
    tick();
  }));

  it('#makeCashOutRequest: should make cash out request for outcome', fakeAsync(() => {
    // service private function generateCashOutBetReqParams covered here
    const dataStub = {
      betId: 1,
      cashOutAmount: '2',
      currency: '3'
    } as any;
    service.makeCashOutRequest(dataStub).subscribe((response) => {
      expect(bppService.send).toHaveBeenCalledWith(
        'cashoutBet', {
        betRef: { id: 1, provider: 'OpenBetSports' },
        channelRef: deviceService.channel.channelRef,
        cashoutValue: {
          amount: '2',
          partialCashoutAmount: null,
          partialCashoutPercentage: null,
          currencyRef: { id: '3' }
        }
      });
     expect(response).toBeTruthy();
    });
    tick();
  }));

  it('#makeCashOutRequest: should make cash out request for outcome ( diff params )', fakeAsync(() => {
    // service private function generateCashOutBetReqParams covered here
    const dataStub = {
      betId: 1,
      cashOutAmount: '2',
      currency: '3',
      partialCashOutAmount: '4',
      partialCashOutPercentage: '5'
    } as any;
    service.makeCashOutRequest(dataStub).subscribe((response) => {
      expect(bppService.send).toHaveBeenCalledWith('cashoutBet', {
        betRef: { id: 1, provider: 'OpenBetSports' },
        channelRef: deviceService.channel.channelRef,
        cashoutValue: {
          amount: '2',
          partialCashoutAmount: '4',
          partialCashoutPercentage: '5',
          currencyRef: { id: '3' }
        }
      });
      expect(response).toBeTruthy();
    });
    tick();
  }));

  it('#makeCashOutRequest: should throw error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.makeCashOutRequest({} as any).subscribe(() => {
    }, () => {
      expect(pubSubService.publish).toHaveBeenCalledWith('RELOAD_CASHOUT');
    });

    deviceService.isMobile = false;
    const analyticsParams = {
      betId: '123',
      cashOutAmount: '123',
      partialCashOutAmount: '123',
      partialCashOutPercentage: '123',
      currency: '123',
      error: 'err',
    };
    service.makeCashOutRequest(analyticsParams).subscribe(() => {
    }, () => {
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
      expect(awsService.addAction).toHaveBeenCalledWith
      ('cashout=>UI_Message=>(bpp)Unavailable=>makeCashOutRequest', analyticsParams);
    });
    tick();
  }));

  it('#makeReadBetRequest: should make cash out makeReadBet request for outcome', fakeAsync(() => {
    service.makeReadBetRequest('1', {} as any).subscribe((response) => {
      expect(bppService.send).toHaveBeenCalledWith('readBet', {
        betRef: [{
          id: '1',
          provider: 'OpenBetCashoutDelay'
        }]
      });
      expect(response).toBeTruthy();
    });

    bppService.send = jasmine.createSpy().and.returnValue(observableOf([]));
    service.makeReadBetRequest('1', {} as any).subscribe((response) => {
      expect((response as any).length).toBe(0);
    });
    tick();
  }));

  it('#makeReadBetRequest: should throw error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    const analyticsParams = {
      betId: '123',
      cashOutAmount: '123',
      partialCashOutAmount: '123',
      partialCashOutPercentage: '123',
      currency: '123',
      error: 'err',
    };
    service.makeReadBetRequest('1', analyticsParams).subscribe(() => {
    }, () => {
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
      expect(awsService.addAction).toHaveBeenCalledWith(
        'cashout=>UI_Message=>(bpp)Unavailable=>makeReadBetRequest', analyticsParams);
    });
    tick();
  }));

  it('getBet should track error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    const analyticsParams = {
      betId: '123',
      showErrorPopup: true,
      error: 'err'
    };
    service.getBet(['123']).subscribe(() => {}, () => {
      expect(awsService.addAction).toHaveBeenCalledWith('cashout=>UI_Message=>(bpp)Unavailable=>getBet', analyticsParams);
    });
    tick();
  }));

  it('getPlacedBets should track error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.getPlacedBets(123).subscribe(() => {}, () => {
      expect(awsService.addAction).toHaveBeenCalledWith('cashout=>UI_Message=>(bpp)Unavailable=>getPlacedBets');
    });
    tick();
  }));

  it('getCashOutBets should track error', fakeAsync(() => {
    bppService.send = jasmine.createSpy().and.returnValue(throwError('err'));
    service.getCashOutBets(true).subscribe(() => {}, () => {
      expect(awsService.addAction).toHaveBeenCalledWith('cashout=>UI_Message=>(bpp)Unavailable=>getCashOutBets');
    });
    tick();
  }));

});
