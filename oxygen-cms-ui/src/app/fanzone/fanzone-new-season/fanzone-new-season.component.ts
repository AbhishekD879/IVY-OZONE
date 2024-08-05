import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { IFanzoneNewSeason } from '@app/client/private/models/fanzone.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { FZ_NEW_SEASON_CONST } from '../constants/fanzone.constants';
import { FanzonesAPIService } from '../services/fanzones.api.service';
@Component({
  selector: 'app-fanzone-new-season',
  templateUrl: './fanzone-new-season.component.html',
  styleUrls: ['./fanzone-new-season.component.scss']
})
export class FanzoneNewSeasonComponent implements OnInit {
  public form: FormGroup;
  fanzoneNewSeason: IFanzoneNewSeason;
  isReady: boolean = false;
  public readonly FZ_NEW_SEASON_CONST = FZ_NEW_SEASON_CONST;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'Fanzone On Vacation',
    url: `/fanzones/fanzone-new-season`
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
    this.fanzoneNewSeason = {
      ...FZ_NEW_SEASON_CONST,
      brand: this.brandService.brand,
      pageName: 'fanzone-coming-back'
    };
    this.getFanzoneNewSeasonDetails();
  }
  getFanzoneNewSeasonDetails() {
    this.fanzonesAPIService.getFanzoneNewSeasonDetails()
      .subscribe(data => {
        this.fanzoneNewSeason = data.body?.id ? data.body : this.fanzoneNewSeason;
        this.isReady = true;
        this.generateForm();
      });
  }
  generateForm(): void {
    this.form = new FormGroup({
      fzNewSeasonTitle: new FormControl(this.fanzoneNewSeason.fzNewSeasonTitle, [Validators.required, Validators.maxLength(25)]),
      fzNewSeasonDescription: new FormControl(this.fanzoneNewSeason.fzNewSeasonDescription, [Validators.required, Validators.maxLength(150)]),
      fzNewSeasonBgImageDesktop: new FormControl(this.fanzoneNewSeason.fzNewSeasonBgImageDesktop, [Validators.required]),
      fzNewSeasonBgImageMobile: new FormControl(this.fanzoneNewSeason.fzNewSeasonBgImageMobile, [Validators.required]),
      fzNewSeasonBadgeDesktop: new FormControl(this.fanzoneNewSeason.fzNewSeasonBadgeDesktop, [Validators.required]),
      fzNewSeasonBadgeMobile: new FormControl(this.fanzoneNewSeason.fzNewSeasonBadgeMobile, [Validators.required]),
      fzNewSeasonLightningDesktop: new FormControl(this.fanzoneNewSeason.fzNewSeasonLightningDesktop, [Validators.required]),
      fzNewSeasonLightningMobile: new FormControl(this.fanzoneNewSeason.fzNewSeasonLightningMobile, [Validators.required]),
    });
  }
  saveFanzoneNewSeasonData() {
    const method = this.fanzoneNewSeason.id ? 'put' : 'post';
    this.fanzonesAPIService.saveFanzoneNewSeasonData(method, this.fanzoneNewSeason, this.fanzoneNewSeason.id || '')
      .subscribe(data => {
        this.fanzoneNewSeason = data.body;
        this.actionButtons.extendCollection(this.fanzoneNewSeason);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone On Vacation data is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }
  public validationHandler(): boolean {
    return this.form && this.form.valid
  }
  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveFanzoneNewSeasonData();
        break;
      case 'revert':
        this.getFanzoneNewSeasonDetails();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
  get fzNewSeasonTitle() {
    return this.form.get('fzNewSeasonTitle');
  }
  get fzNewSeasonDescription() {
    return this.form.get('fzNewSeasonDescription');
  }
}
