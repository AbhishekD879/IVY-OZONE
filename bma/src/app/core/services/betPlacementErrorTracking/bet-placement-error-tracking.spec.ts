import { BetPlacementErrorTrackingService } from './bet-placement-error-tracking';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { tick, fakeAsync } from '@angular/core/testing';

describe('BetPlacementErrorTrackingService', () => {
  let service: BetPlacementErrorTrackingService;
  let gtmService;
  let command;
  let location;
  let bet;

  beforeEach(() => {
    bet = <any>[
      {
        Bet: {
          isMocked: true,
          legs: [],
          error: '400'
        },
        stake: {
          freeBetAmount: 1
        }
      }
    ];
    gtmService = {
      pushBetPlacementErrorInfo: jasmine.createSpy()
    };
    command = {
      API: commandApi,
      executeAsync: jasmine.createSpy().and.callFake(() => new Promise((resolve) => resolve([1])))
    };
    location = {
      path: jasmine.createSpy()
    };
    service = new BetPlacementErrorTrackingService(gtmService, command, location);
  });

  it('constructor', () => {
    expect(service).toBeDefined();
    expect(service['betPlacementErrorStatic']).toEqual({
      event: 'trackEvent',
      eventCategory: 'betslip',
      eventAction: 'place bet',
      eventLabel: 'failure'
    });
  });

  it('should send BetSlip', fakeAsync(() => {
    service.sendBetSlip(
      bet,
      bet,
      [],
      '500',
      'msg',
      {
        isOnlyMultiples: true,
        bothTypesError: true
      }
    );
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.GET_LIVE_STREAM_STATUS, undefined, false);
    tick();
    expect(gtmService.pushBetPlacementErrorInfo).toHaveBeenCalledWith(jasmine.objectContaining(
      {
        errorCode: '500',
        errorMessage: 'msg'
      }
    ));
  }));

  it('should send Lotto', fakeAsync(() => {
    service.sendLotto('400', 'msg');
    expect(gtmService.pushBetPlacementErrorInfo).toHaveBeenCalledWith(jasmine.objectContaining({betCategory: 'Lotto'}));
  }));

  it('should send send Jackpot', fakeAsync(() => {
    service.sendJackpot('400', 'msg');
    expect(gtmService.pushBetPlacementErrorInfo).toHaveBeenCalledWith(jasmine.objectContaining({betCategory: 'Football'}));
  }));
});
