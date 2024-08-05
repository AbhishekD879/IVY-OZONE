import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { RightMenu } from '../../../client/private/models/rightmenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './right-menus-create.component.html',
  styleUrls: ['./right-menus-create.component.scss']
})
export class RightMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public rightMenu: RightMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.rightMenu = {
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

  getRightMenu(): RightMenu {
    const form = this.form.value;
    this.rightMenu.linkTitle = form.linkTitle;
    this.rightMenu.targetUri = form.targetUri;
    this.rightMenu.qa = form.qa;
    return this.rightMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
