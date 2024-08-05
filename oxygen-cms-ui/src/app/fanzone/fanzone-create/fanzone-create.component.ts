import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Fanzone } from '@app/client/private/models/fanzone.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FANZONE_DETAILS, FANZONE } from '@app/fanzone/constants/fanzone.constants';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { AbstractControl, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';

@Component({
  selector: 'app-fanzone-create',
  templateUrl: './fanzone-create.component.html'
})
export class FanzoneCreateComponent implements OnInit {
  public readonly FANZONE_DETAILS = FANZONE_DETAILS;
  fanzone: Fanzone;
  public form: FormGroup;

  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'Create Fanzone',
    url: `/fanzones/create`
  }];

  constructor(
    private router: Router,
    private dialogService: DialogService,
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService
  ) { }

  ngOnInit(): void {
    this.fanzone = {
      ...FANZONE,
      brand: this.brandService.brand
    };
    this.generateForm();
  }

  generateForm(): void {
    this.form = new FormGroup({
      active: new FormControl(this.fanzone?.active, [Validators.required]),
      name: new FormControl(this.fanzone?.name, [Validators.required]),
      launchBannerUrl: new FormControl(this.fanzone?.launchBannerUrl, [Validators.required]),
      launchBannerUrlDesktop: new FormControl(this.fanzone?.fanzoneConfiguration.launchBannerUrlDesktop, [Validators.required]),
      teamId: new FormControl(this.fanzone?.teamId, [Validators.required,  forbiddenNameValidator(/FZ001/i)]),
      openBetID: new FormControl(this.fanzone?.openBetID, [Validators.required]),
      fanzoneBanner: new FormControl(this.fanzone?.fanzoneBanner, [Validators.required]),
      fanzoneBannerDesktop: new FormControl(this.fanzone?.fanzoneConfiguration.fanzoneBannerDesktop, [Validators.required]),
      assetManagementLink: new FormControl(this.fanzone?.assetManagementLink, [Validators.required]),
      location: new FormControl(this.fanzone?.location, [Validators.required]),
      primaryCompetitionId: new FormControl(this.fanzone?.primaryCompetitionId, [Validators.required]),
      secondaryCompetitionId: new FormControl(this.fanzone?.secondaryCompetitionId),
      clubIds: new FormControl(this.fanzone?.clubIds),
      hexColorCode: new FormControl(this.fanzone?.hexColorCode, [Validators.required, Validators.pattern("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}$)")]),
      is21stOrUnlistedFanzoneTeam: new FormControl(this.fanzone?.is21stOrUnlistedFanzoneTeam),
    })

    function forbiddenNameValidator(nameRe: RegExp): ValidatorFn {
      return (control: AbstractControl): ValidationErrors | null => {
        const forbidden = nameRe.test(control.value);
        return forbidden ? {forbiddenName: {value: control.value}} : null;
      };
    }
  }

  generateUnlistedGameForm(): void {
    this.form = new FormGroup({
      active: new FormControl(this.fanzone.active, [Validators.required]),
      name: new FormControl(this.fanzone.name, [Validators.required]),
      launchBannerUrl: new FormControl(this.fanzone.launchBannerUrl, [Validators.required]),
      launchBannerUrlDesktop: new FormControl(this.fanzone.fanzoneConfiguration.launchBannerUrlDesktop, [Validators.required]),
      teamId:new FormControl({value: '', disabled: true}),
      openBetID:new FormControl({value: '', disabled: true}),
      fanzoneBanner: new FormControl(this.fanzone.fanzoneBanner, [Validators.required]),
      fanzoneBannerDesktop: new FormControl(this.fanzone.fanzoneConfiguration.fanzoneBannerDesktop, [Validators.required]),
      assetManagementLink: new FormControl(this.fanzone.assetManagementLink, [Validators.required]),
      location: new FormControl(this.fanzone.location, [Validators.required]),
      primaryCompetitionId: new FormControl(this.fanzone?.primaryCompetitionId, [Validators.required]),
      secondaryCompetitionId: new FormControl(this.fanzone?.secondaryCompetitionId),
      clubIds:new FormControl({value: '', disabled: true}),
      hexColorCode: new FormControl(this.fanzone?.hexColorCode, [Validators.required, Validators.pattern("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}$)")]),
      is21stOrUnlistedFanzoneTeam: new FormControl(this.fanzone.is21stOrUnlistedFanzoneTeam),
    })
    if(this.fanzone?.is21stOrUnlistedFanzoneTeam) {
      this.form.controls['teamId'].setValue('FZ001');
      this.fanzone.teamId='FZ001'
    }
  }
  
  /**
   * creates the Fanzone
   * @returns void
   */
  public createFanzone(): void {
    this.fanzonesAPIService.createFanzone(this.fanzone)
      .subscribe(data => {
        this.finishCampaignCreation(data.body.id);
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  /**
   * Redirect to fanzone-edit page
   * @param id  { id }
   * @returns void
   */
  finishCampaignCreation(id: string): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Fanzone is Created and Stored. Continue to Configure',
      closeCallback() {
        self.router.navigate([`fanzones/fanzone/${id}`]);
      }
    });
  }

  /**
   * checks if the form is valid
   * @returns string
   */
  isValidModel(): boolean {
    if(this.fanzone?.is21stOrUnlistedFanzoneTeam)
    {
      this.generateUnlistedGameForm();
    }
    else
    this.generateForm();
    return this.form && this.form.valid;
  }
  
}
