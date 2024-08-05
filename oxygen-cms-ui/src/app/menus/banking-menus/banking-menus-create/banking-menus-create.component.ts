import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { BankingMenu } from '../../../client/private/models/bankingmenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './banking-menus-create.component.html',
  styleUrls: ['./banking-menus-create.component.scss']
})
export class BankingMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public bankingMenu: BankingMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.bankingMenu = {
      id: '',
      brand: this.brandService.brand,
      collectionType: '',
      createdAt: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      disabled: false,
      heightMedium: 0,
      heightSmall: 0,
      iconAligment: 'left',
      inApp: true,
      lang: '',
      linkTitle: '',
      subHeader: '',
      linkTitle_brand: '',
      menuItemView: 'description',
      path: '',
      section: 'top',
      showItemFor: 'both',
      sortOrder: 0,
      spriteClass: '',
      targetUri: '',
      type: 'link',
      updatedAt: '',
      updatedBy: '',
      uriMedium: '',
      uriSmall: '',
      widthMedium: 0,
      widthSmall: 0,
      showOnlyOnIOS: false,
      showOnlyOnAndroid: false,
      heightLarge: 0,
      widthLarge: 0,
      svg: '',
      svgId: '',
      qa: '',
      uriLarge: '',
      authRequired: false,
      systemID: null,
      filename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      svgFilename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      startUrl: ''
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
      qa: new FormControl('', [Validators.required])
    });
  }

  getBankingMenu(): BankingMenu {
    const form = this.form.value;
    this.bankingMenu.linkTitle = form.linkTitle;
    this.bankingMenu.targetUri = form.targetUri;
    this.bankingMenu.qa = form.qa;
    return this.bankingMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
