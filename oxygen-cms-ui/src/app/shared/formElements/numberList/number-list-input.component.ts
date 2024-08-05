import { Component, forwardRef, Input } from '@angular/core';
import { NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
  provide: NG_VALUE_ACCESSOR,
  // tslint:disable-next-line
  useExisting: forwardRef(() => NumberListInputComponent),
  multi: true
};

@Component({
  selector: 'number-list-input',
  templateUrl: './number-list-input.component.html',
  providers: [CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR]
})
export class NumberListInputComponent implements ControlValueAccessor {
  @Input() placeholder: string = '';
  @Input() required: boolean = false;
  @Input() isDisabled?: boolean = false;

  private innerValue: string = '';
  private onTouchedCallback: Function;
  private onChangeCallback: Function;

  constructor() {
  }

  convertToNumbers(text: string): string {
    const textToConvert = text || '';
    return textToConvert
      .replace(/[^0-9,\s]/gi, '')
      .replace(/\s/gi, ',')
      .replace(/,+/gi, ',');
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
      const res = this.innerValue ? this.innerValue.split(',') : null;
      this.onChangeCallback(res);
    }
  }

  removeFirstLastComma(): void {
    if (this.value[this.value.length - 1] === ',') {
      this.value = this.value.slice(0, this.value.length - 1);
    }

    if (this.value[0] === ',') {
      this.value = this.value.slice(1, this.value.length);
    }
  }

  onBlur(): void {
    this.removeFirstLastComma();
    this.onTouchedCallback();
  }

  writeValue(value: string[]): void {
    const newValue: string = (value || []).join(',');
    if (newValue !== this.innerValue) {
      this.innerValue = newValue;
    }
  }

  registerOnChange(callback: Function): void {
    this.onChangeCallback = callback;
  }

  registerOnTouched(callback: Function): void {
    this.onTouchedCallback = callback;
  }
}
