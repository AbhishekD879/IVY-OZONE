import { of as observableOf } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';

import { ToteBetSlipService } from './tote-bet-slip.service';
import { WinPoolBetsModel } from '../poolBetsModels/wn.model';
import { PlacePoolBetsModel } from '../poolBetsModels/pl.model';
import { ShowPoolBetsModel } from '../poolBetsModels/sh.model';
import { ExPoolBetsModel } from '../poolBetsModels/ex.model';
import { TrPoolBetsModel } from '../poolBetsModels/tr.model';

describe('ToteBetSlipService', () => {
  let service: ToteBetSlipService;

  let userService;
  let deviceService;
  let bppService;
  let toteBetReceipt;
  let clientUserAgentService;
  let timeSyncService;

  beforeEach(() => {
    userService = {};

    deviceService = {
      channel: {}
    };

    bppService = {
      send: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    toteBetReceipt = {
      betReceiptBuilder: jasmine.createSpy()
    };

    clientUserAgentService = {
      getId: jasmine.createSpy()
    };
    timeSyncService = {
      ip: '192.168.3.1'
    };

    service = new ToteBetSlipService(
      userService,
      deviceService,
      bppService,
      toteBetReceipt,
      clientUserAgentService,
      timeSyncService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['poolBetsModels']).toEqual({
      WN: WinPoolBetsModel,
      PL: PlacePoolBetsModel,
      SH: ShowPoolBetsModel,
      EX: ExPoolBetsModel,
      TR: TrPoolBetsModel
    });
  });

  it('getPoolBetsInstance', () => {
    const models = service['poolBetsModels'];

    for (const poolType in models) {
      if (!models.hasOwnProperty(poolType)) {
        continue;
      }

      const modelClass = models[poolType];
      const instance = service.getPoolBetsInstance(poolType, {
        pools: [{ poolType }],
        markets: [{ outcomes: [] }]
      } as any);

      expect(instance).toEqual(jasmine.any(modelClass));
    }

    expect(service.getPoolBetsInstance('_', {} as any)).toBeUndefined();
  });

  describe('placeBets', () => {
    it('has bet', fakeAsync(() => {
      service['placeBets']({
        bet: {
          betslip: {
            stake: { currencyRef: {} },
            slipPlacement: {}
          },
          bet: [{ stake: { currencyRef: {} } }]
        }
      }).subscribe(() => {
        expect(bppService.send).toHaveBeenCalled();
        expect(toteBetReceipt.betReceiptBuilder).toHaveBeenCalled();
      });

      flush();
    }));

    it('no bet', fakeAsync(() => {
      service['placeBets'](null);
      tick();
      expect(bppService.send).not.toHaveBeenCalled();
    }));
  });

  it('getCurrency', () => {
    expect(service.getCurrency('USD')).toBe('$');
    expect(service.getCurrency('UAH')).toBe('UAH');
    expect(service.getCurrency('AUD')).toBe('AUD');
  });

  it('isUserLoggedIn', () => {
    userService.status = true;
    expect(service.isUserLoggedIn()).toBeTruthy();

    userService.status = false;
    expect(service.isUserLoggedIn()).toBeFalsy();
  });

  it('addUserDetails', () => {
    const bet: any = {
      betslip: {
        stake: {
          currencyRef: {}
        }
      },
      bet: [{
        stake: {
          currencyRef: {}
        }
      }]
    };

    service['addUserDetails'](bet);
    expect(bet.betslip.stake.currencyRef.id).toBeUndefined();
    expect(bet.bet[0].stake.currencyRef.id).toBeUndefined();

    userService.currency = 1;
    service['addUserDetails'](bet);
    expect(bet.betslip.stake.currencyRef.id).toBe(1);
    expect(bet.bet[0].stake.currencyRef.id).toBe(1);
  });

  it('addDeviceDetails', () => {
    const bet: any = {
      betslip: {
        slipPlacement: {}
      }
    };

    service['addDeviceDetails'](bet);
    expect(bet.betslip.clientUserAgent).toBeUndefined();
    expect(bet.betslip.slipPlacement.channelRef).toBeUndefined();

    (clientUserAgentService.getId as jasmine.Spy).and.returnValue('testId');
    deviceService.userAgent = 'Chrome';
    deviceService.channel.channelRef = 1;
    service['addDeviceDetails'](bet);
    expect(bet.betslip.clientUserAgent).toBe('testId');
    expect(bet.betslip.slipPlacement.channelRef).toBe(1);
  });

  it('extendWithDetails', () => {
    service['extendArray'] = jasmine.createSpy();
    service['extendBet'] = jasmine.createSpy();

    const bet: any = { requests: [] };
    service['extendWithDetails'](bet);
    expect(service['extendBet']).toHaveBeenCalledWith(bet);

    bet.requests.push({});
    service['extendWithDetails'](bet);
    expect(service['extendArray']).toHaveBeenCalledWith(bet.requests);
  });

  it('extendArray', () => {
    const bets: any[] = [{}, {}, {}];
    service['extendBet'] = jasmine.createSpy();
    service['extendArray'](bets);
    expect(service['extendBet']).toHaveBeenCalledTimes(3);
  });

  it('extendBet', () => {
    service['addUserDetails'] = jasmine.createSpy();
    service['addDeviceDetails'] = jasmine.createSpy();
    const bet: any = {};
    service['extendBet'](bet);
    expect(service['addUserDetails']).toHaveBeenCalledWith(bet);
    expect(service['addDeviceDetails']).toHaveBeenCalledWith(bet);
  });
});
