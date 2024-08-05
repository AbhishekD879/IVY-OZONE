import { of as observableOf } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';

import { BetsIntegrationService } from './bets-integration.service';
import { SessionService } from '@authModule/services/session/session.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { CashoutDataProvider } from '@app/betHistory/services/cashoutDataProvider/cashout-data.provider';
import { CashOutMapService } from '@app/betHistory/services/cashOutMap/cash-out-map.service';

describe('BetsIntegrationService -', () => {
  let service: BetsIntegrationService;
  let serviceHacked: any;
  let userService;
  let sessionService: SessionService;
  let cashoutMapIndexService: CashoutMapIndexService;
  let cashoutDataProvider: CashoutDataProvider;
  let cashOutMapService: CashOutMapService;
  let route: ActivatedRoute;

  const betDetail: any = {
    cashoutStatus: 'foo',
    part: [{eventId: '123'}]
  };

  const cashoutMapItem: any = {
    id: '123',
    isSettled: 'foo'
  };

  beforeEach(() => {
    userService = {
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false),
      currency: 'USD',
      currencySymbol: '$'
    };
    sessionService = jasmine.createSpyObj(['whenProxySession']);
    cashoutMapIndexService = jasmine.createSpyObj(['event']);
    cashoutDataProvider = jasmine.createSpyObj(['getBet', 'getPlacedBets', 'getCashOutBets']);
    cashOutMapService = jasmine.createSpyObj(['createCashoutBetsMap']);
    route = jasmine.createSpyObj(['snapshot']);

    (sessionService.whenProxySession as jasmine.Spy).and.returnValue(new Promise(resolve => resolve(true)));

    service = new BetsIntegrationService(
      userService as any,
      sessionService as any,
      cashoutMapIndexService as any,
      cashoutDataProvider as any,
      cashOutMapService as any,
      route as any
    );
    serviceHacked = service as any;
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('getBetsForEvent method should ', () => {

    it('call cashoutBetsHasEvent', (done: DoneFn) => {
      spyOn(serviceHacked, 'cashoutBetsHasEvent');
      service.getBetsForEvent(123, [], [betDetail]).subscribe(() => {
        expect(serviceHacked.cashoutBetsHasEvent).toHaveBeenCalled();
        done();
      });
    });

    it('call cashoutBetsHasEvent when bets have event', (done: DoneFn) => {
      spyOn(serviceHacked, 'cashoutBetsHasEvent').and.returnValue(true);
      service.getBetsForEvent(123, [], []).subscribe(() => {
        expect(cashOutMapService.createCashoutBetsMap).toHaveBeenCalledWith([], 'USD', '$', false);
        done();
      });
    });

    it('not call cashoutBetsHasEvent when bets have no event', (done: DoneFn) => {
      spyOn(serviceHacked, 'cashoutBetsHasEvent').and.returnValue(false);
      service.getBetsForEvent(123, [], []).subscribe(() => {
        expect(cashOutMapService.createCashoutBetsMap).not.toHaveBeenCalled();
        done();
      });
    });

    it('return proper data', (done: DoneFn) => {
      const expectedResult = {cashoutIds: [cashoutMapItem], placedBets: [betDetail]};
      cashoutMapIndexService.event['123'] = [cashoutMapItem];
      spyOn(serviceHacked, 'cashoutBetsHasEvent').and.returnValue(true);

      service.getBetsForEvent(123, [], [betDetail]).subscribe((result) => {
        expect(result).toEqual(expectedResult);
        done();
      });
    });

    it('should handle retail user', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');

      userService.isInShopUser.and.returnValue(true);
      service.getBetsForEvent(123, [], betDetail).subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith({ cashoutIds: [], placedBets: [] });
    }));
  });

  describe('getPlacedBets method should ', () => {

    it('call isSport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport');

      service.getPlacedBets(123).subscribe(() => {
        expect(serviceHacked.isSport).toHaveBeenCalled();
        done();
      });
    });

    it('return null if not sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(false);

      service.getPlacedBets(123).subscribe((result) => {
        expect(result).toBe(null);
        done();
      });
    });

    it('should return null if is retail user', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');

      route.snapshot.params = {
        sport: 'football'
      };
      userService.isInShopUser.and.returnValue(true);
      service.getPlacedBets(123).subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('call getPlacedBetsWithCasOutDetails if sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(true);
      spyOn(serviceHacked, 'getPlacedBetsWithCasOutDetails').and.returnValue(observableOf([betDetail]));

      service.getPlacedBets(123).subscribe(() => {
        expect(serviceHacked.getPlacedBetsWithCasOutDetails).toHaveBeenCalledWith(123);
        done();
      });
    });

    it('return bets if sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(true);
      spyOn(serviceHacked, 'getPlacedBetsWithCasOutDetails').and.returnValue(observableOf([betDetail]));

      service.getPlacedBets(123).subscribe((result) => {
        expect(result).toEqual([betDetail]);
        done();
      });
    });
  });

  describe('getCashOutBets method should ', () => {

    it('call isSport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport');

      service.getCashOutBets().subscribe(() => {
        expect(serviceHacked.isSport).toHaveBeenCalled();
        done();
      });
    });

    it('return null if not sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(false);

      service.getCashOutBets().subscribe((result) => {
        expect(result).toBe(null);
        done();
      });
    });

    it('should return null if is retail user', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');

      route.snapshot.params = {
        sport: 'football'
      };
      userService.isInShopUser.and.returnValue(true);
      service.getCashOutBets().subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('call getCashOutBets if sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(true);
      (cashoutDataProvider.getCashOutBets as jasmine.Spy).and.returnValue(observableOf([betDetail]));

      service.getCashOutBets().subscribe(() => {
        expect(cashoutDataProvider.getCashOutBets).toHaveBeenCalled();
        done();
      });
    });

    it('return bets if sport', (done: DoneFn) => {
      spyOn(serviceHacked, 'isSport').and.returnValue(true);
      (cashoutDataProvider.getCashOutBets as jasmine.Spy).and.returnValue(observableOf([betDetail]));

      service.getCashOutBets().subscribe((result) => {
        expect(result).toEqual([betDetail]);
        done();
      });
    });
  });

  it('extendPlacedBetsWithCashOutDetails should return null if no bets', (done: DoneFn) => {
    serviceHacked.extendPlacedBetsWithCashOutDetails(null).subscribe((result) => {
      expect(result).toBe(null);
      done();
    });
  });

  it('extendPlacedBetsWithCashOutDetails should return bets', (done: DoneFn) => {
    (cashoutDataProvider.getBet as jasmine.Spy).and.returnValue(observableOf([betDetail]));

    serviceHacked.extendPlacedBetsWithCashOutDetails([betDetail]).subscribe((result) => {
      expect(result).toEqual([betDetail]);
      done();
    });
  });

  it('cashoutBetsHasEvent should return false if no bets', () => {
    expect(serviceHacked.cashoutBetsHasEvent(123, [])).toBe(false);
  });

  it('cashoutBetsHasEvent should return true if bets have events', () => {
    expect(serviceHacked.cashoutBetsHasEvent(123, [betDetail])).toBe(true);
  });

  it('getPlacedBetsWithCasOutDetails should call getPlacedBets', (done: DoneFn) => {
    (cashoutDataProvider.getPlacedBets as jasmine.Spy).and.returnValue(observableOf([]));

    serviceHacked.getPlacedBetsWithCasOutDetails(123).subscribe(() => {
      expect(cashoutDataProvider.getPlacedBets).toHaveBeenCalled();
      done();
    });
  });

  it('getPlacedBetsWithCasOutDetails should call extendPlacedBetsWithCashOutDetails', (done: DoneFn) => {
    (cashoutDataProvider.getPlacedBets as jasmine.Spy).and.returnValue(observableOf([]));
    spyOn(serviceHacked, 'extendPlacedBetsWithCashOutDetails').and.returnValue(observableOf([]));

    serviceHacked.getPlacedBetsWithCasOutDetails(123).subscribe(() => {
      expect(serviceHacked.extendPlacedBetsWithCashOutDetails).toHaveBeenCalled();
      done();
    });
  });

  it('isSport method should return false if HR or GH', () => {
    route.snapshot.params = {sport: 'horseracing'};

    expect(serviceHacked.isSport()).toBe(false);
  });

  it('isSport method should return true if nor HR neither GH', () => {
    route.snapshot.params = {sport: 'football'};

    expect(serviceHacked.isSport()).toBe(true);
  });
});
