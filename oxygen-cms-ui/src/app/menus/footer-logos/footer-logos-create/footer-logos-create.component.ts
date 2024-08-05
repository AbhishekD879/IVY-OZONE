import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { FooterLogo } from '../../../client/private/models/footerlogo.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './footer-logos-create.component.html',
  styleUrls: ['./footer-logos-create.component.scss']
})
export class FooterLogosCreateComponent implements OnInit {

  public form: FormGroup;
  public footerLogo: FooterLogo;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.footerLogo = {
      id: '',
      createdBy: '',
      createdAt: '',
      brand: this.brandService.brand,
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      sortOrder: 0,
      title: '',
      target: '',
      disabled: false,
      lang: '',
      svg: '',
      svgId: '',
      uriMedium: '',
      uriOriginal: '',
      svgFilename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      target: new FormControl('', [Validators.required])
    });
  }

  getFooterLogo(): FooterLogo {
    const form = this.form.value;
    this.footerLogo.title = form.title;
    this.footerLogo.target = form.target;
    return this.footerLogo;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
