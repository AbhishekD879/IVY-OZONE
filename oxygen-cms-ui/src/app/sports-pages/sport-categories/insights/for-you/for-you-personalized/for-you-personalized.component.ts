import { Component, OnInit, ViewChild, ChangeDetectorRef } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActionButtonsComponent } from '@root/app/shared/action-buttons/action-buttons.component';
import * as _ from 'lodash';

import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ForYou } from './for-you-personalized.model';
import { TinymceComponent } from '@root/app/shared/tinymce/tinymce.component';
import { ActivatedRoute } from '@angular/router';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FOR_YOU_DETAILS } from '../../inisghts-tab/insights-mock';

@Component({
  templateUrl: "./for-you-personalized.component.html",
  providers: [],
})
export class ForyoupersonalizedComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('informationTextEditor') informationTextEditor: TinymceComponent;
  breadcrumbsData: any = [];
  isUntiedSport: boolean = false;
  forYou: ForYou;
  form: FormGroup;
  forYouFormGroup: FormGroup;
  forYoutabId: any;
  routeIds: any;

  constructor(
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private changeDetectorRef: ChangeDetectorRef,
    private snackBar: MatSnackBar
  ) {}

  /**
* To save and edit
* @param {string} requestType
*/
  ngOnInit(): void {
    this.loadInitialData();
  }
  /**
 * To save and edit
 * @param {string} requestType
 */

  private loadInitialData(): void {
    this.activatedRoute.params.subscribe(params => {
      this.routeIds = params;
      this.forYoutabId = params['forYouid']; // Access the 'id' parameter from the URL
    });

    this.apiClientService.forYouService()
      .getDetailsByBrand(this.forYoutabId)
      .subscribe((data: { body: ForYou }) => {
        this.forYou = data.body;
        if (!data.body) {
          this.forYou = FOR_YOU_DETAILS;
        }  
        this.buildBreadCrumbsData(this.routeIds);
        if (this.informationTextEditor) {
          this.informationTextEditor.update(this.forYou.informationTextDesc);
        }
        this.createFormGroup();
        this.actionButtons?.extendCollection(this.forYou);
      },
        error => {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      );
  }

  public createFormGroup(): void {
    this.form = new FormGroup({
      headerDisplayName: new FormControl(this.forYou?.headerDisplayName || '', [Validators.required, Validators.maxLength(25)]),
      showMoreText: new FormControl(this.forYou?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(this.forYou?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(this.forYou?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(this.forYou?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      numbOfShowMorePopularBets: new FormControl(this.forYou?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(this.forYou?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(this.forYou?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(this.forYou?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(this.forYou?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(this.forYou?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(this.forYou?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(this.forYou?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(this.forYou?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(this.forYou?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(this.forYou?.nonLoginHeader || '', [Validators.required]),
      noBettingCTA: new FormControl(this.forYou?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(this.forYou?.noBettingHeader || '', [Validators.required, Validators.maxLength(25)]),
      noBettingDesc: new FormControl(this.forYou?.noBettingDesc || '', [Validators.required]),
      enableArrowIcon: new FormControl(this.forYou?.enableArrowIcon || false, [Validators.required]),
      enableBackedUpTimes: new FormControl(this.forYou?.enableBackedUpTimes || false, [Validators.required]),
      noBettingDescTitle: new FormControl(this.forYou?.noBettingDescTitle || '', [Validators.required, Validators.maxLength(250)])
    });
  }

  get formControls() {
    return this.form?.controls;
  }

  private buildBreadCrumbsData(routeIds) {
    this.breadcrumbsData = [
      {
        label: `Sport Categories`,
        url: `/sports-pages/sport-categories`,
      },
      {
        label: 'Foootball',
        url: `/sports-pages/sport-categories/${routeIds.id}`,
      },
      {
        label: "insights Tab",
        url: `/sports-pages/sport-categories/${routeIds.id}/sport-tab/${routeIds.sportTabId}/insightsTab`,
      },
      {
        label: "foryou main",
        url: `/sports-pages/sport-categories/${routeIds.id}/sport-tab/${routeIds.sportTabId}/insightsTab/insights-forYou`,
      },
      {
        label: "foryou personalized bets",
        url: `/sports-pages/sport-categories/${routeIds.id}/sport-tab/${routeIds.sportTabId}/insightsTab/insights-forYou/for-you-personalized-bets/${routeIds.forYouid}`,
      },
    ];
  }

  /**
 * Update Information text Blurb message
 * @param {string}  newBlurbText
 * @param {string} field
 */
  public updateInfoTxtData(data: string) {
    this.form.get('informationTextDesc').setValue(data);
    this.changeDetectorRef.detectChanges();
    return this.forYou.informationTextDesc = data;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
 * To save and edit
 * @param {string} requestType
 */
  saveChanges(): void {
      this.sendRequest('saveCMSForYouPersonalizedData');
  }

  /**
 * To save and edit
 * @param {string} requestType
 */
  private sendRequest(requestType: string, isInitialLoad: boolean = false): void {
    this.apiClientService.forYouService()[requestType](this.forYou)
      .map((response) => response.body)
      .subscribe((data: ForYou) => {
        this.forYou = data;
        this.actionButtons?.extendCollection(this.forYou);
        if (!isInitialLoad) {
          this.snackBar.open(`Sport Tab is saved!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  /**
   * to revert active changes
   */
  public revertChanges(): void {
    this.loadInitialData();
  }

}
