import { OddsBoostPriceComponent } from './odds-boost-price.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OddsBoostPriceComponent', () => {
  let component: OddsBoostPriceComponent;
  let oddsBoostPriceService;
  let windowRefService;
  let userService;
  let pubSubService;

  beforeEach(() => {
    oddsBoostPriceService = {
      getFractionalPriceRange: jasmine.createSpy(),
      getDecimalPriceRange: jasmine.createSpy()
    };
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => cb()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    userService = {
      oddsFormat: 'frac'
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    component = new OddsBoostPriceComponent(
      oddsBoostPriceService,
      windowRefService,
      userService,
      pubSubService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component['applyAnimation'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component['applyAnimation']).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      component['cmpId'], 'show-slide-out-betslip-true', jasmine.any(Function)
    );
  });

  it('applyAnimation (fraction)', () => {
    component['getFormat'] = jasmine.createSpy().and.returnValue('frac');
    component['getFractionalPriceRange'] = jasmine.createSpy();

    component['applyAnimation']();

    expect(component['getFormat']).toHaveBeenCalled();
    expect(component['getFractionalPriceRange']).toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
      jasmine.any(Function), component.animationDelay
    );
  });

  it('applyAnimation (decimal)', () => {
    component['getFormat'] = jasmine.createSpy().and.returnValue('dec');
    component['getDecimalPriceRange'] = jasmine.createSpy();

    component['applyAnimation']();

    expect(component['getFormat']).toHaveBeenCalled();
    expect(component['getDecimalPriceRange']).toHaveBeenCalled();
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
      jasmine.any(Function), component.animationDelay
    );
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(1, 0)).toBe(0);
    expect(component.trackByIndex(2, 1)).toBe(1);
  });

  it('getFractionalPriceRange', () => {
    component.oldPrice = { num: 1, den: 3 };
    component.newPrice = { num: 3, den: 1 };

    component['getFractionalPriceRange']();
    expect(oddsBoostPriceService.getFractionalPriceRange).toHaveBeenCalledWith(
      component.oldPrice, component.newPrice
    );
  });

  it('getDecimalPriceRange', () => {
    component.oldPrice = { decimal: 1 };
    component.newPrice = { decimal: 3 };

    component['getDecimalPriceRange']();
    expect(oddsBoostPriceService.getDecimalPriceRange).toHaveBeenCalledWith(
      component.oldPrice, component.newPrice
    );
  });

  it('getFormat', () => {
    component.format = 'frac';
    expect(component['getFormat']()).toBe('frac');

    component.format = 'dec';
    expect(component['getFormat']()).toBe('dec');

    component.format = 'auto';
    expect(component['getFormat']()).toBe(userService.oddsFormat);
  });

  it('should adjust prices width after view init', () => {
    windowRefService.nativeWindow.setTimeout.and.callFake(() => {});
    component.ngAfterViewInit();

    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
      component['adjustPricesWidth'], component['animationDuration']
    );
  });

  it('should clear resize timer on destroy', () => {
    component['resizeTimer'] = 123;
    component.ngOnDestroy();

    expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(component['resizeTimer']);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['cmpId']);
  });

  it('adjustPricesWidth', () => {
    const numbersLists: any = [{
      nativeElement: {}
    }, {
      nativeElement: {
        firstElementChild: {
          firstElementChild: {
            style: {}, offsetWidth: 7
          },
          classList: { contains: () => true }
        },
        style: {}
      }
    }, {
      nativeElement: {
        firstElementChild: {
          lastElementChild: {
            style: {}, offsetWidth: 14
          },
          classList: { contains: () => false }
        },
        style: {}
      }
    }];

    component.numbersLists = numbersLists;
    component['adjustPricesWidth']();

    expect(
      numbersLists[1].nativeElement.firstElementChild.firstElementChild.style.display
    ).toBe('inline-block');
    expect(
      numbersLists[1].nativeElement.style.width
    ).toBe('7px');

    expect(
      numbersLists[2].nativeElement.firstElementChild.lastElementChild.style.display
    ).toEqual('inline-block');
    expect(
      numbersLists[2].nativeElement.style.width
    ).toBe('14px');
  });

  it('should adjust prices width when betslip is shown', () => {
    component['adjustPricesWidth'] = jasmine.createSpy('adjustPricesWidth');
    pubSubService.subscribe.and.callFake((subscriberName, command, cb) => cb());
    component['numbersLists'] = [] as any;
    component.ngOnInit();

    component['numbersLists'] = [{
      nativeElement: { offsetWidth: 0 }
    }] as any;
    component.ngOnInit();

    expect(component['adjustPricesWidth']).toHaveBeenCalledTimes(1);
  });
});
