import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { of } from 'rxjs';

describe('PriceOddsButtonAnimationService', () => {
  let service: PriceOddsButtonAnimationService,
      windowRef,
      betSlipSelectionsData,
      cmsService,
      deviceService,
      storageService,
      domToolsService,
      renderService,
      eventArg,
      querySelector = true;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        pageYOffset: 0,
        scrollY: 0
      },
      pubsub: {},
      command: {},
      document: {}
    };

    betSlipSelectionsData = {
      count: () => 0
    };

    cmsService = {
      getSystemConfig: (arg1, arg2) => {
        return of({
          Betslip: {
            maxBetNumber: 1
          }
        });
      }
    };

    deviceService = {
      isMobileOrigin: true
    };

    storageService = {
      get: (arg) => false
    };

    domToolsService = {
      getOffset: (arg) => 1,
      css: (arg1, arg2) => {}
    };

    renderService = {
      renderer: {
        addClass: (arg1, arg2) => {},
        removeClass: (arg1, arg2) => {},
        removeAttribute: (arg1, arg2) => {},
      }
    };

    eventArg = {
      currentTarget: {
        classList: {
          contains: () => false
        }
      }
    };

    spyOn(document, 'querySelector').and.callFake(() => querySelector);
    createService();
  });

  const createService = () => {
    service = new PriceOddsButtonAnimationService(
      windowRef,
      betSlipSelectionsData,
      cmsService,
      deviceService,
      storageService,
      domToolsService,
      renderService
    );
  };

  it('should be call resetAnimation when all conditions are true', () => {
    spyOn(window as any, 'setTimeout').and.callFake((fn) => {
      return fn && fn();
    });
    spyOn(service, 'resetAnimation').and.callThrough();
    service.animate(eventArg);
    expect(service.resetAnimation).toHaveBeenCalled();
  });

  it('should not call resetAnimation when deviceService.isMobileOrigin equal false', () => {
    deviceService = {
      isMobileOrigin: false
    };
    createService();
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when animatedElement equal null', () => {
    querySelector = false;
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when currentTarget equal null', () => {
    eventArg = {
      currentTarget: null
    };
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when currentTarget classList contain active class', () => {
    eventArg.currentTarget = {
      classList: {
        contains: (arg) => true
      }
    };
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when currentTarget classList equal animatedClass property ', () => {
    document.querySelector = jasmine.createSpy('HTML Element').and.returnValue('');
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when betSlipSelectionsData count equal maxBetsAmount', () => {
    betSlipSelectionsData.count = () => 1;
    createService();
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when overaskIsInProcess equal true', () => {
    storageService.get = (arg) => true;
    createService();
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });

  it('should not call resetAnimation when getOffset equal 0', () => {
    domToolsService.getOffset = (arg) => 0;
    createService();
    spyOn(service, 'resetAnimation');
    service.animate(eventArg);
    expect(service.resetAnimation).not.toHaveBeenCalled();
  });
});
