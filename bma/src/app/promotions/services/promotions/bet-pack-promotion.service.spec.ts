import { of, throwError } from 'rxjs';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { BetPackPromotionService } from './bet-pack-promotion.service';

describe('BetPackPromotionService', () => {
  let service: BetPackPromotionService;

  let bppService;
  let device;
  let localeService;
  let catchError;
  let gtmService;

  beforeEach(() => {
    localeService = {
      getString: (message: string) => message
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({}))
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };
    catchError = jasmine.createSpy('catchError');
    // throwError = jasmine.createSpy('throwError');
    //mergeMap = jasmine.createSpy('mergeMap');
    device = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true),
      channel: {
        channelRef: {
          id: '2313'
        }
      }
    };
    service = new BetPackPromotionService(
      bppService,
      device,
      localeService,
      gtmService
    );
  });
  describe('on buy betpack', () => {
    it('onBuyBetPack', fakeAsync(() => {
      service.onBuyBetPack().subscribe((data) => {
        expect(Object.keys(data).length).toBe(0);
      });
      tick();
    }));
  });

  describe('Invalid response scenarios', () => {

    it(`should catchError`, fakeAsync(() => {
      const error = 'error';
      bppService.send.and.returnValue(throwError({ type: 'error', msg: 'bs.SERVICE_ERROR' }));
      service.onBuyBetPack().subscribe(null, catchError);
      flush();
      expect(catchError).toHaveBeenCalledWith({ type: 'error', msg: 'bs.SERVICE_ERROR' });
    }));
  });

  describe('Server error scenarios', () => {
    it('getVoucherCode should throw error', () => {
      bppService.send = jasmine.createSpy().and.returnValue(of(throwError({ type: 'error', msg: 'bs.SERVICE_ERROR' })));
      service.onBuyBetPack().subscribe(
        null,
        (error) => {
          expect(error.type).toBe('error');
          expect(error.msg).toBe('bs.SERVICE_ERROR');
        }
      );
    });

    it('getVoucherCode should throw error1', () => {
      bppService.send = jasmine.createSpy().and.returnValue(of({ error: 'FAILED_TO_AWARD_TOKEN', description: { freebetFailureCode: 'freebetFailureCode' } }));

      service.onBuyBetPack().subscribe(
        (err) => {
          expect(err).toEqual({ type: 'error', msg: 'FAILED_TO_AWARD_TOKEN' })
        }

      );
    });
  });

  describe('Success scenarios', () => {
    it('onBuyBetPack should return success result', () => {
      bppService.send = jasmine.createSpy().and.returnValue(of({
        response: {
          returnStatus: {
            message: 'success'
          }
        }
      }));
      service.onBuyBetPack().subscribe((data) => {
        expect(data.type).toBe('success');
        expect(data.msg).toBe('bs.VOUCHER_SUCCESS');
      });
    });
  });

  describe('sendGTM', () => {
    it('should not append errormsg if it is not provided', () => {
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'eventAction',
        eventCategory: 'bet pack',
        eventLabel: 'eventLabel',
        promoType: `Bet Pack – 123`
      };
      service.sendGTM('eventAction', 'eventLabel', '123');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });

    it('should append errormsg if it is provided', () => {
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'eventAction',
        eventCategory: 'bet pack',
        eventLabel: 'eventLabel',
        promoType: `Bet Pack – 123`,
        errorMessage: 'errormsg',
        errorCode: 'errorCode'
      };
      service.sendGTM('eventAction', 'eventLabel', '123', 'errormsg', 'errorCode');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
    });
  });
});
