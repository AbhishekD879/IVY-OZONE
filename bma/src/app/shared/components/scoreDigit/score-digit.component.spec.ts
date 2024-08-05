import { ScoreDigitComponent } from '@shared/components/scoreDigit/score-digit.component';
import { fakeAsync, tick } from '@angular/core/testing';


describe('ScoreDigitComponent', () => {
  let component: ScoreDigitComponent;
  let device: any;
  let elementRef;

  beforeEach(() => {
    device = {

    };

    elementRef = { nativeElement: {
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((t, cb) => cb())
    }};

    component = new ScoreDigitComponent(device, elementRef);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(component['scoreDigitEl']).toBeTruthy();
  });

  it('ngOnInit', () => {
    component['device'] = {
      isAndroid: true,
      isWrapper: true
    } as any;
    component.number = 12;

    component.ngOnInit();

    expect(component.isAndroidWrapper).toBeTruthy();
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(2)).toEqual(2);
  });

  describe('ngOnChanges', () => {

    it('should do nothing for android', () => {
      component.isAndroidWrapper = true;

      component.ngOnChanges({number: {currentValue: 12}} as any);

      expect(component.digits).toBeUndefined();
    });

    it('should do nothing if first change', () => {
      component.isAndroidWrapper = false;

      component.ngOnChanges({number: {currentValue: 12, firstChange: true}} as any);

      expect(component.digits).toBeUndefined();
    });

    it('should do nothing if no value change', () => {
      component.isAndroidWrapper = false;

      component.ngOnChanges({number: {currentValue: 12, previousValue: 12}} as any);

      expect(component.digits).toBeUndefined();
    });

    it('should add listener and return static when fired', () => {
      component.isAndroidWrapper = false;

      component.ngOnChanges({number: {currentValue: 12}} as any);

      expect(component['scoreDigitEl'].addEventListener).toHaveBeenCalledWith(
        'transitionend', jasmine.any(Function), { once: true }
      );
      expect(component.showAnimatedDigit).toBe(false);
    });

    it('should set digits', fakeAsync(() => {
      component.isAndroidWrapper = false;
      component.animationDelay = 0;

      component.ngOnChanges({number: {currentValue: 12}} as any);

      tick();

      expect(component.digits.length).toEqual(2);
      expect(component.digits[0]).toEqual('1');
      expect(component.digits[1]).toEqual('2');
    }));
  });
});
