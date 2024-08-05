import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';

import {DialogService} from '../../../../shared/dialog/dialog.service';
import {Competition} from '../../../../client/private/models';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {CompetitionAddComponent} from '../competition-add/competition-add.component';
import {DataTableColumn} from '../../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../../client/private/models/activeInactiveExpired.model';
import {AppConstants} from '../../../../app.constants';

@Component({
  templateUrl: './competitions-list.component.html'
})
export class CompetitionsListComponent implements OnInit {
  competitions: Array<Competition> = [];
  searchField: '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Competition Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'URL Structure',
      property: 'uri'
    },
    {
      name: 'Active',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    private dialogService: DialogService,
    private dialog: MatDialog,
    private bigCompetitionApiService: BigCompetitionAPIService) {
  }

  get competitionsAmount(): ActiveInactiveExpired {
    const activeCompetitions = this.competitions && this.competitions.filter(competition => competition.enabled);
    const activeAmount = activeCompetitions && activeCompetitions.length;
    const inactiveAmount = this.competitions.length - activeAmount;

    return {
      active: activeAmount,
      inactive: inactiveAmount
    };
  }

  ngOnInit() {
    this.bigCompetitionApiService.getCompetitionsList()
      .subscribe((data: any) => {
        this.competitions = data.body;
      });
  }

  /**
   * Opens modal dialog for new competition creation.
   */
  public createCompetition(): void {
    const dialogRef = this.dialog
      .open(CompetitionAddComponent, { width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH });

    dialogRef.afterClosed().subscribe(newCompetition => {
      if (newCompetition) {
        newCompetition.name = _.trim(newCompetition.name);
        newCompetition.uri = _.trim(newCompetition.uri);
        newCompetition.background = _.trim(newCompetition.background);
        newCompetition.title = _.trim(newCompetition.title);

        this.bigCompetitionApiService.createCompetition(newCompetition)
          .map((competition: HttpResponse<Competition>) => {
            return competition.body;
          })
          .subscribe((competition: Competition) => {
            if (competition) {
              this.competitions.push(competition);

              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Big Competition is Created and Stored'
              });
            }
          });
      }
    });
  }

  /**
   * handle deleting competition
   * @param {Competition} competition
   */
  public removeCompetition(competition: Competition): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Big Competition',
      message: `Are You Sure You Want to Remove Competition "${competition.name}"?`,
      yesCallback: () => {
        this.sendRemoveRequest(competition);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Competition} competition
   */
  public sendRemoveRequest(competition: Competition): void {
    this.bigCompetitionApiService.deleteCompetition(competition.id)
      .subscribe((data: any) => {
        this.competitions.splice(this.competitions.indexOf(competition), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Big Competition is Removed'
        });
      });
  }
}
