import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { BS_LABELS } from '../service/betslip.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { accInsuranceMock } from '../service/betslip-mock';
import { HttpResponse } from '@angular/common/http';
import { AppConstants } from '@app/app.constants';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IbetslipsAcca } from '../service/betslip.model';
import * as _ from 'lodash';

@Component({
  selector: "betslip-acca-insurance-edit",
  templateUrl: "./betslip-acca-insurance-edit.component.html"
})
export class BetslipAccaInsuranceEditComponent implements OnInit {
  @ViewChild("actionButtons") actionButtons;
  @ViewChild('informationTextEditor') informationTextEditor: TinymceComponent;
  BSLABELS = BS_LABELS;
  form: FormGroup;
  isIMActive: boolean;
  betSlipAcca: IbetslipsAcca;
  breadcrumbsData: any[];
  isLoading: boolean;
  

  constructor(
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private changeDetectorRef: ChangeDetectorRef,
    private dialogService: DialogService,

  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.isIMActive = this.brandService.isIMActive();
    Object.assign(accInsuranceMock, {
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
      .betslipService().getBetSlip().subscribe((data: { body: IbetslipsAcca }) => {

        if (!data.body.brand && !data.body.id) {
          this.betSlipAcca = accInsuranceMock;
        } else {
          this.betSlipAcca = data.body;
        }
        this.createBetSlipAccaFormGroup();
        this.actionButtons?.extendCollection( this.betSlipAcca);
        if (this.informationTextEditor) {
          this.informationTextEditor.update(this.betSlipAcca.popUpDetails.popUpMessage);
        }
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
      enabled : new FormControl(this.betSlipAcca.enabled || false),
      accInsMsgEnabled: new FormControl(this.betSlipAcca.accInsMsgEnabled || false),
      svgId: new FormControl(this.betSlipAcca.svgId || ''),
      bsAddToQualifyMsg: new FormControl(this.betSlipAcca.bsAddToQualifyMsg || '',[Validators.required, Validators.maxLength(67)]),
      avlblInscCountIndi: new FormControl(this.betSlipAcca.avlblInscCountIndi || '',[Validators.required, Validators.maxLength(25)]),
      obAccaCount :  new FormControl(this.betSlipAcca.obAccaCount || 0,[Validators.required,Validators.max(10)]),
      bsQualifiedMsg: new FormControl(this.betSlipAcca.bsQualifiedMsg || '',[Validators.required, Validators.maxLength(67)]),
      bsSp: new FormControl(this.betSlipAcca.betslipSp.bsSp || '',[Validators.required, Validators.maxLength(21)]),
      bsspEnabled: new FormControl(this.betSlipAcca.betslipSp.enabled || true),
      bsProgressBar: new FormControl(this.betSlipAcca.betslipSp.progressBar || false),
      bsInfoIcon: new FormControl(this.betSlipAcca.betslipSp.infoIcon || false),
      absp: new FormControl(this.betSlipAcca.accabarSp.absp || '',[Validators.required, Validators.maxLength(21)]),
      abspEnabled: new FormControl(this.betSlipAcca.accabarSp.enabled || true),
      abProgressBar: new FormControl(this.betSlipAcca.accabarSp.progressBar || true),
      brsp: new FormControl(this.betSlipAcca.betreceiptSp.brsp || '',[Validators.required, Validators.maxLength(21)]),
      brspEnabled: new FormControl(this.betSlipAcca.betreceiptSp.enabled || true),
      mbspEnabled: new FormControl(this.betSlipAcca.mybetsSp.enabled || true),
      mbsp: new FormControl(this.betSlipAcca.mybetsSp.mbsp || '',[Validators.required, Validators.maxLength(21)]),
      profitIndi: new FormControl(this.betSlipAcca.profitIndi || '',[Validators.required, Validators.maxLength(67)]),
      profitIndiUrl: new FormControl(this.betSlipAcca.profitIndiUrl || ''),
      popUpTitle: new FormControl(this.betSlipAcca.popUpDetails.popUpTitle || '',[Validators.required, Validators.maxLength(25)]),
      popUpMessage: new FormControl(this.betSlipAcca.popUpDetails.popUpMessage || '',[Validators.required]),
      priCtaLabel: new FormControl(this.betSlipAcca.popUpDetails.priCtaLabel || '',[Validators.required]),
      priCtaUrl: new FormControl(this.betSlipAcca.popUpDetails.priCtaUrl || '',),
      secCtaLabel: new FormControl(this.betSlipAcca.popUpDetails.secCtaLabel || '',),
      secCtaUrl: new FormControl(this.betSlipAcca.popUpDetails.secCtaUrl || ''),
    });
  }
  public saveChanges(message?): void {
    if(this.betSlipAcca?.id){
      this.submitChanges('edit',message);
    }else{
      this.submitChanges('saveBetslip',message);
    }
  }

  public submitChanges(reQuestType,message?): void {
    this.apiClientService
      .betslipService()[reQuestType](this.betSlipAcca)
      .map((data: HttpResponse<any>) => data.body)
      .subscribe((bsData: IbetslipsAcca) => {
        this.betSlipAcca = bsData;
        this.actionButtons.extendCollection(this.betSlipAcca);
        this.snackBar.open(message ? message : `Betslip Acca insurance saved!`, "Ok!", {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  uploadSvgHandler(file): void {
    console.log('uploadSvgHandler', file);
    file.icon = file.svgId;
    this.globalLoaderService.showLoader();
    this.apiClientService.betslipService().uploadSvg(this.betSlipAcca.svgId, file)
      .map((data: HttpResponse<any>) => {
        return data.body;
      })
      .subscribe((data: any) => {
        this.betSlipAcca = _.extend(data, _.pick(this.betSlipAcca, 'icon', 'targetUri'));
        console.log('uploadSvgHandler', data, this.betSlipAcca)
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

  public updateInfoTxtData(data: string) {
    this.form.get('popUpMessage').setValue(data);
    this.changeDetectorRef.detectChanges();
    return this.betSlipAcca.popUpDetails.popUpMessage = data;
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
        label: 'Acca Insurance',
        url: `/betslip/betslip-acca-insurance`,
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
