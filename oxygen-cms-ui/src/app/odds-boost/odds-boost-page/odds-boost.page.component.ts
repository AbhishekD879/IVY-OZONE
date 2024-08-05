import { MatSnackBar } from '@angular/material/snack-bar';
import { ActionButtonsComponent } from '../../shared/action-buttons/action-buttons.component';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '../../shared/dialog/dialog.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { OddsBoost } from '../../client/private/models/odds-boost.model';
import { ApiClientService } from '../../client/private/services/http/index';
import { Component, OnInit, ViewChild } from '@angular/core';
import {AppConstants} from '../../app.constants';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'odds-boost-page',
  templateUrl: './odds-boost.page.component.html'
})
export class OddsBoostPageComponent implements OnInit {

  public oddsBoost: OddsBoost;
  public breadcrumbsData: Breadcrumb[];
  public form: FormGroup;
  public isIMActive: boolean;
  public isLadbrokes: boolean;

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private brandService: BrandService
  ) {
    this.isIMActive = this.brandService.isIMActive();
  }

  ngOnInit(): void {
    this.breadcrumbsData = [{
      label: `Odds Boost`,
      url: `/odds-boost`
    }];
    this.globalLoaderService.showLoader();
    this.loadInitialData();
    this.isLadbrokes = (this.brandService.brand === 'ladbrokes');
  }

  public updateText(htmlMarkup: string, eventType: string): void {
    switch (eventType) {
      case 'logged-out-text':
        this.oddsBoost.loggedOutHeaderText = htmlMarkup;
        break;
      case 'logged-in-text':
        this.oddsBoost.loggedInHeaderText = htmlMarkup;
        break;
      case 'terms-and-conditions':
        this.oddsBoost.termsAndConditionsText = htmlMarkup;
        break;
      case 'no-tokens-text':
        this.oddsBoost.noTokensText = htmlMarkup;
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.loadInitialData();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  uploadSvgHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.oddsBoost()
      .uploadSvg(file)
      .map((data: HttpResponse<OddsBoost>) => {
        return data.body;
      })
      .subscribe((data: OddsBoost) => {
        this.oddsBoost = data;
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeSvgHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.oddsBoost()
      .removeSvg()
      .map((data: HttpResponse<OddsBoost>) => {
        return data.body;
      })
      .subscribe((data: OddsBoost) => {
        this.oddsBoost = data;
        this.snackBar.open(`Svg Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  private saveChanges(): void {
    this.apiClientService.oddsBoost()
      .udpate(this.oddsBoost)
      .map((response: HttpResponse<OddsBoost>) => {
        return response.body;
      })
      .subscribe((data: OddsBoost) => {
        this.oddsBoost = data;
        this.actionButtons.extendCollection(this.oddsBoost);
        this.fillCountDownTimer(this.oddsBoost.countDownTimer?this.oddsBoost.countDownTimer:'01:00:00');
        this.dialogService.showNotificationDialog({
          title: `Odds Boost Configuration Saving`,
          message: `Odds Boost Configuration is Saved.`
        });
      });
  }

  private loadInitialData(): void {
    this.apiClientService.oddsBoost().get().map((response: HttpResponse<OddsBoost>) => {
      return response.body;
    }).subscribe((oddsBoost: OddsBoost) => {
      this.hideLoading();
      this.oddsBoost = oddsBoost;
      let noTokensValidators = [Validators.minLength(1), Validators.required];
      if (!this.isLadbrokes) {
        noTokensValidators = [];
      }
      this.form = new FormGroup({
        loggedOut: new FormControl(this.oddsBoost.loggedOutHeaderText, [
          Validators.minLength(1),
          Validators.required]),
        loggedIn: new FormControl(this.oddsBoost.loggedInHeaderText, [
          Validators.minLength(1),
          Validators.required]),
        termsAndConditions: new FormControl(this.oddsBoost.termsAndConditionsText, [
          Validators.minLength(1),
          Validators.required]),
        moreLink: new FormControl(this.oddsBoost.moreLink),
        allowUserToToggleVisibility: new FormControl(this.oddsBoost.allowUserToToggleVisibility),
        daysToKeepPopupHidden: new FormControl(this.oddsBoost.daysToKeepPopupHidden,
          [Validators.min(0), Validators.max(Number.MAX_SAFE_INTEGER)]),
        noTokens: new FormControl(this.oddsBoost.noTokensText, noTokensValidators),
        hours: new FormControl('01', [Validators.min(1), Validators.max(Number.MAX_SAFE_INTEGER)]),
        minutes: new FormControl('00', [Validators.min(0), Validators.max(Number.MAX_SAFE_INTEGER)]),
        seconds: new FormControl('00', [Validators.min(0), Validators.max(Number.MAX_SAFE_INTEGER)]),
      });
      this.fillCountDownTimer(this.oddsBoost.countDownTimer?this.oddsBoost.countDownTimer:'01:00:00');
    }, () => {
      this.hideLoading();
    });
  }

  private hideLoading(): void {
    this.globalLoaderService.hideLoader();
  }

  validateTime(event: any) {
    event.target.value = this.transformTimeNumber(event.target.value);
    this.validateCountDownTimer();
  }
  private validateCountDownTimer() {
    let hours = this.form.get('hours')?.value;
    if (hours > 23) {
      this.form.get('hours')?.setValue(23);
      hours = 23;
    }
    const convertedHours = this.transformTimeNumber(hours);
    let minutes = this.form.get('minutes')?.value;
    if (minutes > 59) {
      this.form.get('minutes')?.setValue(59);
      minutes = 59;
    }
    const convertedMinutes = this.transformTimeNumber(minutes);
    let seconds = this.form.get('seconds')?.value;
    if (seconds > 59) {
      this.form.get('seconds')?.setValue(59);
      seconds = 59;
    }
    const convertedSeconds = this.transformTimeNumber(seconds);
    const combinedTime = `${convertedHours}:${convertedMinutes}:${convertedSeconds}`;
    this.oddsBoost.countDownTimer = combinedTime;
  }
  private transformTimeNumber(number) {
    const parsedNumber = parseInt(number, 10);
    return parsedNumber < 10 ? '0' + parsedNumber : parsedNumber;
  }
  private fillCountDownTimer(value:string) {
    const timerCountDownValue = value?.split(":");
    let hoursValue = timerCountDownValue[0];
    let minutesValue = timerCountDownValue[1];
    let secondsValue = timerCountDownValue[2];
    this.form.patchValue({
      hours: hoursValue,
      minutes: minutesValue,
      seconds: secondsValue
    })
  }

}
