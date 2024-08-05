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

@Component({
  templateUrl: './competition-sub-tab-edit.component.html'
})
export class CompetitionSubTabEditComponent implements OnInit, ComponentCanDeactivate {
  public subTab: CompetitionTab;
  private originalModel: CompetitionTab;
  private competition: Competition;
  private routeState: string = '';
  public form: FormGroup;
  public modulesList: CompetitionModule[];
  public subTabNotFound: boolean = false;
  public breadcrumbsData: Breadcrumb[] = [];
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
    this.bigCompetitionService.setTabType('subtab');
  }

  private loadInitData(reload?: boolean): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeState = _.last(Object.keys(params));

      this.bigCompetitionApiService.getSingleSubTab(params.competitionId, params.tabId, params.subTabId)
        .subscribe((data: any) => {
          this.competition = data.body || {};
          const competitionTab = _.isArray(this.competition.competitionTabs) && this.competition.competitionTabs[0];
          const subTab = _.isArray(competitionTab.competitionSubTabs) && competitionTab.competitionSubTabs[0];

          if (subTab) {
            this.modulesList = _.compact(subTab.competitionModules || []);
            this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);

            this.form = new FormGroup({
              name: new FormControl(subTab.name, [Validators.required]),
              uri: new FormControl({
                value: subTab.uri,
                disabled: true
              }, []),
              enabled: new FormControl(subTab.enabled, [])
            });

            this.saveOriginalModel(subTab);
            this.subTab = subTab;

            if (reload) {
              this.actionButtons.extendCollection(this.subTab);
            }
          } else {
            this.subTabNotFound = true;
          }
        }, () => {
          this.subTabNotFound = true;
        });
    });
  }

  public isValidForm(subTab: CompetitionTab): boolean {
    return !!(_.trim(subTab.name).length && _.trim(subTab.uri).length);
  }

  private saveChanges(): void {
    const updateData = {
      id: this.subTab.id,
      name: _.trim(this.subTab.name),
      uri: _.trim(this.subTab.uri),
      enabled: this.subTab.enabled
    };

    this.bigCompetitionApiService
      .putSubTabChanges(updateData)
      .map((response: HttpResponse<CompetitionTab>) => {
        return response.body;
      })
      .subscribe((subTab: CompetitionTab) => {
        this.subTab = subTab;
        this.bigCompetitionService.updateCompetition(this.competition, this.subTab);
        this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);

        this.saveOriginalModel(this.subTab);
        this.actionButtons.extendCollection(this.subTab);

        this.dialogService.showNotificationDialog({
          title: 'Sub Tab Saving',
          message: 'Competition Sub Tab is Successfully Saved'
        });
      });
  }

  private revertChanges(): void {
    this.loadInitData(true);
  }

  private removeTab(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteSubTab(params.competitionId, params.tabId, this.subTab.id)
        .subscribe((data: any) => {
          this.originalModel = null;
          this.router.navigate([`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}`]);
        });
    });
  }

  public canDeactivate(): boolean {
    return !this.originalModel || _.isEqual(this.originalModel, this.subTab);
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

  private saveOriginalModel(subTab: CompetitionTab): void {
    this.originalModel = _.extend({}, subTab);
  }

  public onNameChanged(): void {
    this.subTab.uri = `/${this.spaceToDashPipe.transform(this.subTab.name)}`;
  }
}
