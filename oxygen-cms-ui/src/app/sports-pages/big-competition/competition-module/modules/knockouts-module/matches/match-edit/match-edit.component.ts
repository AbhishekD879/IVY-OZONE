import * as _ from 'lodash';
import {DateAndTimeComponent} from '../../../../../../../shared/formElements/dateAndTime/date.time.component';

import {Component, OnInit, ViewChild} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';

import {Breadcrumb} from '../../../../../../../client/private/models/breadcrumb.model';
import {BigCompetitionAPIService} from '../../../../../service/big-competition.api.service';
import {BigCompetitionService} from '../../../../../service/big-competition.service';
import {Competition} from '../../../../../../../client/private/models';
import {CompetitionModule} from '../../../../../../../client/private/models/competitionmodule.model';
import {ComponentCanDeactivate} from '../../../../../../../client/private/interfaces/pending-changes.guard';
import {KnockoutsMatch} from '../../../../../../../client/private/models/knockoutsmatch.model';
import {RoundNameModel} from '../../../../../../../client/private/models/roundName.model';
import {KnockoutEventValid} from '../../../../../../../client/private/models/knockouteventvalid.model';
import {uniqueValidator} from '../../../../../../../shared/validators/unique.validator';

@Component({
  templateUrl: './match-edit.component.html'
})
export class MatchEditComponent implements OnInit, ComponentCanDeactivate {

  @ViewChild('actionButtons') actionButtons;
  @ViewChild('dateTime') dateTimeComponent: DateAndTimeComponent;

  public breadcrumbsData: Array<Breadcrumb> = [];
  public form: FormGroup;
  public match: KnockoutsMatch;
  public moduleNotFound: boolean = false;
  public module: CompetitionModule;
  public rounds: Array<RoundNameModel>;
  public roundNames: Array<string>;
  public abbreviationOptions: Array<string> = [];
  public round: RoundNameModel;
  public chosenRound: RoundNameModel;

  private originalModel: KnockoutsMatch;
  private routeState: string = '';
  private hasErrors: boolean = false;


  private static getCompetitionModule(competition: Competition): CompetitionModule {
    const competitionTab = _.isArray(competition.competitionTabs) && competition.competitionTabs[0],
      subTab = _.isArray(competitionTab.competitionSubTabs) && competitionTab.competitionSubTabs[0],
      subtabModule = subTab && _.isArray(subTab.competitionModules) && subTab.competitionModules[0],
      tabModule = !subtabModule && _.isArray(competitionTab.competitionModules) && competitionTab.competitionModules[0];

    return subtabModule || tabModule;
  }
  private static getModuleMatch (module: CompetitionModule, abbreviation: string): KnockoutsMatch {
    return module.knockoutModuleData.events.find(match => match.abbreviation === abbreviation);
  }

  private static getPreviousPage(params: Params): string {
    return params.subTabId ? `/subtab/${params.subTabId}` : '';
  }


  constructor(
    private bigCompetitionApiService: BigCompetitionAPIService,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionService: BigCompetitionService,
    private router: Router
  ) {}

  ngOnInit() {
    this.form = new FormGroup({
      eventId: new FormControl(null, []),
      eventName: new FormControl('', []),
      homeTeam: new FormControl('', []),
      homeTeamRemark: new FormControl('', []),
      awayTeam: new FormControl('', []),
      awayTeamRemark: new FormControl('', []),
      venue: new FormControl('', []),
      startTime: new FormControl('', []),
      round: new FormControl('', [Validators.required]),
      abbreviation: new FormControl('', [Validators.required]),
    });
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
          const module = MatchEditComponent.getCompetitionModule(competition),
            match = MatchEditComponent.getModuleMatch(module, params.abbreviation),
            previousPage = MatchEditComponent.getPreviousPage(params);


          if (module && match) {
            this.saveOriginalModel(match);

            this.module = module;
            this.match = match;
            this.rounds = this.module.knockoutModuleData.rounds;
            this.roundNames = this.rounds.map(round => round.name);
            this.round = _.find(this.rounds, round => round.name === this.match.round);

            this.breadcrumbsData = this.bigCompetitionService
              .breadcrumbParser(competition, this.routeState)
              .concat([{
                label: this.match.round,
                url: `/sports-pages/big-competition/${params.competitionId}` +
                `/tab/${params.tabId}${previousPage}` +
                `/module/${params.moduleId}` +
                `/matches/${params.abbreviation}`
              }]);

            this.form = new FormGroup({
              eventId: new FormControl(this.match.eventId, []),
              eventName: new FormControl(this.match.eventName, []),
              homeTeam: new FormControl(this.match.homeTeam, []),
              homeTeamRemark: new FormControl(this.match.homeTeamRemark, []),
              awayTeam: new FormControl(this.match.awayTeam, []),
              awayTeamRemark: new FormControl(this.match.awayTeamRemark, []),
              venue: new FormControl(this.match.venue, []),
              startTime: new FormControl(this.match.startTime, []),
              round: new FormControl(this.round.name, [Validators.required]),
              abbreviation: new FormControl(this.match.abbreviation, [
                Validators.required,
                uniqueValidator(module.knockoutModuleData.events, 'abbreviation', this.match)
              ]),
            });

            this.buildAbbreviationSelect(this.round.abbreviation, Number(this.round.number));
            this.dateTimeComponent.setDayTime(Date.parse(this.match.startTime));
          } else {
            this.moduleNotFound = true;
          }
        });
    }, () => {
      this.moduleNotFound = true;
    });
  }

  private saveOriginalModel(match: KnockoutsMatch): void {
    this.originalModel = _.defaultsDeep({}, match);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeMatch();
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

  public removeMatch(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      _.remove(this.module.knockoutModuleData.events, {abbreviation: this.match.abbreviation});

      this.bigCompetitionApiService
        .putModuleChanges(this.module)
        .map((response: HttpResponse<CompetitionModule>) => {
          return response.body;
        })
        .subscribe((module: CompetitionModule) => {
          const previousPage = MatchEditComponent.getPreviousPage(params),
          match = MatchEditComponent.getModuleMatch(module, params.abbreviation);

          this.saveOriginalModel(match);
          this.router.navigate(
            [`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}${previousPage}/module/${params.moduleId}`]);
        });
    });
  }

  public saveChanges(): void {
    const index = this.module.knockoutModuleData.events.findIndex(match => match.abbreviation === this.match.abbreviation);

    this.activatedRoute.params.subscribe((params: Params) => {
      const changedMatch = this.getMatch();
      changedMatch.eventId = Number(changedMatch.eventId);
      if (changedMatch.eventId === 0) {
        changedMatch.eventId = null;
      }
      this.module.knockoutModuleData.events[index] = changedMatch;
      this.bigCompetitionApiService
        .putModuleChanges(this.module)
        .map((response: HttpResponse<CompetitionModule>) => {
          return response.body;
        })
        .subscribe((module: CompetitionModule) => {
          const previousPage = MatchEditComponent.getPreviousPage(params);

          this.saveOriginalModel(changedMatch);
          this.router.navigate(
            [`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}${previousPage}/module/${params.moduleId}`]);
        });
    });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public getMatch(): KnockoutsMatch {
    return this.form.value;
  }

  public canDeactivate(): boolean {
    const areModelsEqual = _.isEqual(
      _.omit(this.originalModel),
      _.omit(this.getMatch())
    );
    return !this.originalModel || areModelsEqual;
  }



  public getConvertedDate(date: string): void {
    const dateNow = new Date();
    this.form.get('startTime').setValue(
      `${new Date(new Date(date).getTime() + (dateNow.getTimezoneOffset() * 60000)).toISOString()}`);
  }

  public onChange(): void {
    this.chosenRound = this.rounds[this.rounds.findIndex(round => round.name === this.form.value.round)];
    this.form.get('abbreviation').setValue('');
    this.buildAbbreviationSelect(this.chosenRound.abbreviation, Number(this.chosenRound.number));
  }

  public buildAbbreviationSelect(abbreviation: string, count: number): void {
    this.abbreviationOptions = [];
    for (let i: number = 1; i <= count; i++) {
      this.abbreviationOptions.push(abbreviation + i);
    }
  }

  public getSSEvent(event, fromButton: boolean, idFromButton: number): void {
    const eventIdForSS = fromButton ? idFromButton : event.srcElement.value;

    if (eventIdForSS.length || eventIdForSS > 0) {
      this.bigCompetitionApiService.getSiteServeEvent(eventIdForSS)
        .map((response: HttpResponse<KnockoutEventValid>) => {
          return response.body;
        })
        .subscribe((data: KnockoutEventValid) => {
          this.hasErrors = false;
          if (fromButton) {
            this.populateMatch(data);
          }
        }, () => {
          this.form.controls['eventId'].setErrors({'invalid': true});
          this.hasErrors = true;
        });
    }
  }

  public checkForErrors(): void {
    if (this.hasErrors) {
      this.form.controls['eventId'].setErrors({'invalid': true});
      this.hasErrors = false;
    }
  }

  public populateMatch(populateObject): void {
    this.form.get('awayTeam').setValue(populateObject.awayTeam);
    this.form.get('homeTeam').setValue(populateObject.homeTeam);
    this.form.get('eventName').setValue(populateObject.eventName);
    this.form.get('startTime').setValue(populateObject.startTime);
    this.dateTimeComponent.setDayTime(populateObject.startTime);
  }

  public get formRound(): AbstractControl {
    return this.form.get('round');
  }

  public get abbreviation(): AbstractControl {
    return this.form.get('abbreviation');
  }

  public get eventId(): AbstractControl {
    return this.form.get('eventId');
  }
}
