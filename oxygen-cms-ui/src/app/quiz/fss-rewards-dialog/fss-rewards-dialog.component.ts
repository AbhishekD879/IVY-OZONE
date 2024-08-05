import { Component, Inject } from "@angular/core";
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { FssRewards } from "@app/client/private/models/coins-rewards.model";

@Component({
    selector: 'fss-rewards-dialog',
    templateUrl: './fss-rewards-dialog.component.html'
  })
  export class FssRewardsDialogComponent {
    fssRewards: FssRewards = {
      value: 0,
      communicationType: '',
      siteCoreId: '',
    };
    
    constructor(
      private dialogRef: MatDialogRef<FssRewardsDialogComponent>,
      @Inject(MAT_DIALOG_DATA) public dialog: any) {
        this.dialogRef.disableClose = true;
    }
    ngOnInit(): void {
      this.fssRewards = this.dialog.data;
    }
    closeDialog() {
      this.dialogRef.close();
    }
  }