import { ElementRef } from '@angular/core';
import { TimeService } from '@core/services/time/time.service';
import { PatternRestrictDirective } from '@shared/directives/pattern-restrict.directive';

describe('PatternRestrictDirective', () => {

  let directive: PatternRestrictDirective;
  let elementRef: ElementRef;
  let time: TimeService;
  let deviceService;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        value: 10,
        getAttribute: jasmine.createSpy(),
        setAttribute: jasmine.createSpy(),
      }
    };
    time = {
      formatByPattern: jasmine.createSpy().and.returnValue('')
    } as any;
    deviceService = {
      isMobileOnly: false
    };

    directive = new PatternRestrictDirective(elementRef, time, deviceService);
  });

  it('should ini props', () => {
    expect(directive['element']).toBeTruthy();
    expect(directive['isMobileOnly']).toBe(false);
  });

  it('ngOnChanges with isToFixedChanged enable', () => {
    directive.ngModelChange.emit = jasmine.createSpy();
    directive.patternToFixed = true;
    directive.isToFixedChanged = true;
    const changes = {
      ngModel: { currentValue: 10 }
    } as any;

    directive.ngOnChanges(changes);
    expect(directive.ngModelChange.emit).toHaveBeenCalledWith('10.00');
  });

  it('ngOnChanges with isToFixedChanged disable', () => {
    directive.ngModelChange.emit = jasmine.createSpy();
    directive.patternToFixed = true;
    directive.isToFixedChanged = false;
    const changes = {
      ngModel: { currentValue: 10 }
    } as any;

    directive.ngOnChanges(changes);
    expect(directive.ngModelChange.emit).not.toHaveBeenCalled();
  });

  describe('@onBlur', () => {

    it('should set positive pattern valid value', () => {
      directive.ngModel = {
        isValid: true
      };
      directive.patternRestrict = '^\\d+$';
      directive.onBlur({target: {value: 10}} as any);
      expect(directive.ngModel).toEqual(jasmine.objectContaining({
        isPatternValid: true
      }));
    });

    it('should set negative pattern valid value', () => {
      directive.ngModel = {
        isValid: true
      };
      directive.patternRestrict = '^\\d+$';
      directive.onBlur({target: {value: 'test'}} as any);
      expect(directive.ngModel).toEqual(jasmine.objectContaining({
        isPatternValid: false
      }));
    });

    describe('should only skip blur for mobile if triggered by other directive', () => {

      beforeEach(() => {
        spyOn(directive as any, 'setValue');
      });

      it('desktop', () => {
        directive.onBlur({target: {value: 10}} as any);

        expect(directive['isBlur']).toBe(true);
        expect(directive.isToFixedChanged).toBe(true);
        expect(directive['setValue']).toHaveBeenCalled();
      });

      it('mobile, not trusted', () => {
        directive['isMobileOnly'] = true;
        directive.onBlur({target: {value: 10}} as any);

        expect(directive['setValue']).not.toHaveBeenCalled();
      });

      it('mobile, trusted', () => {
        directive['isMobileOnly'] = true;
        directive.onBlur({target: {value: 10}, isTrusted: true} as any);

        expect(directive['setValue']).toHaveBeenCalled();
      });

      it('mobile, trusted but with keyboard', () => {
        directive['isMobileOnly'] = true;
        directive['element'].dataset = {hasKeyboard: 'true'};
        directive.onBlur({target: {value: 10}, isTrusted: true} as any);

        expect(directive['setValue']).not.toHaveBeenCalled();
      });
    });
  });

  describe('setValue', () => {

    describe('value isEmpty', () => {
      beforeEach(() => {
        directive['element'] = {
          nativeElement: { value: null },
          validity: { valid: true }
        };
        directive['isValid'] = false;
      });

      it(`ngModel.isValid should be Truthy if ngModel.isRequired is equal False`, () => {
        directive.ngModel = { isValid: false, isRequired: false };

        directive['setValue']('');

        expect(directive.ngModel['isValid']).toBeTruthy();
      });


      it(`ngModel.isValid should be Truthy if ngModel nas Not property 'isRequired'`, () => {
        directive.ngModel = { isValid: false };

        directive['setValue']('');

        expect(directive.ngModel['isValid']).toBeTruthy();
      });

      it(`ngModel.isValid' should be Falthy if ngModel.isRequired is equal True`, () => {
        directive.ngModel = { isValid: true, isRequired: true };

        directive['setValue']('');

        expect(directive.ngModel['isValid']).toBeFalsy();
      });

      it('should format date value', () => {
        directive['isTypeDate'] = true;
        directive['setValue']('01-01-2020');
        expect(time.formatByPattern).toHaveBeenCalledWith(new Date('01-01-2020'), 'yyyy-MM-dd');
      });

      it('should set value', () => {
        directive.patternRestrict = '^[0-9]$';
        directive.patternValidate = true;
        directive['isBlur'] = true;
        directive['setValue'](' ');
        expect(directive['validValue']).toEqual(' ');
      });
      it('should set value too', () => {
        directive.patternRestrict = '^[0-9]$';
        directive.patternValidate = true;
        directive['isBlur'] = false;
        directive['setValue'](' ');
        expect(directive['validValue']).toEqual(' ');
      });
    });

  });

  describe('onChange', () => {
    beforeEach(() => {
      directive['element'] = {
        nativeElement: { value: null },
        validity: { valid: true }
      };
    });
    it('should set isToFixedChanged false', () => {
      directive.patternOnBlur = false;
      directive.isToFixedChanged = true;
      directive.onChange('');
      expect(directive.isToFixedChanged).toEqual(false);
    });
    it('should NOT set isToFixedChanged false', () => {
      directive.patternOnBlur = true;
      directive.isToFixedChanged = true;
      directive.onChange('');
      expect(directive.isToFixedChanged).toEqual(true);
    });
  });

  describe('ngAfterViewInit', () => {
    it('should update properties', () => {
      elementRef.nativeElement.getAttribute.and.returnValue('number');
      directive.ngAfterViewInit();
      expect(directive.isTypeNumber).toEqual(true);
    });
    it('should update element attribute', () => {
      elementRef.nativeElement.getAttribute.and.returnValue('date');
      directive.patternAdultAge = true;
      directive.ngAfterViewInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('max', '');
    });
  });

  describe('checkEqualValues', () => {
    it('should set ngModel.isValid true', () => {
      directive['isValid'] = true;
      directive.patternEqualTo = { value: 10 } as any;
      const ngModel = { value: 10 } as any;
      directive['checkEqualValues'](ngModel);
      expect(ngModel.isValid).toEqual(true);
      expect(ngModel.isEqualTo).toEqual(true);
    });
    it('should set ngModel.isValid true also', () => {
      directive['isValid'] = true;
      directive.patternNotEqualTo = { value: 20 } as any;
      const ngModel = { value: 10 } as any;
      directive['checkEqualValues'](ngModel);
      expect(ngModel.isValid).toEqual(true);
      expect(ngModel.isNotEqualTo).toEqual(true);
    });
  });

  describe('checkAdultAge', () => {
    let ngModel;
    beforeEach(() => {
      ngModel = { isValid: undefined };
      directive['isValid'] = true;
      directive.patternAdultAge = true;
    });
    it('should set true', () => {
      elementRef.nativeElement.value = '1950-01-01';
      directive['checkAdultAge'](ngModel);
      expect(ngModel.isValid).toEqual(true);
    });
    it('should set false', () => {
      elementRef.nativeElement.value = '2020-01-01';
      directive['checkAdultAge'](ngModel);
      expect(ngModel.isValid).toEqual(false);
    });
  });
});
