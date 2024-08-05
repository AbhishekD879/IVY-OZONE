import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@root/app/client/private/models';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { forkJoin } from 'rxjs';
import { SeasonData } from '@root/app/one-two-free/constants/otf.model';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';

@Component({
  selector: 'app-season-view',
  templateUrl: './season-view.component.html',
  styleUrls: ['./season-view.component.scss']
})
export class SeasonViewComponent implements OnInit {

  constructor(private router: Router,
    private seasonApiService: SeasonsApiService,
    private dialogService: DialogService) { }

  paginationLimitOptions: number[] = [5, 10, 25, 50];
  paginationLimit: number = this.paginationLimitOptions[1];
  searchField: string = '';
  seasonData = new Array<SeasonData>();

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Season Name',
      property: 'seasonName',
      link: {
        hrefProperty: 'id',
        path: 'season'
      },
      type: 'link'
    },
    {
      name: 'Active',
      property: 'isActive',
      type: 'boolean'
    }
  ];
  filterProperties: Array<string> = [
    'seasonName'
  ];

  ngOnInit(): void {
    this.seasonApiService.getAllSeasons().subscribe((data) => {
      this.seasonData = _.chain(data.body).orderBy('displayFrom','desc').value().map(season => {
       season.highlighted = season.isActive = this.checkIfSeasonisActive(season);
        return season;
      });
    })
  }

  /**
   * Navigation to Create Season Page
   */
  navigateToCreateSeason() {
    this.router.navigateByUrl('/one-two-free/otf-seasons/create');
  }

  /**
   * Method to delete season
   * @param season 
   */
  removeSeason(season: SeasonData) {
    if (season.isActive) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Season',
        message: 'Active Season Cannot be Deleted.'
      })
    } else if (season.gamificationLinked || season.gameLinked) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Error',
        message: 'Season is linked to Gamification/Game. Unlink to remove season.\n' + 'Games Linked:' + season.gameLinked
      })
    } else {
      this.dialogService.showConfirmDialog({
        title: 'Remove Season',
        message: 'Are You Sure You Want to Remove the Season?',
        yesCallback: () => {
          this.seasonApiService.deleteSeason(season.id).subscribe(data => {
            this.seasonData.splice(this.seasonData.indexOf(season), 1);
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Season is Removed.'
            });
          })
        }
      });
    }
  }

  /**
  * handle deleting seasons Multi
  * @param seasonIds
  */
  removeHandlerMulty(seasonIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Seasons (${seasonIds.length})`,
      message: 'Are You Sure You Want to Remove  selected seasons?',
      yesCallback: () => {
        forkJoin(seasonIds.map(id => this.seasonApiService.deleteSeason(id)))
          .subscribe(() => {
            seasonIds.forEach((id) => {
              const index = _.findIndex(this.seasonData, { id: id });
              this.seasonData.splice(index, 1);
            });
          });
      }
    });
  }

  /**
   * Validation to enable remove Button
   * @param seasonData 
   * @returns boolean
   */
  isRemoveCheckboxEnabled(seasonData : SeasonData): boolean {
    return seasonData.isActive || seasonData.gameLinked || seasonData.gamificationLinked;
  }

    /**
   * check if season is active 
   * @Param : season
   */
     checkIfSeasonisActive(season: SeasonData) {
      return ((new Date(season.displayFrom).getTime() <= new Date().getTime())
        && (new Date(season.displayTo).getTime() > new Date().getTime()));
    }
  
}