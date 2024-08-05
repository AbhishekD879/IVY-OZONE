import { Component, EventEmitter, Output } from '@angular/core';
@Component({
  selector: 'abstract-notification',
  template: ''
})
export class AbstractNotificationComponent {
  @Output() readonly hide: EventEmitter<boolean> = new EventEmitter();
  message: string;

  protected close(): void {
    this.hide.emit();
  }
}
