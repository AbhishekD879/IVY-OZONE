import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Breadcrumb, DateRange } from '@root/app/client/private/models';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { SeasonData } from '@root/app/one-two-free/constants/otf.model';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';

@Component({
  selector: 'app-season-edit',
  templateUrl: './season-edit.component.html',
  styleUrls: ['./season-edit.component.scss']
})
export class SeasonEditComponent implements OnInit {

  constructor(private activateRoute: ActivatedRoute,
    private dialogService: DialogService,
    private seasonApiService: SeasonsApiService,
    private router: Router,
    private globalLoaderService: GlobalLoaderService) {
    this.isValidModel = this.isValidModel.bind(this);
  }
  @ViewChild('actionButtons') actionButtons;
  season = new SeasonData();
  seasonForm: FormGroup;
  isCreate: boolean;
  breadcrumbsData: Breadcrumb[];
  apiFlag: boolean = false;
  isActive = false;
  isDate: boolean = false;
  formDataLoaded: boolean = false;
  public existingSeasonFromDate: string;
  public existingSeasonToDate: string;


  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.activateRoute.params.subscribe((params: Params) => {
      if (params['id'] && params['id'] !== null) {
        this.isCreate = false;
        this.loadInitialData(params['id']);
      } else {
        this.globalLoaderService.hideLoader();
        this.isCreate = true;
        this.isDate = true;
        this.breadcrumbsData = [{
          label: `Seasons`,
          url: '/one-two-free/otf-seasons'
        }, {
          label: 'Create Season',
          url: `/otf-seasons/create`
        }];
      }
    });
  }

  /**
   * Method to get the season data by id
   * @Param : seasonId
   */
  loadInitialData(seasonId: string) {
    this.seasonApiService.getSingleSeasonData(seasonId).
      map((response: HttpResponse<SeasonData>) => {
        return response.body;
      })
      .subscribe((data: SeasonData) => {
        this.season = data;
        this.existingSeasonFromDate = this.season.displayFrom;
        this.existingSeasonToDate = this.season.displayTo;
        this.breadcrumbsData = [{
          label: `Seasons`,
          url: '/one-two-free/otf-seasons'
        }, {
          label: this.season.seasonName,
          url: `/one-two-free/otf-seasons/season/${this.season.id}`
        }];
        this.isActive = this.checkIfSeasonisActive(this.season);
        this.isDate = true;
        this.formDataLoaded = true;
        this.globalLoaderService.hideLoader();
      }, (err) => {
        console.log(err);
      })
  }

  /**
   * Method to get the season data by id
   * @Param : data
   */
  handleDisplayDateUpdate(data: DateRange): void {
    this.season['displayFrom'] = new Date(data.startDate).toISOString();
    this.season['displayTo'] = new Date(data.endDate).toISOString();
  }


  /**
   * Method call on Create or Update season
   * @Param : callType
   */
  createEditSeason(callType: string) {
    if (callType == 'create') {
      this.seasonApiService.createSeason(this.season).subscribe(data => {
        this.season = data.body;
        this.isCreate = false;
        this.isActive = this.checkIfSeasonisActive(this.season);
        this.router.navigateByUrl(`/one-two-free/otf-seasons/season/${this.season.id}`)
        this.successDialog('Created');
      })
    } else {
      this.apiFlag = this.checkDateChanged();
      this.seasonApiService.updateSeason(this.season, this.apiFlag).subscribe(data => {
        this.apiFlag = false;
        this.season = data.body;
        this.actionButtons.extendCollection(this.season);
        this.formDataLoaded = true;
        this.isActive = this.checkIfSeasonisActive(this.season);
        this.successDialog('Updated');
      })
    }
  }

  /**
  * Date Check for existing Season
  */
  checkDateChanged() {
    if (this.existingSeasonFromDate) {
      return (new Date(this.existingSeasonFromDate).toISOString()
        !== new Date(this.season.displayFrom).toISOString()) ||
        (new Date(this.existingSeasonToDate).toISOString()
          !== new Date(this.season.displayTo).toISOString());
    } else return false;
  }

  /**
   *  Confirmation dialog on successful creation or updation of Season info
   * @Param : type 
   */
  successDialog(type: string) {
    this.dialogService.showNotificationDialog({
      title: 'Seasons',
      message: 'Season ' + type + ' Succesfully!! '
    });

  }

  /**
   *   Action Handler for Action buttons
   * @Param : event 
   */
  actionsHandler(event) {
    switch (event) {
      case 'save':
        this.createEditSeason('update');
        break;
      case 'revert':
        this.loadInitialData(this.season.id);
        break;
      case 'remove':
        this.removeSeason(this.season);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * validation for action buttons (save)
   * @Param : season 
   */
  isValidModel(season: SeasonData) {
    return !!(season.seasonName &&
      season.seasonName.length > 0 &&
      !(season.seasonName.length > 50) &&
      season.seasonInfo &&
      season.seasonInfo.length > 0 &&
      !(season.seasonInfo.length > 200) && this.isEndDateValid() &&
      (this.checkDateChanged() ? !this.isPastDate() : true));
  }

  /**
   * Delete Season
   * @Param : season 
   */
  removeSeason(season: SeasonData) {
    const self = this;
    if (season.gamificationLinked || season.gameLinked) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Error',
        message: 'Season is linked to Gamification/Game. Unlink to remove season.\n' + 'Games Linked:' + season.gameLinked
      })
    } else {
      this.seasonApiService.deleteSeason(season.id).subscribe(data => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Season is Removed.',
          closeCallback() {
            self.router.navigateByUrl('/one-two-free/otf-seasons');
          }
        });
      });
    }
  }

  /**
   * check if season is active 
   * @Param : season
   */
  checkIfSeasonisActive(season: SeasonData) {
    return ((new Date(season.displayFrom).getTime() <= new Date().getTime())
      && (new Date(season.displayTo).getTime() > new Date().getTime()));
  }

  /**
   * Date Check for past dates
   */
  isPastDate() {
    return (new Date(this.season.displayFrom).getTime()
      <= new Date().getTime()) ||
      (new Date(this.season.displayTo).getTime()
        <= new Date().getTime());
  }

  isEndDateValid(){
    return (new Date(this.season.displayFrom).toISOString().substring(0,19))
    < (new Date(this.season.displayTo).toISOString().substring(0,19));
  }

   /**
   *Validation to show action button post form initialization
   *  @param: null
   */
   isLoadBadges() {
    return Object.keys(this.season).length > 0;
  }
}