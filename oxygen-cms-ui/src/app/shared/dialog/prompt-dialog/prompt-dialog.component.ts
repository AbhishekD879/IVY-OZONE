import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-prompt-dialog',
  templateUrl: './prompt-dialog.component.html',
  styleUrls: [
    '../dialog.style.scss'
  ]
})
export class PromptDialogComponent {
  constructor(
    private dialogRef: MatDialogRef<PromptDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  get isValid(): boolean {
    return !this.data.controls.some(item => item.required && !item.value);
  }
}
