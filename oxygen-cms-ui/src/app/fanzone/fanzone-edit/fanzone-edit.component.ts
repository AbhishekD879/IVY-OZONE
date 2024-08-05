import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models';
import { Fanzone } from '@app/client/private/models/fanzone.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { FANZONE_ADDITIONAL } from '@app/fanzone/constants/fanzone.constants';
import { ErrorService } from '@app/client/private/services/error.service';
import { AbstractControl, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { DialogService } from '@app/shared/dialog/dialog.service';

@Component({
  selector: 'app-fanzone-edit',
  templateUrl: './fanzone-edit.component.html'
})
export class FanzoneEditComponent implements OnInit {
  public readonly FANZONE_ADDITIONAL = FANZONE_ADDITIONAL;
  isReady: boolean;
  id: string;
  fanzone: Fanzone;
  public form: FormGroup;

  public breadcrumbsData: Breadcrumb[];

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private dialogService: DialogService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getFanzoneDetails(this.id);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.deleteFanzone(this.id);
        break;
      case 'save':
        this.updateFanzoneDetails(this.id, this.fanzone);
        break;
      case 'revert':
        this.getFanzoneDetails(this.id);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public validationHandler(): boolean {
    if(this.fanzone?.is21stOrUnlistedFanzoneTeam)
    {
      this.generateUnlistedGameForm();
    }
    else
    this.generateForm();
    return this.form && this.form.valid;
  }

  getFanzoneDetails(id: string) {
    this.fanzonesAPIService.getFanzoneDetails(id).subscribe((fanzone: any) => {
      this.breadcrumbsData = [
        { label: 'Fanzone', url: '/fanzones' },
        { label: fanzone.body.name, url: `/fanzones/${this.id}` }
      ];
      this.fanzone = fanzone.body;
      this.isReady = true; 
      if(this.fanzone.is21stOrUnlistedFanzoneTeam)
      {
        this.generateUnlistedGameForm();
      }
      else   
      this.generateForm();
    }, error => {
      console.error(error.message);
    });
  }

  generateForm(): void {
    this.form = new FormGroup({
      active: new FormControl(this.fanzone?.active, [Validators.required]),
      name: new FormControl(this.fanzone?.name, [Validators.required]),
      launchBannerUrl: new FormControl(this.fanzone?.launchBannerUrl, [Validators.required]),
      launchBannerUrlDesktop: new FormControl(this.fanzone?.fanzoneConfiguration.launchBannerUrlDesktop, [Validators.required]),
      teamId: new FormControl(this.fanzone?.teamId, [Validators.required, forbiddenNameValidator(/FZ001/i)],),
      openBetID: new FormControl(this.fanzone?.openBetID, [Validators.required]),
      fanzoneBanner: new FormControl(this.fanzone?.fanzoneBanner, [Validators.required]),
      fanzoneBannerDesktop: new FormControl(this.fanzone?.fanzoneConfiguration.fanzoneBannerDesktop, [Validators.required]),
      assetManagementLink: new FormControl(this.fanzone?.assetManagementLink, [Validators.required]),
      location: new FormControl(this.fanzone?.location, [Validators.required]),
      primaryCompetitionId: new FormControl(this.fanzone?.primaryCompetitionId, [Validators.required]),
      secondaryCompetitionId: new FormControl(this.fanzone?.secondaryCompetitionId),
      clubIds: new FormControl(this.fanzone?.clubIds),
      hexColorCode: new FormControl(this.fanzone?.hexColorCode, [Validators.required, Validators.pattern("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}$)")]),
      nextGamesLbl: new FormControl(this.fanzone?.nextGamesLbl, [Validators.required]),
      outRightsLbl: new FormControl(this.fanzone?.outRightsLbl, [Validators.required]),
      premierLeagueLbl: new FormControl(this.fanzone?.premierLeagueLbl, [Validators.required]),
      showNowNext: new FormControl(this.fanzone?.fanzoneConfiguration.showNowNext, [Validators.required]),
      showCompetitionTable: new FormControl(this.fanzone?.fanzoneConfiguration.showCompetitionTable),
      showStats: new FormControl(this.fanzone?.fanzoneConfiguration.showStats, [Validators.required]),
      showClubs: new FormControl(this.fanzone?.fanzoneConfiguration.showClubs, [Validators.required]),
      showGames: new FormControl(this.fanzone?.fanzoneConfiguration.showGames),
      showSlotRivals: new FormControl(this.fanzone?.fanzoneConfiguration.showSlotRivals),
      showScratchCards: new FormControl(this.fanzone?.fanzoneConfiguration.showScratchCards),
      sportsRibbon: new FormControl(this.fanzone?.fanzoneConfiguration.sportsRibbon, [Validators.required]),
      atozMenu: new FormControl(this.fanzone?.fanzoneConfiguration.atozMenu, [Validators.required]),
      homePage: new FormControl(this.fanzone?.fanzoneConfiguration.homePage, [Validators.required]),
      footballHome: new FormControl(this.fanzone?.fanzoneConfiguration.footballHome, [Validators.required]),
      is21stOrUnlistedFanzoneTeam: new FormControl(this.fanzone?.is21stOrUnlistedFanzoneTeam),
      showBetsBasedOnOtherFans: new FormControl(this.fanzone.fanzoneConfiguration.showBetsBasedOnOtherFans),
      showBetsBasedOnYourTeam: new FormControl(this.fanzone.fanzoneConfiguration.showBetsBasedOnYourTeam),
    })
    function forbiddenNameValidator(nameRe: RegExp): ValidatorFn {
      return (control: AbstractControl): ValidationErrors | null => {
        const forbidden = nameRe.test(control.value);
        return forbidden ? {forbiddenName: {value: control.value}} : null;
      };
    }
  }
  
  toggleGamesSwitch(event) {
    if(!event.checked) {
      this.fanzone.fanzoneConfiguration.showScratchCards = false;
      this.fanzone.fanzoneConfiguration.showSlotRivals = false;
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
      hexColorCode: new FormControl(this.fanzone.hexColorCode, [Validators.required, Validators.pattern("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}$)")]),
      nextGamesLbl: new FormControl(this.fanzone.nextGamesLbl, [Validators.required]),
      outRightsLbl: new FormControl(this.fanzone.outRightsLbl, [Validators.required]),
      premierLeagueLbl: new FormControl(this.fanzone.premierLeagueLbl, [Validators.required]),
      showNowNext: new FormControl(this.fanzone.fanzoneConfiguration.showNowNext, [Validators.required]),
      showCompetitionTable: new FormControl(this.fanzone.fanzoneConfiguration.showCompetitionTable),
      showStats: new FormControl(this.fanzone.fanzoneConfiguration.showStats, [Validators.required]),
      showClubs: new FormControl(this.fanzone.fanzoneConfiguration.showClubs, [Validators.required]),
      showGames: new FormControl(this.fanzone.fanzoneConfiguration.showGames),
      showSlotRivals: new FormControl(this.fanzone?.fanzoneConfiguration.showSlotRivals),
      showScratchCards: new FormControl(this.fanzone?.fanzoneConfiguration.showScratchCards),
      sportsRibbon: new FormControl(this.fanzone.fanzoneConfiguration.sportsRibbon, [Validators.required]),
      atozMenu: new FormControl(this.fanzone.fanzoneConfiguration.atozMenu, [Validators.required]),
      homePage: new FormControl(this.fanzone.fanzoneConfiguration.homePage, [Validators.required]),
      footballHome: new FormControl(this.fanzone.fanzoneConfiguration.footballHome, [Validators.required]),
      is21stOrUnlistedFanzoneTeam: new FormControl(this.fanzone.is21stOrUnlistedFanzoneTeam),
      showBetsBasedOnOtherFans: new FormControl(this.fanzone.fanzoneConfiguration.showBetsBasedOnOtherFans),
      showBetsBasedOnYourTeam: new FormControl(this.fanzone.fanzoneConfiguration.showBetsBasedOnYourTeam),
    })
    if(this.fanzone?.is21stOrUnlistedFanzoneTeam) {
      this.fanzone.teamId='FZ001'
      this.form.controls['teamId'].setValue('FZ001');
      this.fanzone.openBetID = '',
      this.fanzone.clubIds = '';
    }
  }

  updateFanzoneDetails(id: string, fanzone: Fanzone) {
    this.fanzonesAPIService.updateFanzoneDetails(id, fanzone).subscribe((fanzoneData: any) => {
      this.fanzone = fanzoneData.body;
      this.actionButtons.extendCollection(this.fanzone);
      this.dialogService.showNotificationDialog({
        title: 'Fanzone Saved'
      });
    }, error => {
      this.errorService.emitError(error.error.message || 'Something went wrong');
    });
  }

  deleteFanzone(id: string) {
    this.fanzonesAPIService.deleteFanzone(id).subscribe(() => {
      this.router.navigate(['fanzones']);
    }, error => {
      console.error(error.message);
    });
  }

}
