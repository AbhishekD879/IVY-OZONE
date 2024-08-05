import {Component, forwardRef, Input} from '@angular/core';
import { NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
  provide: NG_VALUE_ACCESSOR,
  // tslint:disable-next-line
  useExisting: forwardRef(() => VipLevelsInputComponent),
  multi: true
};

@Component({
  selector: 'vip-levels-input',
  templateUrl: './vip-levels-input.component.html',
  styleUrls: ['./vip-levels-input.component.scss'],
  providers: [CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR]
})
export class VipLevelsInputComponent implements ControlValueAccessor {
  private innerValue: string = '';
  private onTouchedCallback: Function;
  private onChangeCallback: Function;
  @Input() placeholder?: string = 'Include VIP Levels';
  @Input() required?: boolean = false;

  constructor() {}

  convertToNumbers(text: string): string {
    const textToConvert = text || '';
    return textToConvert.replace(/[A-Za-z_.]*/gi, '')
      .replace(/([^\d])-/gi, '$1')
      .replace(/\s+/gi, ',')
      .replace(/,+/gi, ',')
      .replace(/-+/gi, '-')
      .replace(/(-\d+)-/gi, '$1')
      .replace(/[`~!@#$%^&*()_|+=?;:'".<>\{\}\[\]\\\/]/gi, '');
  }

  transformToNumber(event) {
    event.target.value = this.convertToNumbers(event.target.value);
  }

  get value(): string {
      return this.convertToNumbers(this.innerValue);
  }

  set value(newValue: string) {
      if (newValue !== this.innerValue) {
          this.innerValue = this.convertToNumbers(newValue);
          this.onChangeCallback(this.innerValue);
      }
  }

  isVipLevelValid(): boolean {
    const vipLevelsData = this.value || '';
    return vipLevelsData.length === 0 ||
      (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(',', ''), 10)));
  }

  removeLastComma(): void {
    if (this.value[this.value.length - 1] === ',') {
      this.value = this.value.slice(0, this.value.length - 1);
    }
  }

  onBlur(): void {
    this.removeLastComma();
    this.onTouchedCallback();
  }

  writeValue(value: string): void {
      if (value !== this.innerValue) {
          this.innerValue = value;
      }
  }

  registerOnChange(callback: Function): void {
      this.onChangeCallback = callback;
  }

  registerOnTouched(callback: Function): void {
      this.onTouchedCallback = callback;
  }
}
