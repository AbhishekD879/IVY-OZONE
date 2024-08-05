import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { FooterMenu } from '../../../client/private/models/footermenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './footer-menus-create.component.html',
  styleUrls: ['./footer-menus-create.component.scss']
})
export class FooterMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public footerMenu: FooterMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.footerMenu = {
      id: '',
      brand: this.brandService.brand,
      updatedAt: '',
      updatedBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      createdBy: '',
      createdAt: '',

      desktop: false,
      disabled: false,
      heightMedium: 0,
      heightSmall: 0,
      imageTitle: '',
      imageTitle_brand: '',
      inApp: true,
      lang: '',
      linkTitle: '',
      linkTitle_brand: '',
      mobile: false,
      path: '',
      showItemFor: '',
      sortOrder: null,
      spriteClass: '',
      svg: '',
      svgId: '',
      tablet: false,
      targetUri: '',
      uriMedium: '',
      uriSmall: '',
      widthMedium: 0,
      widthSmall: 0,
      collectionType: '',
      itemType: '',
      heightLarge: 0,
      widthLarge: 0,
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
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      inclusionList: [],
      exclusionList: [],
      universalSegment: true
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [])
    });
  }

  getFooterMenu(): FooterMenu {
    const form = this.form.value;
    this.footerMenu.linkTitle = form.linkTitle;
    this.footerMenu.targetUri = form.targetUri;
    return this.footerMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
