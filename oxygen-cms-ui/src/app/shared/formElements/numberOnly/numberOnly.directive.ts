import { Directive, ElementRef, forwardRef, HostListener } from '@angular/core';
import { NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
  provide: NG_VALUE_ACCESSOR,
  // tslint:disable-next-line
  useExisting: forwardRef(() => NumberOnlyDirective),
  multi: true
};

@Directive({
  selector: 'input[appNumberOnly]',
  providers: [CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR]
})
export class NumberOnlyDirective implements ControlValueAccessor {
  private innerValue: string = '';
  private onTouchedCallback: Function;
  private onChangeCallback: Function;

  constructor(private el: ElementRef) {
  }

  @HostListener('input')
  onInput() {
    this.innerValue = this.transformToNumberString(this.el.nativeElement.value);
    this.writeValue(this.innerValue);
    this.onChangeCallback(this.innerValue);
  }

  @HostListener('blur')
  onBlur(): void {
    this.onTouchedCallback();
  }

  transformToNumberString(text: string): string {
    return text.replace(/\D/gi, '');
  }

  writeValue(value: number | string): void {
    const newValue = value && value !== 0 ? value.toString() : '';
    this.innerValue = newValue;
    this.el.nativeElement.value = this.innerValue;
  }

  registerOnChange(callback: Function): void {
    this.onChangeCallback = callback;
  }

  registerOnTouched(callback: Function): void {
    this.onTouchedCallback = callback;
  }
}
