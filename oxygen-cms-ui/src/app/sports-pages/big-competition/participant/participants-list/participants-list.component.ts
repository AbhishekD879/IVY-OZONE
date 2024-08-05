import {Component, Input, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params} from '@angular/router';

import {DialogService} from '../../../../shared/dialog/dialog.service';
import {ParticipantCreateComponent} from '../participant-create/participant-create.component';
import {CompetitionParticipant} from '../../../../client/private/models';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {AppConstants} from '../../../../app.constants';

@Component({
  selector: 'participants-list',
  templateUrl: './participants-list.component.html'
})
export class ParticipantsListComponent implements OnInit {
  @Input() participants: CompetitionParticipant[] = [];

  public searchField: '';
  public dataTableColumns: any[] = [
    {
      name: 'OB Name',
      property: 'obName',
      link: {
        hrefProperty: 'id',
        path: 'participant/'
      },
      type: 'link'
    },
    {
      name: 'Front End Full Name',
      property: 'fullName'
    },
    {
      name: 'Name Abbreviation',
      property: 'abbreviation'
    },
    {
      name: 'Flag/Logo',
      property: 'svgId',
      type: 'boolean'
    }
  ];

  filterProperties: string[] = ['obName'];

  constructor(
    private dialog: MatDialog,
    private dialogService: DialogService,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService) {
  }

  ngOnInit(): void {
  }

  public createParticipant(): void {
    const dialogRef = this.dialog
      .open(ParticipantCreateComponent, { width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH });

    dialogRef.afterClosed()
      .subscribe(newParticipant => {
        if (newParticipant) {
          this.activatedRoute.params.subscribe((params: Params) => {
            this.bigCompetitionApiService.createParticipant(params.competitionId, newParticipant)
              .map((participant: HttpResponse<CompetitionParticipant>) => {
                return participant.body;
              })
              .subscribe((participant: CompetitionParticipant) => {
                if (participant) {
                  this.participants.push(participant);
                  this.dialogService.showNotificationDialog({
                    title: 'Save Completed',
                    message: 'Participant Details were Created and Stored'
                  });
                }
              });
           });
        }
      });
  }

  /**
   * Shows confirmation dialog before removing competition's participant.
   * @param {Object} participant
   */
  public removeParticipant(participant: CompetitionParticipant): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Participant Details',
      message: `Are You Sure You Want to Remove Participant Details "${participant.obName}"?`,
      yesCallback: () => {
        this.sendRemoveRequest(participant);
      }
    });
  }

  /**
   * Sends DELETE API request to remove competition's participant.
   * @param {CompetitionParticipant} participant
   */
  private sendRemoveRequest(participant: CompetitionParticipant): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteParticipant(params.competitionId, participant.id)
        .subscribe(() => {
          this.participants.splice(this.participants.indexOf(participant), 1);
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Participant Details were Removed'
          });
        });
    });
  }
}
