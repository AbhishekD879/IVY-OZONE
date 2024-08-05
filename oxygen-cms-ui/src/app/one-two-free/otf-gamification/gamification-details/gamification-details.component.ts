import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormArray } from '@angular/forms';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { GamificationData, SeasonData, Team } from '@root/app/one-two-free/constants/otf.model';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';
import { AssetManagement } from '@root/app/client/private/models/assetManagement.model';

@Component({
  selector: 'app-gamification-details',
  templateUrl: './gamification-details.component.html',
  styleUrls: ['./gamification-details.component.scss']
})
export class GamificationDetailsComponent implements OnInit {

  constructor(
    private activateRoute: ActivatedRoute,
    private seasonApiService: SeasonsApiService,
    private dialogService: DialogService,
    private router: Router,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }
  @ViewChild('actionButtons') actionButtons;
  gamificationData = new GamificationData();
  isCreate: boolean = false;
  breadcrumbsData: Breadcrumb[];
  teams = new Array<Team>();
  isActive = false;
  seasons = new Array<SeasonData>();
  selectedSeason: string;
  nextDisplayName = false;
  nextSvg = false;
  editRowIndex: number;
  teamsArray: FormArray;
  formDataLoaded: boolean = false;
  selectedSeasonisValid: boolean = true;
  selectedTeam: string;

  ngOnInit(): void {
    this.loadSeasons();
    this.loadTeams();
  }

  /**
    * Get svgid for the svg html string
    * @param svgString
    * @returns { string }
    */
  private getSvgId(svgString: string): string {
    const emptyDiv = document.createElement('div');
    emptyDiv.innerHTML = svgString;
    return emptyDiv.querySelector('symbol').id || '';
  }

  /**
   * load all the teamData 
   * @param null
   */
  loadTeams() {
    this.seasonApiService.getAllTeams()
      .map(response => {
        return response.body;
      })
      .subscribe((assetsData: AssetManagement[]) => {
        assetsData.map((assetData) => {
          const displayName: string = assetData.teamName ? assetData.teamName : '';
          const svg: string = assetData.teamsImage ? assetData.teamsImage.svg : '';
          const svgId: string = assetData.teamsImage ? this.getSvgId(assetData.teamsImage.svg) : '';
          const assetManagementObjectId: string = assetData.id;
          this.teams.push({ displayName, svg, svgId, assetManagementObjectId })
        })
      }, error => {
        console.error(error.message);
      });

  };

  /**
   * load initial Data for gamification
   * @param id 
   */
  loadInitialData(id: string) {
    this.seasonApiService.getGamificationById(id).
      map((response: HttpResponse<GamificationData>) => {
        return response.body;
      }).subscribe((data: GamificationData) => {
        this.selectedSeason = data.seasonId;
        this.gamificationData = data;
        this.breadcrumbsData = [{
          label: `Gamification`,
          url: '/one-two-free/otf-gamification'
        }, {
          label: this.gamificationData.seasonName,
          url: `/one-two-free/otf-gamification/gamification/${this.gamificationData.id}`
        }];
        this.formDataLoaded = true;
        this.selectedSeasonisValid = true;
        if (this.seasons) {
          const seasonSel = this.seasons.find(season => season.id == this.gamificationData.seasonId);
          this.isActive = this.checkIfSeasonisActive(seasonSel);
        }
      }, (err) => {

      })
  }

  /**
    * remove team
    * @param i:number
    */
  removeTeams(i: number) {
    i == this.editRowIndex || this.editRowIndex != this.gamificationData.teams.length - 1 ?
      this.editRowIndex = -1 : this.editRowIndex = this.editRowIndex - 1;
    this.gamificationData.teams.splice(i, 1);
  }

  /**
    * Adding teams table if empty and adding rows if already exist
    * @param null
    */
  addTeams(i) {
    this.gamificationData.teams.push(new Team());
    this.editRowIndex = this.gamificationData.teams.length - 1;
  }

  /**
    * Save row edit 
    * @param index team
    */
  saveRowEdit(index: number, team: Team) {
    this.gamificationData.teams[index] = team;
    this.nextDisplayName = false;
    this.nextSvg = false;
    this.selectedTeam = '';
  }

  /**
  * select team from dropDown
  * @param value, i
  */
  onSelectTeams(value, i: number) {
    if (this.gamificationData.teams.filter(team => team.assetManagementObjectId === value.assetManagementObjectId).length > 0) {
      this.gamificationData.teams.pop();
      this.dialogService.showNotificationDialog({
        title: 'Teams Error',
        message: 'Team is already selected. Please select other team to add.'
      })
    } else {
      this.gamificationData.teams[i] = value;
      this.editRowIndex = -1;
      this.saveRowEdit(i, value);
      this.nextDisplayName = false;
    }
  }

  /**
    * alert user onSelectSeason 
    * @param val
    */
  onSelectSeason(val) {
    const seasonSel = this.seasons.find(season => season.id == val.value);
    if (seasonSel.gamificationLinked) {
      this.alertUer('Selected season is already linked to other gamification.Please Select a other Season.');
      this.selectedSeasonisValid = false;
    } else if (this.checkIfSeasonisActive(seasonSel)) {
      this.alertUer('Please note, not allowed to edit/modify/delete Active season');
      this.selectedSeasonisValid = false;
    } else if (this.checkIfSeasonExpired(seasonSel)) {
      this.alertUer('Please note, not allowed to edit/modify Expired season');
      this.selectedSeasonisValid = false;
    } else {
      this.selectedSeason = val.value;
      this.gamificationData.seasonId = val.value;
      this.selectedSeasonisValid = true;
    }
  }

  /**
    * alertUer
    * @param message
    */
  alertUer(message: string) {
    this.dialogService.showNotificationDialog({
      title: 'Season Error',
      message: message
    })
  }

  /**
    *  Method to fetch all Seasons
    * @param null
    * @return seasons
    */
  loadSeasons() {
    this.seasonApiService.getAllSeasons().
      map((response: HttpResponse<SeasonData[]>) => {
        return response.body;
      }).subscribe(data => {
        this.seasons = data;
        this.activateRoute.params.subscribe((params: Params) => {
          if (params['id'] && params['id'] !== null) {
            this.loadInitialData(params['id']);
          } else {
            this.gamificationData.badgeTypes = [{
              name: 'Primary',
              numberOfBadges: null,
              congratsMsg: '',
              prizeType: '',
              amount: null
            }, {
              name: 'Secondary',
              numberOfBadges: null,
              congratsMsg: '',
              prizeType: '',
              amount: null
            }]
            this.isCreate = true;
            this.breadcrumbsData = [{
              label: `Gamification`,
              url: '/one-two-free/otf-gamification'
            }, {
              label: 'Create Gamification',
              url: `/otf-gamification/create`
            }];
          }
        });
      });
  }

  /**
    * Submit (put/post) on creation or updation of gamification
    * @param callType
    * @return seasons
    */
  createEditGamification(callType: string) {
    if (callType == 'create') {
      this.seasonApiService.createGamification(this.gamificationData).subscribe(data => {
        this.gamificationData = data.body;
        this.isCreate = false;
        this.router.navigateByUrl(`/one-two-free/otf-gamification/gamification/${this.gamificationData.id}`)
        this.successDialog('Created');
      })
    } else {
      this.seasonApiService.updateGamification(this.gamificationData).subscribe(data => {
        this.gamificationData = data.body;
        this.actionButtons.extendCollection(this.gamificationData);
        this.nextDisplayName = false;
        this.nextSvg = false;
        this.selectedTeam = '';
        this.successDialog('Updated');
      })
    }
  }

  /**
    * Show the successDialog
    * @param type
    */
  successDialog(type: string) {
    this.dialogService.showNotificationDialog({
      title: 'Gamification',
      message: 'Gamification ' + type + ' Succesfully!! '
    });
  }

  /**
     * action handler for button
     * @param event
     */
  actionsHandler(event) {
    switch (event) {
      case 'save':
        this.createEditGamification('update');
        break;
      case 'revert':
        this.loadInitialData(this.gamificationData.id);
        break;
      case 'remove':
        this.removeGamification(this.gamificationData);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * Delete Gamifications linked to non-active seasons
   * @param gamification
   */
  removeGamification(gamification: GamificationData) {
    const self = this;
    this.seasonApiService.deleteGamification(gamification.id).subscribe(data => {
      this.dialogService.showNotificationDialog({
        title: 'Remove Completed',
        message: 'Gamification is Removed.',
        closeCallback() {
          self.router.navigateByUrl('/one-two-free/otf-gamification');
        }
      });
    });
  }

  /**
   *  Validate form model for button actions
   * @param gamificationData
   * @return boolean
   */
  isValidModel(gamificationData: GamificationData): boolean {
    return gamificationData.seasonId &&
      gamificationData.teams.length > 0 &&
      ((gamificationData.badgeTypes.filter(badgeType => {
        return badgeType.congratsMsg.length > 0 && badgeType.congratsMsg.length <= 100
          && badgeType.amount > 0 && badgeType.numberOfBadges > 0 && badgeType.numberOfBadges < 1000 && badgeType.prizeType.length > 0
      })).length == 2) && this.selectedSeasonisValid;
  }

  /**
 * To check if season is Active
 * @param season
 */
  checkIfSeasonisActive(season: SeasonData) {
    return ((new Date(season.displayFrom).getTime() <= new Date().getTime())
      && (new Date(season.displayTo).getTime() > new Date().getTime()));
  }


  /**
   * To check if season is expired
   * @param season
   */
  checkIfSeasonExpired(season: SeasonData) {
    return (new Date(season.displayTo).getTime() < new Date().getTime());
  }
}