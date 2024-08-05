import { Component, OnInit } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';

import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-coupon-market-mapping-create',
  templateUrl: './coupon-market-mapping-create.component.html',
  styleUrls: ['./coupon-market-mapping-create.component.scss']
})
export class CouponMarketMappingCreateComponent implements OnInit {

  public couponMarketMapping: any;
  public form: FormGroup;
  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    // private apiClientService: ApiClientService,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.couponMarketMapping = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      couponId: '',
      marketName: '',
      sortOrder: 0
    };
    this.form = new FormGroup({
      couponId: new FormControl('', [Validators.required]),
      marketName: new FormControl('', [Validators.required])
    });
  }

  getCouponMarket(): any {
    const form = this.form.value;
    this.couponMarketMapping.couponId= form.couponId;
    this.couponMarketMapping.marketName = form.marketName;
    return this.couponMarketMapping;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isMarketSelectorValid(): boolean{
    return this.form.valid;
  }
}
