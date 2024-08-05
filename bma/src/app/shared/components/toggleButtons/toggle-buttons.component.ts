import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'toggle-buttons',
  templateUrl: 'toggle-buttons.component.html'
})
export class ToggleButtonsComponent {
  @Input() buttons: { val: string; label: string; }[];
  @Input() selectedBtn: string;
  @Input() hideCheckIcons?: boolean;
  @Output() readonly toggleData: EventEmitter<string> = new EventEmitter<string>();


  /**
   * On button toggle - change selected value and
   * invoke delegated function
   */
  toggleBtnOnClick(btnVal: string): void {
    this.selectedBtn = btnVal;
    this.toggleData.emit(btnVal);
  }

  trackByIndex(index): number {
    return index;
  }
}
