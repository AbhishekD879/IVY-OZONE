import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { Syc } from '@app/client/private/models/fanzone.model';
import { SYC_POPUP_CONST, SYC_SELECT_CONST, SYC } from '@app/fanzone/constants/fanzone.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { DateRange } from '@app/client/private/models';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-fanzone-syc',
  templateUrl: './fanzone-syc.component.html'
})
export class FanzoneSycComponent implements OnInit {
  public form: FormGroup;
  fanzoneSyc: Syc;
  isReady: boolean;
  public readonly SYC_POPUP_CONST = SYC_POPUP_CONST;
  public readonly SYC_SELECT_CONST = SYC_SELECT_CONST;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'Show Your Colors',
    url: `/fanzones/show-your-colors`
  }];

  constructor(
    private dialogService: DialogService,
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.fanzoneSyc = {
      ...SYC,
      brand: this.brandService.brand,
      pageName: 'fanzone-syc'
    };
    this.getFanzoneSyc();
  }

  saveSYC() {
    const method = this.fanzoneSyc.id ? 'put' : 'post';
    this.fanzonesAPIService.saveFanzoneSyc(method, this.fanzoneSyc, this.fanzoneSyc.id || '')
      .subscribe(data => {
        this.fanzoneSyc = data.body;
        this.actionButtons.extendCollection(this.fanzoneSyc);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone SYC is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  getFanzoneSyc(): void {
    this.fanzonesAPIService.getFanzoneSyc()
      .subscribe(data => {
        this.fanzoneSyc = data.body?.id ? data.body : this.fanzoneSyc;
        this.isReady = true;
        this.generateForm();
      });
  }

  generateForm(): void {
    this.form = new FormGroup({
      sycPopUpTitle: new FormControl(this.fanzoneSyc.sycPopUpTitle, [Validators.required]),
      sycPopUpDescription: new FormControl(this.fanzoneSyc.sycPopUpDescription, [Validators.required]),
      sycImage: new FormControl(this.fanzoneSyc.sycImage, [Validators.required]),
      okCTA: new FormControl(this.fanzoneSyc.okCTA, [Validators.required]),
      dontShowAgain: new FormControl(this.fanzoneSyc.dontShowAgain, [Validators.required]),
      remindLater: new FormControl(this.fanzoneSyc.remindLater, [Validators.required]),
      remindLaterHideDays: new FormControl(this.fanzoneSyc.remindLaterHideDays, [Validators.required]),
      sycTitle: new FormControl(this.fanzoneSyc.sycTitle, [Validators.required]),
      sycDescription: new FormControl(this.fanzoneSyc.sycDescription, [Validators.required]),
      daysToChangeTeam: new FormControl(this.fanzoneSyc.daysToChangeTeam, [Validators.required, Validators.pattern(/^[1-9]\d*$/)]),
      sycLoginCTA: new FormControl(this.fanzoneSyc.sycLoginCTA, [Validators.required]),
      sycConfirmCTA: new FormControl(this.fanzoneSyc.sycConfirmCTA, [Validators.required]),
      sycChangeCTA: new FormControl(this.fanzoneSyc.sycChangeCTA, [Validators.required]),
      sycExitCTA: new FormControl(this.fanzoneSyc.sycExitCTA, [Validators.required]),
      sycCancelCTA: new FormControl(this.fanzoneSyc.sycCancelCTA, [Validators.required, Validators.maxLength(10)]),
      sycThankYouTitle: new FormControl(this.fanzoneSyc.sycThankYouTitle, [Validators.required]),
      sycConfirmTitle: new FormControl(this.fanzoneSyc.sycConfirmTitle, [Validators.required]),
      sycNoTeamSelectionTitle: new FormControl(this.fanzoneSyc.sycNoTeamSelectionTitle, [Validators.required]),
      customTeamNameText: new FormControl(this.fanzoneSyc.customTeamNameText, [Validators.required]),
      customTeamNameDescription: new FormControl(this.fanzoneSyc.customTeamNameDescription, [Validators.required, Validators.maxLength(150)]),
      thankYouMsg: new FormControl(this.fanzoneSyc.thankYouMsg, [Validators.required]),
      sycConfirmMsgMobile: new FormControl(this.fanzoneSyc.sycConfirmMsgMobile, [Validators.required]),
      sycConfirmMsgDesktop: new FormControl(this.fanzoneSyc.sycConfirmMsgDesktop, [Validators.required]),
      sycPreLoginTeamSelectionMsg: new FormControl(this.fanzoneSyc.sycPreLoginTeamSelectionMsg, [Validators.required]),
      sycPreLoginNoTeamSelectionMsg: new FormControl(this.fanzoneSyc.sycPreLoginNoTeamSelectionMsg, [Validators.required]),
      changeTeamTimePeriodMsg: new FormControl(this.fanzoneSyc.changeTeamTimePeriodMsg, [Validators.required])
    });
  }
  
  handleDateUpdate(data: DateRange) {
    this.fanzoneSyc.seasonStartDate = data.startDate;
    this.fanzoneSyc.seasonEndDate = data.endDate;
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveSYC();
        break;
      case 'revert':
        this.getFanzoneSyc();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

}
