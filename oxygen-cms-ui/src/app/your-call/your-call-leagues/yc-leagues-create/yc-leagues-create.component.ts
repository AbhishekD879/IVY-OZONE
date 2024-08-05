import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { YourCallLeague } from '../../../client/private/models';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'yc-leagues-create',
  templateUrl: './yc-leagues-create.component.html',
  styleUrls: ['./yc-leagues-create.component.scss']
})
export class YcLeaguesCreateComponent implements OnInit {
  public newLeague: YourCallLeague;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService) {
  }

  ngOnInit() {
    this.newLeague = {
      id: '',
      updatedAt: '',
      createdAt: '',
      updatedBy: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,

      sortOrder: 0,
      name: '',
      lang: '',
      enabled: true,
      activeFor5aSide: false,
      typeId: null
    };
  }

  isValidFormData(): boolean {
    return this.newLeague.typeId && this.newLeague.name.length > 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
