import * as _ from 'lodash';

import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@root/app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { GamingSubMenu } from '@root/app/client/private/models/gaming-submenu.model';

@Component({
    templateUrl: './gaming-menus-create.component.html'
})
export class GamingMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public gamingSubMenu: GamingSubMenu;
  public targetWindow: Array<string> = ['NEW', 'CURRENT'];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
   ) { }

  ngOnInit() {
    this.gamingSubMenu = {
      id: '',
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      updatedAt: '',
      updatedBy: '',
      title: '',
      url: '',
      target: 'CURRENT',
      sortOrder: 0,
      externalImageId: '',
      pngFilename: '',
      isNative: true
    } as GamingSubMenu;

    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      url: new FormControl('', [Validators.required]),
      target: new FormControl('', [])
    });
  }

  getGamingSubMenu(): GamingSubMenu {
    const form = this.form.value;
    this.gamingSubMenu.title = form.title;
    this.gamingSubMenu.url = form.url;
    return this.gamingSubMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  onTargetWindowChanged(): void {
    this.gamingSubMenu.target = this.form.value.target;
  }
}
