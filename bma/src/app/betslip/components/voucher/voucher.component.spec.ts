import { of, throwError } from 'rxjs';

import { VoucherComponent } from './voucher.component';
import { SPORT_VOUCHER_FORM } from './voucher.constant';

describe('VoucherComponent', () => {
   let component: VoucherComponent;
   let freebetTriggerService;
   let localeService;
   let router;
   let auth;
   const mockString = 'some value';

   beforeEach(() => {
     freebetTriggerService = {
       getVoucherCode: jasmine.createSpy('getVoucherCode').and.returnValue(of({})),
       getGamingCode: jasmine.createSpy('getGamingCode').and.returnValue(of({}))
     };
     localeService = {
       getString: jasmine.createSpy('getString').and.returnValue(mockString)
     };
     router = {
       navigate: jasmine.createSpy('navigate')
     };
     auth = {
       isLoggedIn: jasmine.createSpy('isLoggedIn').and.returnValue(true)
     };

     component = new VoucherComponent(freebetTriggerService, localeService, router, auth);
   });

  it('ngOnInit isLoggedIn = true', () => {
    component.ngOnInit();
    expect(component.sportVoucherForm).toEqual(SPORT_VOUCHER_FORM);
    expect(component.sportVoucher).toBeTruthy();
    expect(localeService.getString).toHaveBeenCalled();
    expect(component.state.loading).toBeFalsy();
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('ngOnInit isLoggedIn = false', () => {
    auth.isLoggedIn = jasmine.createSpy().and.returnValue(false);
    component.ngOnInit();
    expect(localeService.getString).not.toHaveBeenCalled();
    expect(component.state.loading).toBeTruthy();
    expect(router.navigate).toHaveBeenCalled();
  });

  describe('@checkIsDisabled', () => {
     it('should return true if value of voucher form is empty', () => {
       const voucherForm = {
         value: ''
       };
       expect(component.checkIsDisabled(voucherForm)).toEqual(true);
     });

    it('should check if value of sport voucher form is valid', () => {
      const gamingFormValid = {
        value: '0184-8479-4D53-6862-5DC0-42D7',
        pattern: SPORT_VOUCHER_FORM.pattern
      };
      const gamingFormInvalid = {
        value: '0184-8479-4D53-6862-5DC0-42D',
        pattern: SPORT_VOUCHER_FORM.pattern
      };

      expect(component.checkIsDisabled(gamingFormValid)).toEqual(false);
      expect(component.checkIsDisabled(gamingFormInvalid)).toEqual(true);
    });

  });

  describe('submitVoucherForm', () => {
    it('Success', () => {
      const mouseEvent: any = {
        preventDefault: jasmine.createSpy()
      };
      component.submitVoucherForm(mouseEvent);
      expect(mouseEvent.preventDefault).toHaveBeenCalledTimes(1);
      expect(component.sportVoucherForm.isSent).toBeFalsy();
      expect(freebetTriggerService.getVoucherCode).toHaveBeenCalledTimes(1);
    });
    it('Error', () => {
      component['freebetTriggerService'].getVoucherCode = jasmine
        .createSpy('getVoucherCode')
        .and.returnValue(throwError({}));
      const mouseEvent: any = {
        preventDefault: jasmine.createSpy()
      };
      component.submitVoucherForm(mouseEvent);
      expect(mouseEvent.preventDefault).toHaveBeenCalledTimes(1);
      expect(component.sportVoucherForm.isSent).toBeFalsy();
      expect(component.sportVoucherForm.value).toEqual('');
    });
  });

  it('openPromotions', () => {
    const mouseEvent: any = {
      preventDefault: jasmine.createSpy()
    };

    component.openPromotions(mouseEvent);
    expect(mouseEvent.preventDefault).toHaveBeenCalledTimes(1);
    expect(router.navigate).toHaveBeenCalledWith(['/promotions']);
  });

  describe('checkIsDisabled', () => {
    it('should return true if value of voucher form is empty', () => {
      const voucherForm = {
        value: ''
      };

      expect(component.checkIsDisabled(voucherForm)).toEqual(true);
    });

    it('should check if value of sport voucher form is valid', () => {
      const gamingFormValid = {
        value: '0184-8479-4D53-6862-5DC0-42D7',
        pattern: SPORT_VOUCHER_FORM.pattern
      };
      const gamingFormInvalid = {
        value: '0184-8479-4D53-6862-5DC0-42D',
        pattern: SPORT_VOUCHER_FORM.pattern
      };

      expect(component.checkIsDisabled(gamingFormValid)).toEqual(false);
      expect(component.checkIsDisabled(gamingFormInvalid)).toEqual(true);
    });
  });
});
