import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Brand } from '../../../client/private/models';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'add-brand',
  templateUrl: './add-brand.component.html',
  styleUrls: ['./add-brand.component.scss']
})
export class AddBrandComponent implements OnInit {
  public newBrand: Brand;

  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>) {
  }

  ngOnInit(): void {
    this.newBrand = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      key: '',
      sortOrder: 0,
      brandCode: '',
      title: '',
      disabled: true,
      updatedByUserName: '',
      createdByUserName: '',
      brand: '',
      siteServerEndPoint: ''
    };
  }

  isValidBrandCode(): boolean {
    return this.newBrand.brandCode.indexOf(' ') === -1;
  }

  isValidFormData(): boolean {
    return this.newBrand.brandCode.length && this.isValidBrandCode() &&
      this.newBrand.title.length > 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
