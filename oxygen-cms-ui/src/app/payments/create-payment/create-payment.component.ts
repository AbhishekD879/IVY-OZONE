import { PaymentMethod } from './../../client/private/models/paymentMethod.model';
import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../client/private/services/brand.service';

@Component({
  selector: 'app-create-payment',
  templateUrl: './create-payment.component.html',
  styleUrls: ['./create-payment.component.scss']
})
export class CreatePaymentComponent implements OnInit {

  public payment: PaymentMethod;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
  ) { }

  ngOnInit(): void {
    this.payment = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      brand: this.brandService.brand,
      active: false,
      identifier: null,
      name: '',
      sortOrder: -1,
    };
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public isValidPaymentMethod(): boolean {
    return !!this.payment.name;
  }

  public getNewPaymentMethod(): PaymentMethod {
    return this.payment;
  }
}
