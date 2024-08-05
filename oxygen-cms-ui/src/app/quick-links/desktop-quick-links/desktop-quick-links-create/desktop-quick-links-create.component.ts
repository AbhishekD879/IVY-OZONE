import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {DesktopQuickLink} from '../../../client/private/models/desktopquicklink.model';
import {ConfirmDialogComponent} from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './desktop-quick-links-create.component.html',
  styleUrls: ['./desktop-quick-links-create.component.scss']
})
export class DesktopQuickLinksCreateComponent implements OnInit {

  public form: FormGroup;
  public desktopQuickLink: DesktopQuickLink;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.desktopQuickLink = {
      id: '',
      brand: this.brandService.brand,
      createdBy: '',
      createdAt: '',
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      collectionType: '',
      disabled: false,
      heightMedium: 0,
      heightSmall: 0,
      lang: '',
      sortOrder: 0,
      spriteClass: '',
      target: '',
      title: '',
      uriMedium: '',
      uriSmall: '',
      widthMedium: 0,
      widthSmall: 0,
      filename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      isAtoZQuickLink: false
    };
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      target: new FormControl('', [Validators.required])
    });
  }

  getDesktopQuickLink(): DesktopQuickLink {
    const form = this.form.value;
    this.desktopQuickLink.title = form.title;
    this.desktopQuickLink.target = form.target;
    return this.desktopQuickLink;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
