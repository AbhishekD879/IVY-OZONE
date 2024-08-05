import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@root/app/client/private/models';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { forkJoin } from 'rxjs';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';
import { SeasonData } from '@root/app/one-two-free/constants/otf.model';

@Component({
  selector: 'app-gamification-list',
  templateUrl: './gamification-list.component.html',
  styleUrls: ['./gamification-list.component.scss']
})

export class GamificationListComponent implements OnInit {

  constructor(private router: Router, private seasonApiService: SeasonsApiService,
    private dialogService: DialogService) { }

  seasonGamificationData: SeasonData[];

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Season Name',
      property: 'seasonName',
      link: {
        hrefProperty: 'id',
        path: 'gamification'
      },
      type: 'link'
    }
  ];
  filterProperties: Array<string> = [
    'seasonName'
  ];

  paginationLimitOptions: number[] = [5, 10, 25, 50];
  paginationLimit: number = this.paginationLimitOptions[1];
  searchField: string = '';

  ngOnInit(): void {
    this.seasonApiService.getAllGamification().subscribe((data) => {
      this.seasonGamificationData = _.chain(data.body).orderBy('displayFrom','desc').value();
      this.seasonGamificationData.map(game =>{
        game.highlighted = this.isRemoveCheckboxEnabled(game);
    })
  })
  }

/**
 * Navigation to Create gamification page
 */
  navigateToCreateGamification() {
    this.router.navigateByUrl('/one-two-free/otf-gamification/create');
  }

/**
 * remove gamification
 * @Params gamification
 */
  removeGamification(seasonGamification:SeasonData) {
    if (this.isRemoveCheckboxEnabled(seasonGamification)) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Gamification',
        message: 'Please note, not allowed to edit/modify/delete active season'
      })
    } else {
      this.dialogService.showConfirmDialog({
        title: 'Remove gamification',
        message: 'Are You Sure You Want to Remove the gamification?',
        yesCallback: () => {
          this.seasonApiService.deleteGamification(seasonGamification.id).subscribe(data => {
            this.seasonGamificationData.splice(this.seasonGamificationData.indexOf(seasonGamification), 1);
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'gamification is Removed.'
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
      title: `Remove gamification (${seasonIds.length})`,
      message: 'Are You Sure You Want to Remove  selected gamification?',
      yesCallback: () => {
        forkJoin(seasonIds.map(id => this.seasonApiService.deleteGamification(id)))
          .subscribe(() => {
            seasonIds.forEach((id) => {
              const index = _.findIndex(this.seasonGamificationData, { id: id });
              this.seasonGamificationData.splice(index, 1);
            });
          });
      }
    });
  }

  /* Validation to enable remove Button  
  *  @param seasonData
  */
  isRemoveCheckboxEnabled(seasonData:SeasonData): boolean {
    return ((new Date(seasonData.displayFrom).getTime() <= new Date().getTime())
      && (new Date(seasonData.displayTo).getTime() > new Date().getTime()));
  }
}