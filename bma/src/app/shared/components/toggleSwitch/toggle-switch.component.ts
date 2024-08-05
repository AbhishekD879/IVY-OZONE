import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'toggle-switch',
  templateUrl: 'toggle-switch.component.html',
  styleUrls: ['./toggle-switch.component.scss']
})
export class ToggleSwitchComponent {

  @Input() componentId: string;
  @Input() initialState: boolean;
  @Input() disabled: boolean;

  @Output() readonly switcherControl: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() readonly clickIfDisabled: EventEmitter<any> = new EventEmitter<any>();

  onChange(event, value: boolean) {
    this.switcherControl && this.switcherControl.emit(value);
  }

  onClick(event) {
    if (this.disabled) {
      this.clickIfDisabled.emit(event);
    }
  }
}
