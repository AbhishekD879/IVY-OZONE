import { from as observableFrom, throwError } from 'rxjs';
import { FreebetTriggerService } from './freebet-trigger.service';

describe('FreebetTriggerService', () => {

  let service: FreebetTriggerService;
  let bppService;
  let localeService;
  let deviceService;

  beforeEach(() => {
    localeService = {
      getString: (message: string) => message
    };
    deviceService = {
      channel: {
        channelRef: {
          id: '2313'
        }
      }
    };
  });

  describe('Success scenarios', () => {

    beforeEach(() => {
      bppService = {
        send: jasmine.createSpy().and.returnValue(observableFrom([{
          response: {
            returnStatus: {
              message: 'success'
            }
          }
        }]))
      };
      service = new FreebetTriggerService(bppService, deviceService, localeService);
    });

    it('getVoucherCode should return success result', () => {
      service.getVoucherCode().subscribe((data) => {
        expect(data.type).toBe('success');
        expect(data.msg).toBe('bs.VOUCHER_SUCCESS');
      });
    });
  });

  describe('Empty result scenarios', () => {

    beforeEach(() => {
      bppService = {
        send: jasmine.createSpy().and.returnValue(observableFrom([{
          response: {}
        }]))
      };
      service = new FreebetTriggerService(bppService, deviceService, localeService);
    });

    it('getVoucherCode should return empty object with default value', () => {
      service.getVoucherCode().subscribe((data) => {
        expect(Object.keys(data).length).toBe(0);
      });
    });

    it('getVoucherCode should return empty object', () => {
      service.getVoucherCode('test').subscribe((data) => {
        expect(Object.keys(data).length).toBe(0);
      });
    });
  });

  describe('Invalid response scenarios', () => {

    beforeEach(() => {
      bppService = {
        send: jasmine.createSpy().and.returnValue(observableFrom([{ error: 'VOUCHER_INVALID_LENGTH' }]))
      };
      service = new FreebetTriggerService(bppService, deviceService, localeService);
    });

    it('getVoucherCode should throw error', () => {
      service.getVoucherCode().subscribe(
        null,
        (error) => {
          expect(error.type).toBe('error');
          expect(error.msg).toBe('bs.VOUCHER_INVALID_LENGTH');
        }
      );
    });
  });

  describe('Server error scenarios', () => {

    beforeEach(() => {
      bppService = {
        send: jasmine.createSpy().and.returnValue(throwError(''))
      };
      service = new FreebetTriggerService(bppService, deviceService, localeService);
    });

    it('getVoucherCode should throw error', () => {
      service.getVoucherCode().subscribe(
        null,
        (error) => {
          expect(error.type).toBe('error');
          expect(error.msg).toBe('bs.SERVICE_ERROR');
        }
      );
    });
  });
});
