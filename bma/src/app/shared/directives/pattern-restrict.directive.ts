import * as _ from 'underscore';
import {
  Directive, EventEmitter, ElementRef, HostListener, AfterViewInit, Input, Output, OnChanges, SimpleChanges
} from '@angular/core';

import { TimeService } from '@core/services/time/time.service';
import { DeviceService } from '@core/services/device/device.service';

@Directive({
  // eslint-disable-next-line
  selector: 'input[patternRestrict]',
  // Hack to handle live $event change
  /* eslint-disable */
  host: {
    '(input)': 'onChange($event.target.value)'
  }
})

export class PatternRestrictDirective implements AfterViewInit, OnChanges {
  @Input() patternRestrict: string;
  @Input() patternToFixed: boolean = false;
  @Input() patternOnBlur: boolean = false;
  @Input() patternValidate: boolean = false;
  @Input() patternAdultAge: boolean = false;
  @Input() patternEqualTo: { value: string, isValid: boolean };
  @Input() patternNotEqualTo: { value: string, isValid: boolean };
  @Input() ngModel: {};
  @Input() isToFixedChanged: boolean = false;
  @Output() readonly ngModelChange: EventEmitter<{}> = new EventEmitter<{}>();

  isTypeNumber: boolean = false;

  private element: any;
  private isTypeDate: boolean = false;
  private isTouched: boolean = false;
  private isValid: boolean = false;
  private isBlur: boolean = false;
  private validValue: number | string | null = null;
  private isMobileOnly: boolean;

  constructor(
    private elementRef: ElementRef,
    private time: TimeService,
    private deviceService: DeviceService
  ) {
    this.element = this.elementRef.nativeElement;
    this.isMobileOnly = this.deviceService.isMobileOnly;
  }

  @HostListener('change', ['$event.target.value']) onChange(value: number | string | null): void {
    if (!this.patternOnBlur) {
      this.isToFixedChanged = false;
      this.setValue(value);
    }
  }

  @HostListener('blur', ['$event']) onBlur(event: Event): void {
    // skip blur events triggered by DigitKeyboardInputDirective (implicit check: has special hasKeyboard attr OR event triggered by script)
    if (this.isMobileOnly && ((this.element.dataset && this.element.dataset.hasKeyboard !== undefined) || !event.isTrusted)) { return; }

    const value = (event.target as any).value;
    this.isBlur = true;
    this.isToFixedChanged = true;
    this.setValue(value, value !== '');
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.ngModel && this.patternToFixed) {
      this.setValue(changes.ngModel.currentValue, this.isToFixedChanged);
    }
  }

  ngAfterViewInit(): void {
    this.isTypeNumber = this.element.getAttribute('type') === 'number';
    this.isTypeDate = this.element.getAttribute('type') === 'date';

    if (this.isTypeDate && this.patternAdultAge) {
      this.element.setAttribute('max', this.time.formatByPattern(this.getAdultYear(), 'yyyy-MM-dd'));
    }
  }

  private setValue(value: any, emitChange: boolean = true): void {
    if (this.isTypeDate) {
      value = value && this.time.formatByPattern(new Date(value), 'yyyy-MM-dd');
    }
    const regexpPattern: RegExp = new RegExp(this.patternRestrict, 'g');
    const isValid: boolean = value && regexpPattern.test(value);
    const isEmpty: boolean = !value && this.element.validity.valid;
    if (!isEmpty && !isValid && !this.patternValidate) {
      this.element.value = null;
      this.element.value = this.validValue;
      this.isTouched = true;
    } else if (isEmpty) {
      this.element.value = null;
      this.validValue = null;
      this.isValid = _.has(this.ngModel, 'isRequired')
        ? !this.ngModel['isRequired']
        : true;
      this.isTouched = true;
    } else if (isValid) {
      this.validValue = value;
      this.isValid = true;
      this.isTouched = true;
      this.isBlur = true;
    } else {
      this.element.value = value;
      this.validValue = value;
      this.isValid = isValid;
      this.isTouched = this.isBlur ? true : this.isInputLength(value);
    }

    this.setNgModel(emitChange);
  }

  private setNgModel(emitChange: boolean): void {
    let value;

    if (_.has(this.ngModel, 'isValid')) {
      const ngModel = {
        value: this.element.value,
        isTouched: this.isTouched,
        isValid: this.isValid,
        isPatternValid: this.isValid
      };

      this.checkEqualValues(ngModel);
      this.checkAdultAge(ngModel);

      this.ngModel = _.extend(this.ngModel, ngModel);

      value = this.ngModel;
    } else {
      value = this.element.value;
    }

    if (emitChange) {
      if (this.patternToFixed && this.validValue && this.isToFixedChanged) {
        value = this.convertValue(this.validValue);
      }
      this.ngModelChange.emit(value);
    }
  }

  private checkEqualValues(ngModel: any): void  {
    if (this.patternEqualTo && this.isValid && this.patternEqualTo.value) {
      const isEqual = this.element.value === this.patternEqualTo.value;
      ngModel.isEqualTo = isEqual;
      ngModel.isValid = isEqual;
      const ngCompareModel = {
        isEqualTo: isEqual,
        isValid: isEqual
      };
      this.patternEqualTo = _.extend(this.patternEqualTo, ngCompareModel);
      this.ngModelChange.emit(this.patternEqualTo);
    }
    if (this.patternNotEqualTo && this.isValid && this.patternNotEqualTo.value) {
      const isEqual = this.element.value !== this.patternNotEqualTo.value;
      ngModel.isNotEqualTo = isEqual;
      ngModel.isValid = isEqual;
      const ngCompareModel = {
        isNotEqualTo: isEqual,
        isValid: isEqual
      };
      this.patternNotEqualTo = _.extend(this.patternNotEqualTo, ngCompareModel);
      this.ngModelChange.emit(this.patternNotEqualTo);
    }
  }

  private checkAdultAge(ngModel: { isValid: boolean }): void  {
    if (this.isValid && this.patternAdultAge) {
      ngModel.isValid = this.isValidAdultAge(this.element.value);
    }
  }

  private isInputLength(value: string): boolean {
    const matchPattern: RegExp = new RegExp('{(\\d+),', 'g');
    const matchArray: Array<string> = this.patternRestrict && this.patternRestrict.match(matchPattern);
    const matchString: string = matchArray && matchArray[0];
    const matchNumber: number = matchString && Number(matchString.replace(/[^0-9.]/g, ''));
    return this.patternRestrict && matchNumber && (value.length > matchNumber);
  }

  /**
   * Convert & filter input value (Ex: 24a$!c --> 24.00)
   */
  private convertValue(val: number | string): number | string {
    const value: number = Number(val.toString().replace(/[^0-9.]/g, ''));
    return value ? value.toFixed(2) : null;
  }

  /**
   * Returns adult year
   */
  private getAdultYear(): Date {
    return new Date(new Date().getFullYear() - 18, new Date().getMonth(), new Date().getDate());
  }

  /**
   * Check Adult Age
   */
  private isValidAdultAge(value: Date): boolean {
    const birthDate: Date = new Date(value);
    const adultAge: number = birthDate.setDate(birthDate.getDate() - 1);
    const adultYear: number = this.getAdultYear().getTime();
    return adultYear > adultAge;
  }
}
