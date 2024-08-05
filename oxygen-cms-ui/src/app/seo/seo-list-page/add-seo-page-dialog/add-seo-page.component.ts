import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { SeoPage } from '@app/client/private/models/seopage.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'add-seo-page',
  templateUrl: './add-seo-page.component.html',
  styleUrls: ['./add-seo-page.component.scss']
})
export class AddSeoPageComponent implements OnInit {
  public newSeoPage: SeoPage;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
   ) {}

  ngOnInit() {
    this.newSeoPage = {
      id: '',
      brand: this.brandService.brand,
      changefreq: 'daily',
      createdAt: '',
      createdBy: '',
      description: '',
      disabled: true,
      lang: '',
      staticBlock: '',
      title: '',
      updatedAt: '',
      updatedBy: '',
      url: '',
      urlBrand: '',
      priority: '0',
      updatedByUserName: '',
      createdByUserName: '',
      staticBlockTitle: ''
    };
  }

  isValidUrl() {
    return this.newSeoPage.url.length > 0 && this.newSeoPage.url.match(/^\//);
  }

  isValidFormData() {
    return this.isValidUrl() &&
      this.newSeoPage.title.length > 0;
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
