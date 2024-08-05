import {Component, OnInit} from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import {Sport} from '../../../../client/private/models/sport.model';
import {ConfirmDialogComponent} from '../../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '../../../../client/private/services/brand.service';

@Component({
  selector: 'add-olympics-page',
  templateUrl: './add-olympics-page.component.html',
  styleUrls: ['./add-olympics-page.component.scss']
})
export class AddOlympicsPageComponent implements OnInit {
  public newOlympicsPage: Sport;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.newOlympicsPage = {
      id: '',
      imageTitle: '',
      alt: '',
      brand: this.brandService.brand,
      categoryId: null,
      createdAt: '',
      createdBy: '',
      typeIds: '',
      collectionType: '',
      disabled: true,
      dispSortName: '',
      heightMedium: 0,
      heightMediumIcon: 0,
      heightSmall: 0,
      heightSmallIcon: 0,
      inApp: true,
      isOutrightSport: false,
      lang: 'en',
      outcomesTemplateType1: 'homeDrawAwayType',
      outcomesTemplateType2: 'homeDrawAwayType',
      outcomesTemplateType3: 'homeDrawAwayType',
      primaryMarkets: '',
      showInPlay: true,
      sortOrder: 0,
      spriteClass: '',
      ssCategoryCode: '',
      svg: '',
      svgId: '',
      tabCompetitions: {
        tablabel: '',
        visible: false
      },
      tabCoupons: {
        tablabel: '',
        visible: false
      },
      tabJackpot: {
        tablabel: '',
        visible: false
      },
      tabLive: {
        tablabel: '',
        visible: false
      },
      tabMatches: {
        tablabel: '',
        visible: false
      },
      tabOutrights: {
        tablabel: '',
        visible: false
      },
      tabSpecials: {
        tablabel: '',
        visible: false
      },
      targetUri: '',
      updatedAt: '',
      updatedBy: '',
      uriMedium: '',
      uriSmall: '',
      viewByFilters: '',
      widthMedium: 0,
      widthMediumIcon: 0,
      widthSmall: 0,
      widthSmallIcon: 0,
      defaultTab: '',
      heightLarge: 0,
      heightLargeIcon: 0,
      uriLarge: '',
      widthLarge: 0,
      widthLargeIcon: 0,
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
      },
      icon: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      updatedByUserName: '',
      createdByUserName: '',
      fileNameString: ''
    };
  }

  isValidTypeIds() {
    return this.newOlympicsPage.typeIds.length > 0 && this.newOlympicsPage.typeIds.match(/^[0-9,]+$/);
  }

  isValidFormData() {
    return this.isValidTypeIds() &&
      this.newOlympicsPage.categoryId > 0 &&
      this.newOlympicsPage.imageTitle.length > 0;
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
