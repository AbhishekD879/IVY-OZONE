import {Component, OnInit} from '@angular/core';
import {StaticTextOtf} from '../../../client/private/models/staticTextOtf.model';
import {ConfirmDialogComponent} from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import {BrandService} from '../../../client/private/services/brand.service';

@Component({
  selector: 'static-text-otf-create-dialog',
  templateUrl: './static-text.create.component.html',
  styleUrls: ['./static-text.create.component.scss'],
  providers: []
})
export class StaticTextOtfCreateComponent implements OnInit {
  getDataError: string;
  newStaticTextOtf: StaticTextOtf;

  selectPageNames = [
    {id: '1', name: 'Splash page'},
    {id: '2', name: 'Current week tab'},
    {id: '3', name: 'You are in page'},
  ];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {}

  public updateText(htmlMarkup: string, index: number): void {
    this.newStaticTextOtf['pageText' + index] = htmlMarkup;
  }

  isValidModel() {
    return this.newStaticTextOtf.pageName.length > 0;
  }

  closeDialog() {
    this.dialogRef.close();
  }

  ngOnInit() {
    this.newStaticTextOtf = {
      lang: '',
      enabled: false,
      pageName: '',
      title: '',
      ctaText1: '',
      ctaText2: '',
      pageText1: '',
      pageText2: '',
      pageText3: '',
      pageText4: '',
      pageText5: '',
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',
    };
  }
}
