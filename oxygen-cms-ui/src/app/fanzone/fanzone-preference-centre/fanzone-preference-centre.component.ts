import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { FzPreferences, Preferences } from '@app/client/private/models/fanzone.model';
import { PREFERENCES_CONST, PREFERENCES } from '@app/fanzone/constants/fanzone.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-fanzone-preference-centre',
  templateUrl: './fanzone-preference-centre.component.html',
  styleUrls: ['./fanzone-preference-centre.component.scss']
})

export class FanzonePreferenceCentreComponent implements OnInit {
  public form: FormGroup;
  fanzonePreferences: FzPreferences;
  isReady: boolean;
  singlePreference: Preferences = {
    name: '',
    key: ''
  }
  public readonly PREFERENCES_CONST = PREFERENCES_CONST;

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private dialogService: DialogService,
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.fanzonePreferences = {
      ...PREFERENCES,
      pcKeys: [{
        name: '',
        key: ''
      }],
      brand: this.brandService.brand
    };
    this.getFanzonePreferences();
  }

  getFanzonePreferences(): void {
    this.fanzonesAPIService.getFanzonePreferences()
      .subscribe(data => {
        this.fanzonePreferences = data.body?.id ? data.body : this.fanzonePreferences;
        this.isReady = true;
        this.generateForm();
      });
  }

  generateForm(): void {
    this.form = new FormGroup({
      // active: new FormControl(this.fanzonePreferences.active),
      pcDescription: new FormControl(this.fanzonePreferences.pcDescription, [Validators.required]),
      ctaText: new FormControl(this.fanzonePreferences.ctaText, [Validators.required]),
      confirmText: new FormControl(this.fanzonePreferences.confirmText, [Validators.required]),
      subscribeText: new FormControl(this.fanzonePreferences.subscribeText, [Validators.required]),
      confirmCTA: new FormControl(this.fanzonePreferences.confirmCTA, [Validators.required]),
      exitCTA: new FormControl(this.fanzonePreferences.exitCTA, [Validators.required]),
      notificationPopupTitle: new FormControl(this.fanzonePreferences.notificationPopupTitle, [Validators.required]),
      unsubscribeTitle: new FormControl(this.fanzonePreferences.unsubscribeTitle, [Validators.required]),
      notificationDescriptionDesktop: new FormControl(this.fanzonePreferences.notificationDescriptionDesktop, [Validators.required]),
      unsubscribeDescription: new FormControl(this.fanzonePreferences.unsubscribeDescription, [Validators.required]),
      pushPreferenceCentreTitle: new FormControl(this.fanzonePreferences.pushPreferenceCentreTitle, [Validators.required]),
      noThanksCTA: new FormControl(this.fanzonePreferences.noThanksCTA, [Validators.required]),
      optInCTA: new FormControl(this.fanzonePreferences.optInCTA, [Validators.required]),
      genericTeamNotificationTitle: new FormControl(this.fanzonePreferences.genericTeamNotificationTitle, [Validators.required]),
      genericTeamNotificationDescription: new FormControl(this.fanzonePreferences.genericTeamNotificationDescription, [Validators.required]),
    })

    if (this.fanzonePreferences.pcKeys.length) {
      const prefGroup = this.fanzonePreferences.pcKeys.map(pref => {
        return new FormGroup({
          name: new FormControl([pref?.name || '', Validators.required]),
          key: new FormControl([pref?.key || '', Validators.required])
        })
      });
      this.form.registerControl('pcKeys', new FormArray(prefGroup))
    }
  }

  get pcKeys() {
    return this.form.controls["pcKeys"] as FormArray;
  }

  addPreference(pref?: Preferences) {
    const preference = new FormGroup({
      name: new FormControl([pref?.name || '', Validators.required]),
      key: new FormControl([pref?.key || '', Validators.required])
    });
    this.pcKeys.push(preference);
    this.fanzonePreferences.pcKeys.push({ name: '', key: '' });
    this.actionButtons.extendCollection(this.fanzonePreferences);
  }

  deletePreference(i: number) {
    if (this.pcKeys.length > 1) {
      this.pcKeys.removeAt(i);
      this.fanzonePreferences.pcKeys.splice(i, 1);
    } else {
      this.dialogService.showNotificationDialog({
        title: 'Remove',
        message: 'You can not delete all the preferences. It should at least have single preference added'
      });
    }
  }

  saveFanzonePreferences() {
    const method = this.fanzonePreferences.id ? 'put' : 'post';
    this.fanzonesAPIService.saveFanzonePreferences(method, this.fanzonePreferences, this.fanzonePreferences.id || '')
      .subscribe(data => {
        this.fanzonePreferences = data.body;
        this.actionButtons.extendCollection(this.fanzonePreferences);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone SYC is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveFanzonePreferences();
        break;
      case 'revert':
        this.getFanzonePreferences();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

}
