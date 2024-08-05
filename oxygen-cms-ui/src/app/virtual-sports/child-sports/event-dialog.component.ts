import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'event-dialog',
  templateUrl: './event-dialog.component.html'
})
export class EventDialogComponent {
  event: string;

  constructor(
    private dialogRef: MatDialogRef<EventDialogComponent>) {
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
