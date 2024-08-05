import * as _ from 'lodash';

import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';

import {RoundNameModel} from '@app/client/private/models/roundName.model';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {RoundNamesAddComponent} from '../round-names-add/round-names-add.component';
import {BigCompetitionAPIService} from '../../../../../service/big-competition.api.service';
import {CompetitionModule} from '../../../../../../../client/private/models';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';

@Component({
  selector: 'app-round-names-list',
  templateUrl: './round-names-list.component.html'
})
export class RoundNamesListComponent implements OnInit {

  @Input() competitionModule: CompetitionModule;
  @Output() competitionModuleChange = new EventEmitter<CompetitionModule>();

  public roundNames: Array<RoundNameModel> = [];
  public searchField: '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'abbreviation',
        path: 'round-name/'
      },
      type: 'link'
    },
    {
      name: 'Abbreviation',
      property: 'abbreviation'
    },
    {
      name: 'Number Of Matches',
      property: 'number'
    },
    {
      name: 'Current',
      property: 'active',
      type: 'boolean'
    }
  ];
  public filterProperties: string[] = ['name', 'abbreviation'];

  constructor(
    private dialogService: DialogService,
    private dialog: MatDialog,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.roundNames = this.competitionModule.knockoutModuleData.rounds;
  }

  public createRoundName(): void {
    const dialog = this.dialog.open(RoundNamesAddComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: { rounds: this.roundNames }
    });

    dialog.afterClosed()
      .subscribe((roundName: RoundNameModel) => {
        if (roundName) {
          if (roundName.active) {
            this.competitionModule.knockoutModuleData.rounds.forEach(round => round.active = false);
          }

          this.competitionModule.knockoutModuleData.rounds.push(roundName);
          this.bigCompetitionApiService
            .putModuleChanges(this.competitionModule)
            .map((response: HttpResponse<CompetitionModule>) => {
              return response.body;
            })
            .subscribe((competitionModule: CompetitionModule) => {
              this.competitionModuleChange.emit(competitionModule);
              this.competitionModule = competitionModule;
              this.roundNames = competitionModule.knockoutModuleData.rounds;
              this.snackBar.open('Round Created', 'OK!', {
                duration: AppConstants.HIDE_DURATION
              });
            });
        }
      });
  }

  public removeRoundName(roundName: RoundNameModel): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Round',
      message: `Are You Sure You Want To Remove Round ${roundName.name}?`,
      yesCallback: () => {
        _.remove(this.competitionModule.knockoutModuleData.rounds, {abbreviation: roundName.abbreviation});
        _.remove(this.competitionModule.knockoutModuleData.events, {round: roundName.name});

        this.bigCompetitionApiService
          .putModuleChanges(this.competitionModule)
          .map((response: HttpResponse<CompetitionModule>) => {
            return response.body;
          })
          .subscribe((competitionModule: CompetitionModule) => {
            this.competitionModuleChange.emit(competitionModule);
            this.competitionModule = competitionModule;
            this.roundNames = competitionModule.knockoutModuleData.rounds;
            this.snackBar.open('Round Removed', 'OK!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
      }
    });
  }
}
