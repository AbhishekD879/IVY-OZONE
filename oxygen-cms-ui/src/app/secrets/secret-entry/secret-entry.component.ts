import { Component, EventEmitter, Input, Output } from '@angular/core';
import { SecretEntry } from '@app/client/private/models/secret.model';

@Component({
  selector: 'secret-entry',
  templateUrl: './secret-entry.component.html',
  styleUrls: ['./secret-entry.component.scss']
})
export class SecretEntryComponent {
  @Output() onSecretRemove: EventEmitter<SecretEntry> = new EventEmitter<SecretEntry>();
  @Output() onSecretEdit: EventEmitter<SecretEntry> = new EventEmitter<SecretEntry>();
  @Input() secret: SecretEntry;

  editSecret(): void {
    this.onSecretEdit.emit(this.secret);
  }

  removeSecret(): void {
    this.onSecretRemove.emit(this.secret);
  }
}
