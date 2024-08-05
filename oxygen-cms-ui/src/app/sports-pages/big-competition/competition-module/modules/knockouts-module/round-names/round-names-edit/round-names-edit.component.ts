import * as _ from 'lodash';

import {Component, OnInit, ViewChild} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {BigCompetitionAPIService} from '../../../../../service/big-competition.api.service';
import {BigCompetitionService} from '../../../../../service/big-competition.service';
import {Competition} from '../../../../../../../client/private/models';
import {RoundNameModel} from '@app/client/private/models/roundName.model';
import {CompetitionModule} from '@app/client/private/models/competitionmodule.model';
import {ComponentCanDeactivate} from '@app/client/private/interfaces/pending-changes.guard';
import {uniqueValidator} from '@app/shared/validators/unique.validator';
import {AppConstants} from '@app/app.constants';

@Component({
  templateUrl: './round-names-edit.component.html'
})
export class RoundNamesEditComponent implements OnInit, ComponentCanDeactivate {

  @ViewChild('actionButtons') actionButtons;

  public breadcrumbsData: Array<Breadcrumb> = [];
  public form: FormGroup;
  public roundName: RoundNameModel;
  public moduleNotFound: boolean = false;
  public module: CompetitionModule;

  private originalModel: RoundNameModel;
  private routeState: string = '';

  private static getCompetitionModule(competition: Competition): CompetitionModule {
    const competitionTab = _.isArray(competition.competitionTabs) && competition.competitionTabs[0],
      subTab = _.isArray(competitionTab.competitionSubTabs) && competitionTab.competitionSubTabs[0],
      subTabModule = subTab && _.isArray(subTab.competitionModules) && subTab.competitionModules[0],
      tabModule = !subTabModule && _.isArray(competitionTab.competitionModules) && competitionTab.competitionModules[0];

    return subTabModule || tabModule;
  }

  private static getModuleRoundName(module: CompetitionModule, abbreviation: string): RoundNameModel {
    return module.knockoutModuleData.rounds.find(roundName => roundName.abbreviation === abbreviation);
  }

  private static getPreviousPage(params: Params): string {
    return params.subTabId ? `/subtab/${params.subTabId}` : '';
  }

  constructor(
    private bigCompetitionApiService: BigCompetitionAPIService,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionService: BigCompetitionService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
  }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      (Object.keys(params).length > 3) ? this.routeState = 'subTabAndModuleId'
        : this.routeState = _.last(Object.keys(params));

      this.bigCompetitionApiService
        .getSingleModule(params.competitionId, params.tabId, params.subTabId, params.moduleId)
        .map((response: HttpResponse<Competition>) => {
          return response.body;
        })
        .subscribe((competition: Competition) => {
          const module = RoundNamesEditComponent.getCompetitionModule(competition),
            roundName = RoundNamesEditComponent.getModuleRoundName(module, params.abbreviation),
            previousPage = RoundNamesEditComponent.getPreviousPage(params),
            roundNames = module.knockoutModuleData.rounds && _.isArray(module.knockoutModuleData.rounds) ?
              module.knockoutModuleData.rounds : [];

          if (module && roundName) {
            this.saveOriginalModel(roundName);

            this.module = module;
            this.roundName = roundName;

            this.breadcrumbsData = this.bigCompetitionService
              .breadcrumbParser(competition, this.routeState)
              .concat([{
                label: this.roundName.name,
                url: `/sports-pages/big-competition/${params.competitionId}` +
                `/tab/${params.tabId}${previousPage}` +
                `/module/${params.moduleId}` +
                `/round-name/${params.abbreviation}`
              }]);

            this.form = new FormGroup({
              name: new FormControl(this.roundName.name, [Validators.required]),
              abbreviation: new FormControl(this.roundName.abbreviation, [
                Validators.required,
                uniqueValidator(roundNames, 'abbreviation', roundName).bind(this)]),
              number: new FormControl(this.roundName.number, [
                Validators.required,
                Validators.min(1),
                Validators.pattern('^\\d+$')
              ]),
              active: new FormControl(this.roundName.active, []),
            });
          } else {
            this.moduleNotFound = true;
          }
        });
    }, () => {
      this.moduleNotFound = true;
    });
  }

  private saveOriginalModel(roundName: RoundNameModel): void {
    this.originalModel = _.defaultsDeep({}, roundName);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeRoundName();
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

  public removeRoundName(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      _.remove(this.module.knockoutModuleData.rounds, {abbreviation: this.roundName.abbreviation});
      _.remove(this.module.knockoutModuleData.events, {round: this.roundName.name});

      this.bigCompetitionApiService
        .putModuleChanges(this.module)
        .map((response: HttpResponse<CompetitionModule>) => {
          return response.body;
        })
        .subscribe(() => {
          const previousPage = RoundNamesEditComponent.getPreviousPage(params);

          this.snackBar.open('Round Removed', 'OK!', {
            duration: AppConstants.HIDE_DURATION
          });
          this.originalModel = null;
          this.router.navigate(
            [`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}${previousPage}/module/${params.moduleId}`]);
        });
    });
  }

  public saveChanges(): void {
    const index = this.module.knockoutModuleData
      .rounds.findIndex(round => round.abbreviation === this.roundName.abbreviation);

    this.activatedRoute.params.subscribe((params: Params) => {
      let roundName = this.getRoundName();

      if (roundName.active) {
        this.module.knockoutModuleData.rounds.forEach(round => round.active = false);
      }

      this.module.knockoutModuleData.rounds[index] = roundName;
      this.bigCompetitionApiService
        .putModuleChanges(this.module)
        .map((response: HttpResponse<CompetitionModule>) => {
          return response.body;
        })
        .subscribe((module: CompetitionModule) => {
          const previousPage = RoundNamesEditComponent.getPreviousPage(params);
          roundName = RoundNamesEditComponent.getModuleRoundName(module, params.abbreviation);

          this.snackBar.open('Round Saved', 'OK!', {
            duration: AppConstants.HIDE_DURATION
          });
          this.roundName = this.getRoundName();
          this.saveOriginalModel(roundName);
          this.router.navigate(
            [`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}${previousPage}/module/${params.moduleId}`]);
        });
    });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public getRoundName(): RoundNameModel {
    return this.form.value;
  }

  public canDeactivate(): boolean {
    const areModelsEqual = _.isEqual(
      _.omit(this.roundName),
      _.omit(this.getRoundName())
    );
    return !this.originalModel || areModelsEqual;
  }

  public get name(): AbstractControl {
    return this.form.get('name');
  }

  public get abbreviation(): AbstractControl {
    return this.form.get('abbreviation');
  }

  public get number(): AbstractControl {
    return this.form.get('number');
  }
}
