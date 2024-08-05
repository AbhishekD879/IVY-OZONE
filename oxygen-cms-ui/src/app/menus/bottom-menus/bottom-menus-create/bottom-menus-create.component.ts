import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { BottomMenu } from '../../../client/private/models/bottommenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './bottom-menus-create.component.html',
  styleUrls: ['./bottom-menus-create.component.scss']
})
export class BottomMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public bottomMenu: BottomMenu;
  public sections: Array<string> = ['help', 'quick links'];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.bottomMenu = {
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
      section: '',
      authRequired: false,
      systemID: null,
      updatedByUserName: '',
      createdByUserName: '',
      startUrl: ''
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
      section: new FormControl('', [Validators.required])
    });
  }

  onSectionChanged(): void {
    this.bottomMenu.section = this.form.value.section;
  }

  getBottomMenu(): BottomMenu {
    const form = this.form.value;
    this.bottomMenu.linkTitle = form.linkTitle;
    this.bottomMenu.targetUri = form.targetUri;
    return this.bottomMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
