import {
  Component,
  ElementRef,
  EventEmitter, HostListener,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  ViewChild
} from '@angular/core';
import { COMMA, ENTER, SPACE } from '@angular/cdk/keycodes';
import { MatAutocomplete, MatAutocompleteTrigger } from '@angular/material/autocomplete';

@Component({
  selector: 'inline-multiselect',
  templateUrl: './inline-multiselect.component.html',
  styleUrls: ['./inline-multiselect.component.scss']
})
export class InlineMultiselectComponent implements OnChanges {
  @Input() disabled: boolean;
  @Input() options: Array<string | number> = [];
  @Input() values: Array<string | number> = [];
  @Input() pattern: RegExp;
  @Input() unique: boolean;
  @Input() ordered: boolean;
  @Input() templateName: string = '';
  @Input() validationMessage: string = 'Invalid value';
  @Input() required: boolean = false;
  @Input() placeholder: string = 'Enter values';
  @Output() readonly update: EventEmitter<Array<string | number>> = new EventEmitter<Array<string | number>>();

  @ViewChild('valuesInput', { read: ElementRef }) valuesInputElement: ElementRef<HTMLInputElement>;
  @ViewChild('valuesInput', { read: MatAutocompleteTrigger }) valueAutocompleteTrigger: MatAutocompleteTrigger;
  @ViewChild('autocomplete') valueAutocomplete: MatAutocomplete;

  readonly duplicateValueMessage: string = 'Value already entered';
  readonly requiredValueMessage: string = 'Value should be entered';
  errorMessage: string = '';
  separatorKeysCodes: number[] = [ENTER, COMMA, SPACE];
  optionsList: Array<string | number>;

  @HostListener('click', ['$event.target'])
  openPanel(target: HTMLElement): void {
    if (target === this.valuesInputElement.nativeElement) {
      this.valueAutocompleteTrigger.openPanel();
    }
  }

  @HostListener('focusout', ['$event.target'])
  clearInput(target: HTMLElement): void {
    if (target === this.valuesInputElement.nativeElement) {
      this.errorMessage = this.validateRequired();
      (target as HTMLInputElement).value = '';
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.options || changes.values || changes.unique) {
      if (!this.values) { this.values = []; }
      if (!this.options) { this.options = []; }
      this.filterOptions();
    }
  }

  removeItem(index: number): void {
    this.values.splice(index, 1);
    this.updateValues();
    window.requestAnimationFrame(() => this.valuesInputElement.nativeElement.focus());
  }

  filterOptions(): void {
    this.optionsList = this.options.filter((option: string | number) =>
      this.unique ? this.values.every((val: string | number) => String(val) !== String(option)) : true);
  }

  addItem(value: string): void {
    this.errorMessage = this.validateValue(value);
    this.valuesInputElement.nativeElement.value = '';

    if (!this.errorMessage) {
      this.values.push(value);
      this.ordered && this.values.sort(InlineMultiselectComponent.orderValues);
      this.updateValues();
      window.requestAnimationFrame(() => this.valueAutocompleteTrigger.openPanel());
    } else {
      this.valueAutocompleteTrigger.closePanel();
    }
  }

  private validateValue(value: string): string {
    switch (true) {
      case !value:
      case !value.trim():
      case this.pattern && !this.pattern.test(value):
        return this.validationMessage;
      case this.unique && this.values.some((val: string | number) => String(val) === String(value)):
        return this.duplicateValueMessage;
      default: return '';
    }
  }

  private validateRequired(): string {
    return this.required && this.values.length === 0 ? this.requiredValueMessage : '';
  }

  private updateValues(): void {
    this.filterOptions();
    this.update.emit(this.values);
  }

  static orderValues(a, b) {
    const aN = Number(a), bN = Number(b);
    return !isNaN(aN) && !isNaN(bN) ? aN - bN :
      !isNaN(aN) && isNaN(bN) ? -1 :
        isNaN(aN) && !isNaN(bN) ? 1 :
          a < b ? -1 : 1;
  }
}

