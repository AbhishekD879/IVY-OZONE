import {Component, Inject, OnInit} from '@angular/core';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {SsoPage} from '@app/client/private/models/ssopage.model';
import {BrandService} from '@app/client/private/services/brand.service';

@Component({
  selector: 'promotions-create-dialog',
  templateUrl: './sso.create.component.html',
  styleUrls: ['./sso.create.component.scss']
})
export class SsoCreateComponent implements OnInit {
  newSsoPage: SsoPage = {
    // values will be set from from
    title: '',
    openLink: '',
    showOnIOS: false,
    showOnAndroid: false,

    // default automatically created values
    id: undefined,
    updatedBy: undefined,
    updatedAt: undefined,
    createdBy: undefined,
    createdAt: undefined,
    title_brand: undefined,
    sortOrder: undefined,
    targetIOS: undefined,
    targetAndroid: undefined,
    disabled: false,
    brand: this.brandService.brand,
    heightMedium: undefined,
    uriMedium: undefined,
    uriOriginal: undefined,
    widthMedium: undefined,
    filename: undefined,
    updatedByUserName: '',
    createdByUserName: '',
  };
  ssoData: SsoPage[];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {}

  isValidModel(): boolean {
    return this.newSsoPage.title.length > 0 &&
      this.isPageNameUniq(this.newSsoPage.title);
  }

  /**
   * group name should be unique
   * @param groupName
   */
  isPageNameUniq(ssoPageName: string): boolean {
    return this.data.ssoData.every(item => item.title.toLowerCase() !== ssoPageName.toLowerCase());
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  ngOnInit(): void {}
}
