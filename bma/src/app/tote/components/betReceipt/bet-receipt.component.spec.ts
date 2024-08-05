import { BetReceiptComponent } from './bet-receipt.component';

describe('BetReceiptComponent', () => {
  let component: BetReceiptComponent, document, rendererService;

  beforeEach(() => {
    document = {};
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('renderer.listen')
      }
    };

    component = new BetReceiptComponent(document, rendererService);

    spyOn(component.betReceiptContinue, 'emit');
  });

  it(`#eventClickSub should be a function and initial value of function return should be undefined`, () => {
    expect(component.eventClickSub).toEqual(jasmine.any(Function));
    expect(component.eventClickSub()).toBeUndefined();
  });

  describe('ngOnInit', () => {
    it('init', () => {
      component.continue = jasmine.createSpy('continue');
      component.ngOnInit();
      expect(component.expanded).toBeFalsy();
    });

    it(`shoud not throw error if 'scrollToBetReceipt' is not defined`, () => {
      (component as any).scrollToBetReceipt = null;
      expect(() => component.ngOnInit()).not.toThrowError();
    });
  });

  it('ngOnDestroy', () => {
    component.eventClickSub = jasmine.createSpy('eventClickSub');
    component.ngOnDestroy();

    expect(component.eventClickSub).toHaveBeenCalled();
  });

  it('trackByIndex', () => {
    const result = component.trackByIndex(2);

    expect(result).toBe(2);
  });

  describe('continue', () => {
    it('betReceiptContinue is defined', () => {
      component.continue();
      expect(component.betReceiptContinue.emit).toHaveBeenCalled();
    });

    it('betReceiptContinue is not defined', () => {
      (component as any).betReceiptContinue = null;
      expect(() => component.continue()).not.toThrowError();
    });
  });

  it('closeReceiptOnOutsideClick(', () => {
    const eventMock = {
      stopPropagation: jasmine.createSpy('event.preventDefault')
    } as any;
    component.continue = jasmine.createSpy('continue');

    component['closeReceiptOnOutsideClick'](eventMock);

    expect(eventMock.stopPropagation).toHaveBeenCalled();
  });
});
