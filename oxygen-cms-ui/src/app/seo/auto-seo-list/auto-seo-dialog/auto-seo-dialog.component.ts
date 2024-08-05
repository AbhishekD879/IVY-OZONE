import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-auto-seo-dialog',
  templateUrl: './auto-seo-dialog.component.html'
})
export class AutoseoPageDialogComponent implements OnInit {
  public newAutoSeoPage: AutoSeoPage;
  getDataError: string;
  autoseopageid: string;
  dailogTitle: string;
  autoseoPage: AutoSeoPage;
  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    @Inject(MAT_DIALOG_DATA) public dialog: any,
  ) { }

  /**
   * loads the autoseopage data from dialog box
   */
  ngOnInit(): void {
    this.autoseopageid = this.dialog.data.id;
    this.newAutoSeoPage = {
      id: '',
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      metaDescription: '',
      metaTitle: '',
      updatedAt: '',
      updatedBy: '',
      uri: '',
      updatedByUserName: '',
      createdByUserName: ''
    };
    this.dailogTitle = this.autoseopageid ? 'Edit a Auto Seo Page' : 'Create a New AutoSeo Page';
    if (this.autoseopageid) {
    this.autoseoPage = this.dialog.data;
   }
  }
  /**
   * validates the url
   * @param uri 
   * @returns 
   */
  isValidUrl(uri: string): boolean {
    const regex: RegExp = /^\//;
    return uri?.length > 0 && regex.test(uri);
  }
  /**
   * validates form data 
   * @param autoseopage 
   * @returns boolean value
   */
  isValidFormData(autoseopage: AutoSeoPage): number {
    return this.isValidUrl(autoseopage.uri) &&
      autoseopage?.metaTitle.length  && autoseopage?.metaDescription.length;
  }
  /**
   * calls close method 
   */
  closeDialog(): void {
    this.dialogRef.close();
  }
}

