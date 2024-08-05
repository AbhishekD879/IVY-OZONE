import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, ValidatorFn, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {SportCategory, TARGET_URI_PATTERN} from '@app/client/private/models/sportcategory.model';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import {Tier} from '@app/client/private/models/tier.enum';

@Component({
  templateUrl: './sport-categories-create.component.html',
  styleUrls: ['./sport-categories-create.component.scss']
})
export class SportCategoriesCreateComponent implements OnInit {

  public form: FormGroup;
  public sportCategory: SportCategory;
  public isRealSport;
  get tiers() { return Tier; }

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.sportCategory = {
      id: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      alt: '',
      brand: this.brandService.brand,
      tier: Tier.TIER_2,
      categoryId: null,
      disabled: false,
      heightMedium: 0,
      heightMediumIcon: 0,
      heightSmall: 0,
      heightSmallIcon: 0,
      imageTitle: '',
      inApp: true,
      isTopSport: false,
      key: '',
      lang: '',
      link: '',
      path: '',
      showInMenu: false,
      sortOrder: 0,
      spriteClass: '',
      ssCategoryCode: '',
      outrightSport: true,
      multiTemplateSport: false,
      oddsCardHeaderType: null,
      typeIds: null,
      dispSortNames: '',
      primaryMarkets: '',
      svg: '',
      svgId: '',
      targetUri: 'sport/',
      updatedAt: '',
      updatedBy: '',
      uriMedium: '',
      uriMediumIcon: '',
      uriSmall: '',
      uriSmallIcon: '',
      widthMedium: 0,
      widthMediumIcon: 0,
      widthSmall: 0,
      widthSmallIcon: 0,
      collectionType: '',
      showInAZ: false,
      showInHome: false,
      showInPlay: false,
      heightLarge: 0,
      heightLargeIcon: 0,
      uriLarge: '',
      widthLarge: 0,
      widthLargeIcon: 0,
      scoreBoardUri: '',
      topMarkets:'',
      aggrigatedMarkets:[],
      filename: {
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
      svgFilename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      showScoreboard: false,
      highlightCarouselEnabled: false,
      quickLinkEnabled: false,
      inplayEnabled: false,
      inplaySportModule: {
        enabled: false,
        inplayCount: 10
      },
      isRealSport(): boolean {
        return this.tier === Tier.TIER_1 || this.tier === Tier.TIER_2;
      },
      isFRRealSport(): boolean {
        return false;
      },
      isReactionsEnabled: false,
      inplayStatsConfig: {
        showStatsWidget:false,
        note:'Please note: Stats widget league are configured in System Configurations'+"/ "+'"'+'CouponStatsWidget'+'" '+'Table'
      }
    };
    this.form = new FormGroup({
      imageTitle: new FormControl(this.sportCategory.imageTitle, [Validators.required]),
      categoryId: new FormControl(this.sportCategory.categoryId, [Validators.required]),
      ssCategoryCode: new FormControl(this.sportCategory.ssCategoryCode, [Validators.required]),
      targetUri: new FormControl(this.sportCategory.targetUri, [Validators.required, Validators.pattern(TARGET_URI_PATTERN)]),
      tier: new FormControl(this.sportCategory.tier, [Validators.required])
    });
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isSportCategoryInValid() {
    return !this.form.valid;
  }

  tierChanged() {
    this.updateValidators();
  }

  private updateValidators() {
    this.setValidatorIfRealSport('categoryId', Validators.required, null);
    this.setValidatorIfRealSport('targetUri', Validators.pattern(TARGET_URI_PATTERN), null);
  }

  private setValidatorIfRealSport(field: string, realSportValidator: ValidatorFn, defaultValidator: ValidatorFn) {
    const control = this.form.get(field);
    control.setValidators(this.sportCategory.isRealSport() ? realSportValidator : defaultValidator);
    control.updateValueAndValidity();
  }
}
