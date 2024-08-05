import {Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {SABChildElement} from '@app/client/private/models/SABChildElement.model';


@Component({
  selector: 'app-edit-stream-and-bet-node',
  templateUrl: './edit-stream-and-bet-node.component.html',
  styleUrls: ['./edit-stream-and-bet-node.component.scss']
})
export class EditStreamAndBetNodeComponent implements OnInit {
  public node: SABChildElement;

  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any) {
  }

  ngOnInit() {
    this.node = this.data.node;
  }

  getNewCategorySubItem(): SABChildElement {
    return this.node;
  }

  closeDialog() {
    this.dialogRef.close();
  }

}
