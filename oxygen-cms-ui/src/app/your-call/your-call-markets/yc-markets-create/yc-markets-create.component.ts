import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { YourCallMarket } from '../../../client/private/models';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'yc-markets-create',
  templateUrl: './yc-markets-create.component.html',
  styleUrls: ['./yc-markets-create.component.scss']
})
export class YcMarketsCreateComponent implements OnInit {
  public newMarket: YourCallMarket;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService) {
  }

  ngOnInit() {
    this.newMarket = {
      id: '',
      updatedAt: '',
      createdAt: '',
      createdBy: '',
      updatedBy: '',
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',

      sortOrder: 0,
      name: '',
      lang: '',
      dsMarket: ''
    };
  }

  isValidFormData(): boolean {
    return this.newMarket.name.length > 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}

