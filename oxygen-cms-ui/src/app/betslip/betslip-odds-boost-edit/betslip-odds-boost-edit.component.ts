import { Component, OnInit, ViewChild } from '@angular/core';
import { BS_LABELS } from '../service/betslip.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { oddsBoostMock } from '../service/betslip-mock';
import { HttpResponse } from '@angular/common/http';
import { AppConstants } from '@app/app.constants';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IoddsBoost } from '../service/betslip.model';
import * as _ from 'lodash';

@Component({
  selector: 'betslip-odds-boost-edit',
  templateUrl: './betslip-odds-boost-edit.component.html',
  
})
export class BetslipOddsBoostEditComponent implements OnInit {
  @ViewChild("actionButtons") actionButtons;
  BSLABELS = BS_LABELS;
  form: FormGroup;
  isIMActive: boolean;
  oddsBoost: IoddsBoost;
  breadcrumbsData: any[];
  isLoading: boolean;
  

  constructor(
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService,

  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.isIMActive = this.brandService.isIMActive();
    Object.assign(oddsBoostMock, {
      brand: this.brandService.brand,
    })
    this.loadInitialData();
  }
  /*
*form controls
 */
  get formControls() {
    return this.form?.controls;
  }

  /**
   * it loads the initial data
   * loadInitialData()
   */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .betslipService().getOddsBoost().subscribe((data: { body: any }) => {
        if (!data.body.brand && !data.body.id) {
          this.oddsBoost = oddsBoostMock;
        } else {
          this.oddsBoost = data.body;
        }
        this.createBetSlipAccaFormGroup();
        this.actionButtons?.extendCollection(this.oddsBoost);
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.buildBreadCrumbsData();
      },
        error => {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        });
  }

  createBetSlipAccaFormGroup() {
     this.form = new FormGroup({
      oddsBoostMsgEnabled: new FormControl(this.oddsBoost.oddsBoostMsgEnabled || false),
      svgId: new FormControl(this.oddsBoost.svgId || ''),
      bsHeader: new FormControl(this.oddsBoost.bsHeader || '',[Validators.required, Validators.maxLength(20)]),
      bsDesc: new FormControl(this.oddsBoost.bsDesc || '',[Validators.required, Validators.maxLength(50)]),
      infoIcon:new FormControl(this.oddsBoost.infoIcon|| false),
      brsp :  new FormControl(this.oddsBoost.brsp || '',[Validators.required]),
      brspEnabled: new FormControl(this.oddsBoost.brspEnabled || false),
      brDispBoostedPrice: new FormControl(this.oddsBoost.brDispBoostedPrice || false),
      mbsp: new FormControl(this.oddsBoost.mbsp || '',[Validators.required]),
      mbspEnabled: new FormControl(this.oddsBoost.mbspEnabled || false),
      mbDispBoostedPrice: new FormControl(this.oddsBoost.mbDispBoostedPrice || false),
      profitIndicator: new FormControl(this.oddsBoost.profitIndicator || '',[Validators.required]),
    });
  }
  public saveChanges(message?): void {
    if(this.oddsBoost?.id){
      this.submitChanges('editOddsBoost',message);
    }else{
      this.submitChanges('saveOddsBoost',message);
    }
  }

  public submitChanges(reQuestType,message?): void {
    this.apiClientService
      .betslipService()[reQuestType](this.oddsBoost)
      .map((data: HttpResponse<IoddsBoost>) => data.body)
      .subscribe((bsData: IoddsBoost) => {
        this.oddsBoost = bsData;
        this.actionButtons.extendCollection(this.oddsBoost);
        this.snackBar.open(message ? message : `Odds Boost Data saved!`, "Ok!", {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  uploadSvgHandler(file): void {
    console.log('uploadSvgHandler', file);
    file.icon = file.svgId;
    this.globalLoaderService.showLoader();
    this.apiClientService.betslipService().uploadSvg(this.oddsBoost.svgId, file)
      .map((data: HttpResponse<IoddsBoost>) => {
        return data.body;
      })
      .subscribe((data: IoddsBoost) => {
        this.oddsBoost = _.extend(data, _.pick(this.oddsBoost, 'icon', 'targetUri'));
        console.log('uploadSvgHandler', data, this.oddsBoost)
        this.snackBar.open(`Svg Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case "save":
        this.saveChanges();
        break;
      case "revert":
        this.revertChanges();
        break;
      default:
        console.error("Unhandled Action");
        break;
    }
  }
/**
 * revrting the changes to onload 
 */
  public revertChanges(): void {
    this.loadInitialData();
  }

    /**
   * 
   *  Creating the BreadCrumbs for the page
   */

  private buildBreadCrumbsData() {
    this.breadcrumbsData = [
      {
        label: `Betslip`,
        url: `/betslip`,
      },
      {
        label: 'Odds Boost',
        url: `/betslip/betslip-odds-boost`,
      },
    ];
  }

  /**
   * @returns boolean
   * Here Validating the fields Which are out of form scope
   */

  // form validation
  public validationHandler(): boolean {
    return this.form && this.form.valid  ;
  }
}
