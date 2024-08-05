import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params, Router} from '@angular/router';
import * as _ from 'lodash';
import { MatSnackBar } from '@angular/material/snack-bar';

import {Breadcrumb, Competition, CompetitionParticipant, Filename} from '../../../../client/private/models';
import {DialogService} from '../../../../shared/dialog/dialog.service';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {ComponentCanDeactivate} from '../../../../client/private/interfaces/pending-changes.guard';
import {AppConstants} from '../../../../app.constants';

@Component({
  templateUrl: './participant-edit.component.html'
})
export class ParticipantEditComponent implements OnInit, ComponentCanDeactivate {
  public participant: CompetitionParticipant;
  public form: FormGroup;
  public participantNotFound: boolean = false;
  public svgFile: Filename;
  private originalModel: CompetitionParticipant;
  private competition: Competition;
  public breadcrumbsData: Breadcrumb[] = [];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private dialogService: DialogService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private snackBar: MatSnackBar) { }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData(reload?: boolean): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.getSingleParticipant(params.competitionId, params.participantId)
        .subscribe((data: any) => {
          this.competition = data.body || {};
          const participant = _.isArray(this.competition.competitionParticipants) && this.competition.competitionParticipants[0];

          if (participant) {
            this.updateBreadcrumbs(participant);
            this.form = new FormGroup({
              obName: new FormControl(participant.obName, [Validators.required]),
              fullName: new FormControl(participant.fullName, []),
              abbreviation: new FormControl(participant.abbreviation, [])
            });

            this.saveOriginalModel(participant);
            this.svgFile = {
              filename: participant.svgFilename,
              path: '',
              size: 0,
              filetype: ''
            };

            if (reload) {
              this.actionButtons.extendCollection(this.participant);
            }
          } else {
            this.participantNotFound = true;
          }
        }, () => {
          this.participantNotFound = true;
        });
    });
  }

  public isValidForm(participant: CompetitionParticipant): boolean {
    return participant.obName.length > 0;
  }

  private saveChanges(): void {
    this.bigCompetitionApiService
      .putParticipantChanges(this.participant)
      .map((response: HttpResponse<CompetitionParticipant>) => {
        return response.body;
      })
      .subscribe((participant: CompetitionParticipant) => {
        this.updateBreadcrumbs(participant);
        this.saveOriginalModel(participant);
        this.actionButtons.extendCollection(this.participant);

        this.dialogService.showNotificationDialog({
          title: 'Participant Details Saving',
          message: 'Participant Details are Successfully Saved'
        });
      });
  }

  private revertChanges(): void {
    this.loadInitData(true);
  }

  private removeParticipant(): void {
    this.bigCompetitionApiService.deleteParticipant(this.competition.id, this.participant.id)
      .subscribe(() => {
        this.originalModel = null;
        this.router.navigate([`/sports-pages/big-competition/${this.competition.id}`]);
      });
  }

  public canDeactivate(): boolean {
    return !this.originalModel || _.isEqual(this.originalModel, this.participant);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeParticipant();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private saveOriginalModel(participant: CompetitionParticipant): void {
    this.participant = participant;
    this.originalModel = _.extend({}, participant);
  }

  private updateBreadcrumbs(participant: CompetitionParticipant): void {
    const bigCompetitionPath = '/sports-pages/big-competition';

    this.breadcrumbsData = [{
      label: 'Competitions',
      url: bigCompetitionPath
    }, {
      label: this.competition.name,
      url: `${bigCompetitionPath}/${this.competition.id}`
    }, {
      label: participant.obName,
      url: `${bigCompetitionPath}/${this.competition.id}/participant/${participant.id}`
    }];
  }

  public uploadSvgHandler(file): void {
    this.bigCompetitionApiService
      .uploadParticipantSvg(this.participant.id, file)
      .map((response: HttpResponse<CompetitionParticipant>) => {
        return response.body;
      })
      .subscribe((participant: CompetitionParticipant) => {
        this.saveOriginalModel(participant);
        this.actionButtons.extendCollection(participant);
        this.svgFile.filename = participant.svgFilename;
        this.snackBar.open('Svg Uploaded.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  public removeSvgHandler(): void {
    this.bigCompetitionApiService
      .removeParticipantSvg(this.participant.id)
      .map((response: HttpResponse<CompetitionParticipant>) => {
        return response.body;
      })
      .subscribe((participant: CompetitionParticipant) => {
        this.saveOriginalModel(participant);
        this.actionButtons.extendCollection(participant);
        this.svgFile.filename = participant.svgFilename;
        this.snackBar.open('Svg Deleted.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
