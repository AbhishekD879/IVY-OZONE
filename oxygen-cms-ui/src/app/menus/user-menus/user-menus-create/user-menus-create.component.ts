import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { UserMenu } from '../../../client/private/models/usermenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './user-menus-create.component.html',
  styleUrls: ['./user-menus-create.component.scss']
})
export class UserMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public userMenu: UserMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.userMenu = {
      id: '',
      updatedByUserName: '',
      createdByUserName: '',
      createdBy: '',
      createdAt: '',
      activeIfLogout: false,
      brand: this.brandService.brand,
      collectionType: '',
      disabled: false,
      heightMedium: 0,
      heightSmall: 0,
      lang: '',
      linkTitle: '',
      linkTitle_brand: '',
      path: '',
      sortOrder: 0,
      spriteClass: '',
      targetUri: '',
      updatedAt: '',
      updatedBy: '',
      uriMedium: '',
      uriSmall: '',
      widthMedium: 0,
      widthSmall: 0,
      heightLarge: 0,
      showUserMenu: '',
      widthLarge: 0,
      svg: '',
      svgId: '',
      qa: '',
      uriLarge: '',
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
      }
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
      qa: new FormControl('', [Validators.required])
    });
  }

  getUserMenu(): UserMenu {
    const form = this.form.value;
    this.userMenu.linkTitle = form.linkTitle;
    this.userMenu.targetUri = form.targetUri;
    this.userMenu.qa = form.qa;
    return this.userMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
