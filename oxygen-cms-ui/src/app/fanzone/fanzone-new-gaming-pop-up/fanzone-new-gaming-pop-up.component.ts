import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { IPopUp } from '@app/client/private/models/fanzone.model';
import { FZ_POPUP, FZ_POPUP_CONST } from '@app/fanzone/constants/fanzone.constants';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BrandService } from '@root/app/client/private/services/brand.service';

@Component({
  selector: 'app-fanzone-new-gaming-pop-up-component.ts',
  templateUrl: './fanzone-new-gaming-pop-up.component.html'
})
export class FanzoneNewGamingPopUpComponent implements OnInit {
  public form: FormGroup;
  fanzoneNewGamingPopUp: IPopUp;
  isReady: boolean;
  public readonly FZ_POPUP = FZ_POPUP;
  public readonly FZ_POPUP_CONST = FZ_POPUP_CONST;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'New Gaming Pop Up',
    url: `/fanzones/new-gaming-pop-up`
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
    this.fanzoneNewGamingPopUp = {
      ...FZ_POPUP,
      brand: this.brandService.brand,
      pageName: 'fanzone-new-gaming-pop-up'
    };

    this.getFzPopUp();
  }

  saveFzPopUp() {
    const method = this.fanzoneNewGamingPopUp.id ? 'put' : 'post';
    this.fanzonesAPIService.saveNewGamingPopUp(method, this.fanzoneNewGamingPopUp, this.fanzoneNewGamingPopUp.id || '')
      .subscribe(data => {
        this.fanzoneNewGamingPopUp = data.body;
        this.actionButtons.extendCollection(this.fanzoneNewGamingPopUp);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone PopUp is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  generateForm(): void {
    this.form = new FormGroup({
      title: new FormControl(this.fanzoneNewGamingPopUp?.title, [Validators.required]),
      description: new FormControl(this.fanzoneNewGamingPopUp?.description, [Validators.required]),
      closeCTA: new FormControl(this.fanzoneNewGamingPopUp?.closeCTA, [Validators.required]),
      playCTA: new FormControl(this.fanzoneNewGamingPopUp?.playCTA, [Validators.required]),
    });
  }

  getFzPopUp(): void {
    this.fanzonesAPIService.getNewGamingPopUp()
      .subscribe(data => {
        this.fanzoneNewGamingPopUp = data.body?.id ? data.body : this.fanzoneNewGamingPopUp;
        this.isReady = true;
        this.generateForm();
      });
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveFzPopUp();
        break;
      case 'revert':
        this.getFzPopUp();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
