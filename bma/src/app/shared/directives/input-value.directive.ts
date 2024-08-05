import { Directive, EventEmitter, ElementRef, HostListener, Output } from '@angular/core';

@Directive({
  // eslint-disable-next-line
  selector: 'input[input-value]',
  // Hack to handle live $event change
  /* eslint-disable */
  host: {
    '(input)': 'onChange($event)'
  }
})

export class InputValueDirective {
  @Output() readonly errorBlockChange: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() readonly fieldValueChange: EventEmitter<number> = new EventEmitter<number>();

  private element: { value: number };

  constructor(private elementRef: ElementRef) {
    this.element = this.elementRef.nativeElement;
  }

  @HostListener('change', ['$event'])
  onChange($event: any): void {
    const event: number = $event && $event.target.value;
    this.errorBlockChange.emit(false);
    this.fieldValueChange.emit(event);
    if (!event) {
      this.element.value = null;
    }
  }
}
