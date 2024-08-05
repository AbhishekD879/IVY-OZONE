import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-event-hub-create',
  templateUrl: './event-hub-create.component.html',
  styleUrls: ['./event-hub-create.component.scss']
})
export class EventHubCreateComponent implements OnInit {
  newEventHub: IEventHub;
  title: FormControl;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.title = new FormControl('', [Validators.required]);

    this.newEventHub = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedBy: null,
      updatedAt: null,
      updatedByUserName: null,
      createdByUserName: null,

      brand: this.brandService.brand,
      title: '',
      indexNumber: this.data.data.index,
      disabled: false
    };
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }
}
