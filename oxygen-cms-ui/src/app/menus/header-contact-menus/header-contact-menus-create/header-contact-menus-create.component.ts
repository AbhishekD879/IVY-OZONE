import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { HeaderContactMenu} from '../../../client/private/models/headercontactmenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './header-contact-menus-create.component.html',
  styleUrls: ['./header-contact-menus-create.component.scss']
})
export class HeaderContactMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public headerContactMenu: HeaderContactMenu;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.headerContactMenu = {
      id: '',
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      disabled: false,
      inApp: true,
      lang: '',
      linkTitle: '',
      linkTitleBrand: '',
      sortOrder: 0,
      targetUri: '',
      updatedAt: '',
      updatedBy: '',
      label: '',
      authRequired: false,
      systemID: null,
      updatedByUserName: '',
      createdByUserName: '',
      startUrl: ''
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required])
    });
  }

  getHeaderContactMenu(): HeaderContactMenu {
    const form = this.form.value;
    this.headerContactMenu.linkTitle = form.linkTitle;
    this.headerContactMenu.targetUri = form.targetUri;
    return this.headerContactMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
