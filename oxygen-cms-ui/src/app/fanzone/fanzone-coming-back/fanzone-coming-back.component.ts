import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { IFanzoneComingBack } from '@app/client/private/models/fanzone.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { FZ_COMING_BACK_CONST } from '../constants/fanzone.constants';
import { FanzonesAPIService } from '../services/fanzones.api.service';
@Component({
  selector: 'app-fanzone-coming-back',
  templateUrl: './fanzone-coming-back.component.html',
  styleUrls: ['./fanzone-coming-back.component.scss']
})
export class FanzoneComingBackComponent implements OnInit {
  public form: FormGroup;
  fanzoneComingBack: IFanzoneComingBack;
  isReady: boolean = false;
  public readonly FZ_COMING_BACK_CONST = FZ_COMING_BACK_CONST;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'Fanzone Coming Soon',
    url: `/fanzones/fanzone-coming-back`
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
    this.fanzoneComingBack = {
      ...FZ_COMING_BACK_CONST,
      brand: this.brandService.brand,
      pageName: 'fanzone-coming-back'
    };
    this.getFanzoneComingBackDetails();
  }
  getFanzoneComingBackDetails() {
    this.fanzonesAPIService.getFanzoneComingBackDetails()
      .subscribe(data => {
        this.fanzoneComingBack = data.body?.id ? data.body : this.fanzoneComingBack;
        this.isReady = true;
        this.generateForm();
      });
  }
  generateForm(): void {
    this.form = new FormGroup({
      fzComingBackPopupDisplay: new FormControl(this.fanzoneComingBack.fzComingBackPopupDisplay, []),
      fzComingBackTitle: new FormControl(this.fanzoneComingBack.fzComingBackTitle, [Validators.required, Validators.maxLength(25)]),
      fzComingBackDescription: new FormControl(this.fanzoneComingBack.fzComingBackDescription, [Validators.required, Validators.maxLength(150)]),
      fzComingBackBadgeUrlDesktop: new FormControl(this.fanzoneComingBack.fzComingBackBadgeUrlDesktop, [Validators.required]),
      fzComingBackBgImageDesktop: new FormControl(this.fanzoneComingBack.fzComingBackBgImageDesktop, [Validators.required]),
      fzComingBackOKCTA: new FormControl(this.fanzoneComingBack.fzComingBackOKCTA, [Validators.required, Validators.maxLength(20)]),
      fzComingBackDisplayFromDays: new FormControl(this.fanzoneComingBack.fzComingBackDisplayFromDays, [Validators.required, Validators.pattern(/^[1-9]\d*$/)])
    });
  }
  saveFanzoneComingBackData() {
    const method = this.fanzoneComingBack.id ? 'put' : 'post';
    this.fanzonesAPIService.saveFanzoneComingBackData(method, this.fanzoneComingBack, this.fanzoneComingBack.id || '')
      .subscribe(data => {
        this.fanzoneComingBack = data.body;
        this.actionButtons.extendCollection(this.fanzoneComingBack);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone Coming Soon data is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }
  public validationHandler(): boolean {
    return this.form && this.form.valid;
  }
  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveFanzoneComingBackData();
        break;
      case 'revert':
        this.getFanzoneComingBackDetails();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
  get fzComingBackTitle() {
    return this.form.get('fzComingBackTitle');
  }
  get fzComingBackDescription() {
    return this.form.get('fzComingBackDescription');
  }
  get fzComingBackOKCTA() {
    return this.form.get('fzComingBackOKCTA');
  }
}
