import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { IFzOptinEmail } from '@app/client/private/models/fanzone.model';
import { FANZONE_OPTIN_EMAIL, OPTIN_EMAIL } from '@app/fanzone/constants/fanzone.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-fanzone-optin-email',
  templateUrl: './fanzone-optin-email.component.html'
})
export class FanzoneOptinEmailComponent implements OnInit {
  public form: FormGroup;
  fanzoneOptinEmail: IFzOptinEmail;
  isReady: boolean;
  public readonly FANZONE_OPTIN_EMAIL = FANZONE_OPTIN_EMAIL;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
    }, {
    label: 'FANZONE EMAIL OPTIN',
    url: `/fanzones/fanzone-optin-email`
  }];

  constructor(
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private dialogService: DialogService,
    private errorService: ErrorService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.fanzoneOptinEmail = {
      ...OPTIN_EMAIL,
      brand: this.brandService.brand,
      pageName: 'fanzone-optin-email'
    };
    this.getOptinEmail();
  }
  
  getOptinEmail(): void {
    // this.fanzoneOptinEmail = {
    //   optinEmailPopUpTitle: 'Test optinEmailPopUpTitle',
    //   optinEmailPopUpDescription: 'Test optinEmailPopUpDescription',
    //   fanzoneEmailPopupOptIn: 'Test fanzoneEmailPopupOptIn',
    //   fanzoneEmailPopupRemindMeLater: 'Test fanzoneEmailPopupRemindMeLater',
    //   fanzoneEmailPopupDontShowThisAgain: 'Test fanzoneEmailPopupDontShowThisAgain'
    // };
    this.isReady = true;
    this.generateForm();
    this.fanzonesAPIService.getFanzoneOptinEmail()
      .subscribe((fzData) => {
        const [data] = fzData.body;
        this.fanzoneOptinEmail = data?.id ? data : this.fanzoneOptinEmail;
        this.isReady = true;
        this.generateForm();
      });
  }

  generateForm(): void {
    this.form = new FormGroup({
      fanzoneEmailPopupTitle: new FormControl(this.fanzoneOptinEmail.fanzoneEmailPopupTitle, [Validators.required]),
      fanzoneEmailPopupDescription: new FormControl(this.fanzoneOptinEmail.fanzoneEmailPopupDescription, [Validators.required]),
      fanzoneEmailPopupOptIn: new FormControl(this.fanzoneOptinEmail.fanzoneEmailPopupOptIn, [Validators.required]),
      fanzoneEmailPopupRemindMeLater: new FormControl(this.fanzoneOptinEmail.fanzoneEmailPopupRemindMeLater, [Validators.required]),
      fanzoneEmailPopupDontShowThisAgain: new FormControl(this.fanzoneOptinEmail.fanzoneEmailPopupDontShowThisAgain, [Validators.required])
    });
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

  saveOptinEmail() {
    const method = this.fanzoneOptinEmail.id ? 'put' : 'post';
    this.fanzonesAPIService.saveOptinEmail(method, this.fanzoneOptinEmail, this.fanzoneOptinEmail.id || '')
      .subscribe(data => {
        this.fanzoneOptinEmail = data.body;
        this.actionButtons.extendCollection(this.fanzoneOptinEmail);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone Optin Email is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }


  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveOptinEmail();
        break;
      case 'revert':
        this.getOptinEmail();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
