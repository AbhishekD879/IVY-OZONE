import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { HeaderSubMenu } from '@app/client/private/models/headersubmenu.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  templateUrl: './header-sub-menus-create.component.html',
  styleUrls: ['./header-sub-menus-create.component.scss']
})
export class HeaderSubMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public headerSubMenu: HeaderSubMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
  ) { }

  ngOnInit() {
    this.headerSubMenu = {
      id: '',
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      updatedAt: '',
      updatedBy: '',

      disabled: false,
      lang: '',
      linkTitle: '',
      linkTitle_brand: '',
      sortOrder: 0,
      targetUri: '',
      inApp: true
    };

    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
    });
  }

  getHeaderMenu(): HeaderSubMenu {
    const form = this.form.value;
    this.headerSubMenu.linkTitle = form.linkTitle;
    this.headerSubMenu.targetUri = form.targetUri;
    return this.headerSubMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
