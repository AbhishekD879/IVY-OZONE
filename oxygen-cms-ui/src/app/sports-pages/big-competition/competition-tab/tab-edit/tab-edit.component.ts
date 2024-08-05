import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params, Router} from '@angular/router';
import * as _ from 'lodash';

import {Competition, CompetitionModule, CompetitionTab} from '../../../../client/private/models';
import {DialogService} from '@app/shared/dialog/dialog.service';

import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {ComponentCanDeactivate} from '@app/client/private/interfaces/pending-changes.guard';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {BigCompetitionService} from '../../service/big-competition.service';
import {SpaceToDashPipe} from '@app/client/private/pipes/space-to-dash.pipe';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';

@Component({
  templateUrl: './tab-edit.component.html'
})
export class TabEditComponent implements OnInit, ComponentCanDeactivate {
  public competitionTab: CompetitionTab;
  private originalModel: CompetitionTab;
  private competition: Competition;
  private routeState: string = '';
  public form: FormGroup;
  public subTabsList: CompetitionTab[];
  public modulesList: CompetitionModule[];
  public tabNotFound: boolean = false;
  public breadcrumbsData: Breadcrumb[] = [];
  public highlightCarouselList: SportsHighlightCarousel[];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private spaceToDashPipe: SpaceToDashPipe,
    private dialogService: DialogService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private bigCompetitionApiService: BigCompetitionAPIService,
    private bigCompetitionService: BigCompetitionService) { }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData(reload?: boolean): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeState = _.last(Object.keys(params));

      this.bigCompetitionApiService.getSingleCompetitionTab(params.competitionId, params.tabId)
        .subscribe((data: any) => {
          this.competition = data.body || {};
          const competitionTab = _.isArray(this.competition.competitionTabs) && this.competition.competitionTabs[0];

          if (competitionTab) {
            this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);
            this.subTabsList = _.compact(competitionTab.competitionSubTabs || []);
            this.modulesList = _.compact(competitionTab.competitionModules || []);
            this.form = new FormGroup({
              name: new FormControl(competitionTab.name, [Validators.required]),
              uri: new FormControl({
                value: competitionTab.uri,
                disabled: true
              }, []),
              enabled: new FormControl(competitionTab.enabled, [])
            });

            this.saveOriginalModel(competitionTab);
            this.competitionTab = competitionTab;

            if (reload) {
              this.actionButtons.extendCollection(this.competitionTab);
            }
          } else {
            this.tabNotFound = true;
          }
        }, () => {
          this.tabNotFound = true;
        });
    });
  }

  public isValidForm(competitionTab: CompetitionTab): boolean {
    return !!(_.trim(competitionTab.name).length && _.trim(competitionTab.uri).length);
  }

  private saveChanges(): void {
    const updateData = {
      id: this.competitionTab.id,
      name: _.trim(this.competitionTab.name),
      uri: _.trim(this.competitionTab.uri),
      enabled: this.competitionTab.enabled,
      hasSubtabs: this.competitionTab.hasSubtabs
    };

    this.bigCompetitionApiService
      .putCompetitionTabChanges(updateData)
      .map((response: HttpResponse<CompetitionTab>) => {
        return response.body;
      })
      .subscribe((competitionTab: CompetitionTab) => {
        this.competitionTab = competitionTab;
        this.bigCompetitionService.updateCompetition(this.competition, this.competitionTab);
        this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);
        this.saveOriginalModel(this.competitionTab);
        this.actionButtons.extendCollection(this.competitionTab);

        this.dialogService.showNotificationDialog({
          title: 'Competition Tab Saving',
          message: 'Competition Tab is Successfully Saved'
        });
      });
  }

  private revertChanges(): void {
    this.loadInitData(true);
  }

  private removeTab(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteCompetitionTab(params.competitionId, this.competitionTab.id)
        .subscribe((data: any) => {
          this.originalModel = null;
          this.router.navigate([`/sports-pages/big-competition/${params.competitionId}`]);
        });
    });
  }

  public canDeactivate(): boolean {
    return !this.originalModel || _.isEqual(this.originalModel, this.competitionTab);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeTab();
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

  private saveOriginalModel(competitionTab: CompetitionTab): void {
    this.originalModel = _.extend({}, competitionTab);
  }

  public onNameChanged(): void {
    this.competitionTab.uri = `/${this.spaceToDashPipe.transform(this.competitionTab.name)}`;
  }
}
