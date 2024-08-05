import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';

import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {Competition, CompetitionParticipant, CompetitionTab} from '../../../../client/private/models';
import {DialogService} from '../../../../shared/dialog/dialog.service';
import {ComponentCanDeactivate} from '../../../../client/private/interfaces/pending-changes.guard';

import {BigCompetitionService} from '../../service/big-competition.service';
import {Breadcrumb} from '../../../../client/private/models/breadcrumb.model';
import {SpaceToDashPipe} from '../../../../client/private/pipes/space-to-dash.pipe';
import {BrandService} from '@app/client/private/services/brand.service';

@Component({
  templateUrl: './competition-edit.component.html'
})
export class CompetitionEditComponent implements OnInit, ComponentCanDeactivate {
  public competition: Competition;
  private originalModel: Competition;
  private routeState: string = '';
  public tabsList: CompetitionTab[] = [];
  public participantsList: CompetitionParticipant[] = [];
  public form: FormGroup;
  public competitionNotFound: boolean = false;
  public breadcrumbsData: Breadcrumb[] = [];
  public labelShown: boolean = true;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private spaceToDashPipe: SpaceToDashPipe,
    private dialogService: DialogService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private bigCompetitionService: BigCompetitionService,
    private brandService: BrandService) {
  }

  ngOnInit() {
    this.loadInitData();
  }

  private saveChanges(): void {
    const updateData = {
      id: this.competition.id,
      name: _.trim(this.competition.name),
      uri: _.trim(this.competition.uri),
      enabled: this.competition.enabled,
      typeId: this.competition.typeId,
      brand: this.brandService.brand,
      title: _.trim(this.competition.title),
     background: _.trim(this.competition.background),
     svgBgId: _.trim(this.competition.svgBgId)
    };

    this.bigCompetitionApiService
      .putCompetitionChanges(updateData)
      .map((response: HttpResponse<Competition>) => {
        return response.body;
      })
      .subscribe((competition: Competition) => {
        this.competition = competition;
        this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);
        this.saveOriginalModel(competition);
        this.actionButtons.extendCollection(this.competition);

        this.dialogService.showNotificationDialog({
          title: 'Competition Saving',
          message: 'Competition is Successfully Saved'
        });
      });
  }

  private revertChanges(): void {
    this.loadInitData(true);
  }

  private removeCompetition(): void {
    this.bigCompetitionApiService.deleteCompetition(this.competition.id)
      .subscribe((data: any) => {
        this.originalModel = null;
        this.router.navigate(['/sports-pages/big-competition']);
      });
  }

  public isValidForm(competition: Competition): boolean {
    return !!(_.trim(competition.name).length && _.trim(competition.uri).length && competition.typeId && _.trim(competition.title).length);
  }

  private loadInitData(reload?: boolean): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeState = _.last(Object.keys(params));

      this.bigCompetitionApiService.getSingleCompetition(params.competitionId)
        .subscribe((data: any) => {
          const competition = data.body;

          if (competition) {
            this.tabsList = _.compact(competition.competitionTabs || []);
            this.participantsList = _.compact(competition.competitionParticipants || []);
            this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(competition, this.routeState);
            this.form = new FormGroup({
              name: new FormControl(competition.name, [Validators.required]),
              url: new FormControl({
                value: competition.uri,
                disabled: true
              }, []),
              enabled: new FormControl(competition.enabled),
              typeId: new FormControl(competition.typeId, [Validators.required]),
              title: new FormControl(competition.title, [Validators.required])
            });

            this.saveOriginalModel(competition);
            this.competition = competition;
            this.bigCompetitionService.setTabType('');

            if (reload) {
              this.actionButtons.extendCollection(this.competition);
            }
          } else {
            this.competitionNotFound = true;
          }
        }, () => {
          this.competitionNotFound = true;
        });
    });
  }

  public canDeactivate(): boolean {
    return !this.originalModel || _.isEqual(this.originalModel, this.competition);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeCompetition();
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

  private saveOriginalModel(competition: Competition): void {
    this.originalModel = _.extend({}, competition);
  }

  public onNameChanged(): void {
    this.competition.uri = `/${this.spaceToDashPipe.transform(this.competition.name)}`;
  }
}
