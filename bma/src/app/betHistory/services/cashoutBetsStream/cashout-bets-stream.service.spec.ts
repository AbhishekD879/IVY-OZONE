import { fakeAsync, tick } from '@angular/core/testing';
import { CashoutBetsStreamService } from '@app/betHistory/services/cashoutBetsStream/cashout-bets-stream.service';
import { of as observableOf, throwError, Observable, Subject } from 'rxjs';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('CashoutBetsStreamService', () => {
  let service: CashoutBetsStreamService;
  let bppService,
    cashoutDataProvider,
    cashoutWsConnectorService,
    awsService,
    cashOutLiveServeUpdatesService;

  beforeEach(() => {
    bppService = {
      showErrorPopup: jasmine.createSpy('showErrorPopup'),
    };
    cashoutDataProvider = {
      getCashOutBets: jasmine.createSpy('cashoutDataProvider'),
      getBet: jasmine.createSpy('getBet'),
    };
    cashoutWsConnectorService = {
      updateBet: jasmine.createSpy('updateBet'),
      closeStream: jasmine.createSpy('closeStream'),
      streamBetDetails: jasmine.createSpy('streamBetdetails').and.returnValue(observableOf([])),
    };
    awsService = jasmine.createSpyObj('awsService', ['addAction']);
    cashOutLiveServeUpdatesService = jasmine.createSpyObj('cashOutLiveServeUpdatesService', ['updateBetDetails']);

    service = new CashoutBetsStreamService(
      bppService,
      cashoutDataProvider,
      cashoutWsConnectorService,
      awsService,
      cashOutLiveServeUpdatesService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getCashoutBets', () => {
    let spy1, spy2;
    beforeEach(() => {
      spy1 = jasmine.createSpy('spy1');
      spy2 = jasmine.createSpy('spy2');
    });

    it('should return existing observable', () => {
      const observable = Symbol('observable');
      service.cashoutBetsObservable = observable as any;
      expect(service.getCashoutBets()).toEqual(observable as any);
      expect(cashoutWsConnectorService.streamBetDetails).not.toHaveBeenCalled();
    });

    it('should handle error of cashout WS', fakeAsync(() => {
      cashoutWsConnectorService.streamBetDetails.and.returnValue(throwError('error'));
      const result = service.getCashoutBets();

      expect(service.cashoutBetsObservable).toEqual(result);
      result.subscribe(spy1, spy2);

      tick();
      expect(cashoutWsConnectorService.streamBetDetails).toHaveBeenCalled();
      expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
      expect(awsService.addAction).toHaveBeenCalled();
      expect(spy1).not.toHaveBeenCalled();
      expect(spy2).toHaveBeenCalledWith('error');
      expect(service.cashoutBetsObservable).toEqual(null);
    }));

    it('should handle success response of cashout bets WS', fakeAsync(() => {
      const betsMock = [{ betId: 'wew' }] as IBetDetail[];
      cashoutWsConnectorService.streamBetDetails.and.returnValue(observableOf(betsMock));
      const result = service.getCashoutBets();

      expect(service.cashoutBetsObservable).toEqual(result);
      result.subscribe(spy1, spy2);

      tick();
      expect(cashoutWsConnectorService.streamBetDetails).toHaveBeenCalled();
      expect(spy1).toHaveBeenCalledWith([{ betId: 'wew' }] as any);
      expect(spy2).not.toHaveBeenCalled();
      expect(service.cashoutBetsObservable).toEqual(null);
    }));

    it('should replay late subscription to cashout bets WS', fakeAsync(() => {
      const subject = new Subject();
      const betsMock = [{ betId: 'wew' }] as IBetDetail[];
      cashoutWsConnectorService.streamBetDetails.and.returnValue(subject);
      const result = service.getCashoutBets();
      result.subscribe(spy1);
      subject.next(betsMock);
      tick();
      expect(spy1).toHaveBeenCalledWith([{ betId: 'wew' }] as any);
      expect(service.cashoutBetsObservable).toEqual(result);
      subject.complete();
      result.subscribe(spy2);
      tick();
      expect(spy2).toHaveBeenCalledWith([{ betId: 'wew' }] as any);
      expect(service.cashoutBetsObservable).toEqual(null);
    }));
  });

  describe('getCashoutBet', () => {
    const idArray = ['111', '222'];
    const betsMock = [{ betId: '123' }] as IBetDetail[];
    let spy1, spy2;
    beforeEach(() => {
      spy1 = jasmine.createSpy('spy1');
      spy2 = jasmine.createSpy('spy2');
    });

    describe('should handle error of', () => {
      let error = null;

      it('should handle error of cashout data provider', fakeAsync(() => {
        error = 'error';
        cashoutDataProvider.getBet.and.returnValue(throwError(error));

        const result = service.getCashoutBet(idArray);
        result.subscribe(spy1, spy2);
        tick();
        expect(cashoutDataProvider.getBet).toHaveBeenCalledWith(idArray, false, false);
        expect(bppService.showErrorPopup).toHaveBeenCalledWith('cashOutError');
      }));

      afterEach(() => {
        expect(awsService.addAction).toHaveBeenCalledWith('cashout=>getCashoutBet=>error', { error });
        expect(spy1).not.toHaveBeenCalled();
        expect(spy2).toHaveBeenCalledWith(error);
      });
    });

    describe('should handle success of cashout WS', () => {
      let data, updateBetDetails;

      beforeEach(() => {
        updateBetDetails = false;
      });

      it('with bet data', () => {
        data = betsMock;
        updateBetDetails = true;
        spyOn(Date, 'now').and.returnValue(1234567890);
      });

      describe('with empty response', () => {
        it('[]', () => data = []);
        it('null', () => data = null);
      });

      afterEach(fakeAsync(() => {
        cashoutDataProvider.getBet.and.returnValue(observableOf(data));
        const result = service.getCashoutBet(idArray, true);
        result.subscribe(spy1, spy2);
        tick();
        if (updateBetDetails) {
          expect(cashOutLiveServeUpdatesService.updateBetDetails).toHaveBeenCalledWith(betsMock[0], 1234567890, null, true);
        } else {
          expect(cashOutLiveServeUpdatesService.updateBetDetails).not.toHaveBeenCalled();
        }
        expect(cashoutDataProvider.getBet).toHaveBeenCalledWith(idArray, true, false);
        expect(spy1).toHaveBeenCalledWith(data);
        expect(spy2).not.toHaveBeenCalled();
      }));
    });
  });

  it('closeBetsStream', () => {
    service.closeBetsStream();
    expect(cashoutWsConnectorService.closeStream).toHaveBeenCalled();
  });

  describe('openBetsStream', () => {
    it('should call streamBetDetails', () => {
      const result = Symbol('observable');
      cashoutWsConnectorService.streamBetDetails.and.returnValue(result);

      expect(service.openBetsStream()).toEqual(result as any);
      expect(cashoutWsConnectorService.streamBetDetails).toHaveBeenCalled();
    });
  });

  describe('updateCashedOutBet', () => {
    it('should emit WS updateBet message', () => {
      service.updateCashedOutBet({ betId: '123' } as any);
      expect(cashoutWsConnectorService.updateBet).toHaveBeenCalledWith({ betId: '123' });
    });
  });

  describe('#clearCashoutBetsObservable', () => {
    it('should clear cashoutBetsObservable', () => {
      service.cashoutBetsObservable = new Observable();

      service.clearCashoutBetsObservable();

      expect(service.cashoutBetsObservable).toBeNull();
    });
  });
});
