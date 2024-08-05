import * as _ from 'lodash';

import {Component, EventEmitter, Input, OnChanges, OnInit, Output} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import {HttpResponse} from '@angular/common/http';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {MatchCreateComponent} from '../match-create/match-create.component';
import {BigCompetitionAPIService} from '../../../../../service/big-competition.api.service';
import {KnockoutsMatch} from '@app/client/private/models/knockoutsmatch.model';
import {CompetitionModule} from '../../../../../../../client/private/models';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';

@Component({
  selector: 'matches-list',
  templateUrl: './matches-list.component.html'
})
export class MatchesListComponent implements OnInit, OnChanges {

  @Input() competitionModule: CompetitionModule;
  @Output() competitionModuleChange = new EventEmitter<CompetitionModule>();

  public searchField: '';
  public matches: KnockoutsMatch[] = [];
  public dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Event ID',
      property: 'eventId',
    },
    {
      name: 'Event Name',
      property: 'eventName',
    },
    {
      name: 'Home Team Name',
      property: 'homeTeam'
    },
    {
      name: 'Home Team Remark',
      property: 'homeTeamRemark'
    },
    {
      name: 'Away Team Name',
      property: 'awayTeam'
    },
    {
      name: 'Away Team Remark',
      property: 'awayTeamRemark'
    },
    {
      name: 'Venue',
      property: 'venue',
    },
    {
      name: 'Match Start Time',
      property: 'startTime',
      type: 'date'
    },
    {
      name: 'Specify Round',
      property: 'round',
    },
    {
      name: 'Round Stage Abbreviation',
      property: 'abbreviation',
      link: {
        hrefProperty: 'abbreviation',
        path: 'matches/'
      },
      type: 'link'
    }
  ];

  filterProperties: string[] = ['eventId', 'eventName', 'round', 'homeTeam', 'homeTeamRemark',
    'venue', 'awayTeam', 'awayTeamRemark', 'abbreviation'];

  constructor(
    private dialog: MatDialog,
    private dialogService: DialogService,
    private bigCompetitionApiService: BigCompetitionAPIService) {
  }

  ngOnInit(): void {
    this.matches = this.competitionModule.knockoutModuleData.events;
  }

  ngOnChanges(): void {
    this.matches = this.competitionModule.knockoutModuleData.events;
  }

  public createMatch(): void {
    const dialogRef = this.dialog.open(MatchCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: this.competitionModule
    });

    dialogRef.afterClosed()
      .subscribe((match: KnockoutsMatch) => {
        if (match) {
          this.competitionModule.knockoutModuleData.events.push(match);
          this.bigCompetitionApiService
            .putModuleChanges(this.competitionModule)
            .map((response: HttpResponse<CompetitionModule>) => {
              return response.body;
            })
            .subscribe((competitionModule: CompetitionModule) => {
              this.competitionModuleChange.emit(competitionModule);
              this.competitionModule = competitionModule;
              this.matches = this.competitionModule.knockoutModuleData.events;
              this.dialogService.showNotificationDialog({
                title: 'Module Saving',
                message: 'Competition Module is Successfully Saved'
              });
            });
        }
      });
  }

  /**
   * Shows confirmation dialog before removing knockouts's match.
   * @param {Object} match
   */
  public removeMatch(match: KnockoutsMatch): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Round Name',
      message: `Are You Sure You Want To Remove Round Name ${match.homeTeam} vs ${match.awayTeam}?`,
      yesCallback: () => {
        _.remove(this.competitionModule.knockoutModuleData.events, {abbreviation: match.abbreviation});

        this.bigCompetitionApiService
          .putModuleChanges(this.competitionModule)
          .map((response: HttpResponse<CompetitionModule>) => {
            return response.body;
          })
          .subscribe((competitionModule: CompetitionModule) => {
            this.competitionModuleChange.emit(competitionModule);
            this.competitionModule = competitionModule;
            this.matches = this.competitionModule.knockoutModuleData.events;
            this.dialogService.showNotificationDialog({
              title: 'Module Saving',
              message: 'Competition Module is Successfully Saved'
            });
          });
      }
    });
  }
}
