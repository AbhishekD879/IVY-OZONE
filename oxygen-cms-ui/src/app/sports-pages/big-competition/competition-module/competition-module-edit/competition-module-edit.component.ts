import {Component, ComponentFactoryResolver, ComponentRef, OnInit, ViewChild, ViewContainerRef} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import * as _ from 'lodash';

import {Competition, CompetitionModule} from '../../../../client/private/models';
import {BigCompetitionAPIService} from '../../service/big-competition.api.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {BigCompetitionService} from '../../service/big-competition.service';

import {AemModuleComponent} from '../modules/aem-module/aem-module.component';
import {GroupAllComponent} from '../modules/group-all/group-all.component';
import {GroupIndividualComponent} from '../modules/group-individual/group-individual.component';
import {GroupWidgetComponent} from '../modules/group-widget/group-widget.component';
import {NexteventsModuleComponent} from '../modules/nextevents-module/nextevents-module.component';
import {OutrightModuleComponent} from '../modules/outright-module/market-list/market-list.component';
import {PromotionsModuleComponent} from '../modules/promotions-module/promotions-module.component';
import {SpecialsModuleComponent} from '../modules/specials-module/specials-module.component';
import {SpecialsoverviewModuleComponent} from '../modules/specialsoverview-module/specialsoverview-module.component';
import {ComponentCanDeactivate} from '@app/client/private/interfaces/pending-changes.guard';
import {KnockoutsModuleComponent} from '../modules/knockouts-module/knockouts-module.component';
import {NexteventsIndividualComponent} from '../modules/nextevents-individual/nextevents-individual.component';
import {ResultsModuleComponent} from '../modules/results-module/results-module.component';
import { SportsSurfaceBetsListComponent } from '@app/sports-modules/surface-bets/surface-bets-list/surface-bets-list.component';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { SurfaceBet } from '@app/client/private/models/surfaceBet.model';

@Component({
  selector: 'app-competition-module-edit',
  templateUrl: './competition-module-edit.component.html',
  styleUrls: ['./competition-module-edit.component.scss']
})
export class CompetitionModuleEditComponent implements OnInit, ComponentCanDeactivate {
  private routeState: string = '';
  public moduleNotFound: boolean = false;
  public competition: Competition;
  public module: CompetitionModule;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[] = [];
  private originalModel: CompetitionModule;
  private componentRef: ComponentRef<any>;
  public surfaceBetsData: any;
  public highlighCarouselData: any;
  private selectedBetsResponse: any;
  public surfaceBets: SurfaceBet[];
  public activeBets: SurfaceBet[];
  public show: boolean = true;
  private modulesComponentsMap: object = {
    AEM: AemModuleComponent,
    NEXT_EVENTS: NexteventsModuleComponent,
    PROMOTIONS: PromotionsModuleComponent,
    OUTRIGHTS: OutrightModuleComponent,
    SPECIALS: SpecialsModuleComponent,
    SPECIALS_OVERVIEW: SpecialsoverviewModuleComponent,
    GROUP_INDIVIDUAL: GroupIndividualComponent,
    GROUP_ALL: GroupAllComponent,
    GROUP_WIDGET: GroupWidgetComponent,
    KNOCKOUTS: KnockoutsModuleComponent,
    NEXT_EVENTS_INDIVIDUAL: NexteventsIndividualComponent,
    RESULTS: ResultsModuleComponent,
    SURFACEBET: SportsSurfaceBetsListComponent
  };
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('moduleComponent', {
    read: ViewContainerRef
}) viewContainerRef: ViewContainerRef;

  constructor(private componentFactoryResolver: ComponentFactoryResolver,
              private bigCompetitionApiService: BigCompetitionAPIService,
              private activatedRoute: ActivatedRoute,
              private bigCompetitionService: BigCompetitionService,
              private dialogService: DialogService,
              private router: Router,
              private apiClientService: ApiClientService,
              private brandService: BrandService,
              private globalLoaderService: GlobalLoaderService) {
    this.isValidForm = this.isValidForm.bind(this);
  }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData(reload?: boolean): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      // Detect module path(if > 3 then module comes from sub tab page, else - from tab page)
      if (Object.keys(params).length > 3) {
        this.routeState = 'subTabAndModuleId';
      } else {
        this.routeState = _.last(Object.keys(params));
      }

      this.bigCompetitionApiService.getSingleModule(params.competitionId, params.tabId, params.subTabId, params.moduleId)
        .subscribe((data: any) => {
          this.competition = data.body || {};
          const competitionTab = _.isArray(this.competition.competitionTabs) && this.competition.competitionTabs[0];
          const subTab = _.isArray(competitionTab.competitionSubTabs) && competitionTab.competitionSubTabs[0];
          const subtabModule = subTab && _.isArray(subTab.competitionModules) && subTab.competitionModules[0];
          const tabModule = !subtabModule && _.isArray(competitionTab.competitionModules) && competitionTab.competitionModules[0];
          const module = subtabModule || tabModule;
          if(module.type === 'SURFACEBET') {
            this.selectedBetsResponse = this.competition.competitionTabs[0].competitionModules[0].surfaceBets;
            this.show = false;
          } else if(module.type === 'HIGHLIGHT_CAROUSEL') {
            this.selectedBetsResponse = this.competition.competitionTabs[0].competitionModules[0].highlightCarousels;
            this.show = false;
          }

          if (module) {
            this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);

            this.form = new FormGroup({
              name: new FormControl(module.name, [Validators.required]),
              categoryIDs: new FormControl(module.categoryIDs, []),
              type: new FormControl({
                value: module.type,
                disabled: true
              }, []),
              enabled: new FormControl(module.enabled, [])
            });

            this.saveOriginalModel(module);
            this.module = module;
            this.getSurfaceBetsBySport(this.competition.sportId);
            this.getHighlightscaraouselData(this.competition.sportId);
            this.module.categoryIDs = this.selectedBetsResponse;
            this.renderModuleComponentByType(this.module.type);
            if (reload) {
              this.actionButtons.extendCollection(this.module);
            }
          } else {
            this.moduleNotFound = true;
          }
        }, () => {
          this.moduleNotFound = true;
        });
    });
  }

  public isValidForm(module: CompetitionModule): boolean {
    // All nested dynamic components should HAVE 'isValidForm' method if theirs fields should be verified
    const isComponentShouldBeVerified: boolean = this.componentRef && _.isFunction(this.componentRef.instance.isValidForm),
      isModuleName: boolean = !!(_.trim(module.name).length);

    if (isComponentShouldBeVerified) {
     return isModuleName && this.componentRef.instance.isValidForm();
    }

    return isModuleName;
  }

  private saveChanges(): void {
    const isGroupAll = this.module.type === 'GROUP_ALL';
    const updateData = {
      id: this.module.id,
      name: _.trim(this.module.name),
      enabled: this.module.enabled,
      type: this.module.type,
      markets: isGroupAll ? this.module.markets : this.originalModel.markets,
      typeId: this.module.typeId,
      viewType: this.module.viewType,
      aemPageName: this.module.aemPageName,
      maxDisplay: this.module.maxDisplay,
      groupModuleData: this.module.groupModuleData,
      specialModuleData: this.module.specialModuleData,
      eventIds: this.module.eventIds,
      knockoutModuleData: {
        rounds: this.module.knockoutModuleData.rounds,
        events: this.module.knockoutModuleData.events
      },
      resultModuleSeasonId: this.module.resultModuleSeasonId,
      surfaceBets: [],
      highlightCarousels: []
    };

    if(this.module.type === 'SURFACEBET') {
       updateData.surfaceBets = this.module.categoryIDs? this.module.categoryIDs: [];
    } else if(this.module.type === 'HIGHLIGHT_CAROUSEL') {
      updateData.highlightCarousels = this.module.categoryIDs? this.module.categoryIDs: [];
    }

    this.bigCompetitionApiService
      .putModuleChanges(updateData)
      .map((response: HttpResponse<CompetitionModule>) => {
        return response.body;
      })
      .subscribe((module: CompetitionModule) => {
        this.module = module;
        // Update embedded component's input
        //(<any>this.componentRef.instance).module = this.module;
        this.bigCompetitionService.updateCompetition(this.competition, this.module);
        this.breadcrumbsData = this.bigCompetitionService.breadcrumbParser(this.competition, this.routeState);

        this.saveOriginalModel(this.module);

        this.dialogService.showNotificationDialog({
          title: 'Module Saving',
          message: 'Competition Module is Successfully Saved'
        });
        if(module.type === 'SURFACEBET') {
          this.module.categoryIDs = module.surfaceBets;
        } else if(module.type === 'HIGHLIGHT_CAROUSEL') {
          this.module.categoryIDs = module.highlightCarousels;
        }
        this.actionButtons.extendCollection(this.module);
      });
  }

  private revertChanges(): void {
    this.loadInitData(true);
  }

  private removeModule(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bigCompetitionApiService.deleteModule(params.competitionId, params.tabId, params.subTabId, this.module.id)
        .subscribe((data: any) => {
          this.originalModel = null;
          const previousPage = params.subTabId ? `/subtab/${params.subTabId}` : '';
          this.router.navigate([`/sports-pages/big-competition/${params.competitionId}/tab/${params.tabId}${previousPage}`]);
        });
    });
  }

  public canDeactivate(): boolean {
    let areGroupAllModelsEqual,
      areModelsEqual;

    // handle if models are equal considering module type
    if (this.module.type === 'GROUP_ALL') {
      areGroupAllModelsEqual = _.isEqual(this.originalModel, this.module);
    } else {
      areModelsEqual = _.isEqual(
        _.omit(this.originalModel, ['markets', 'knockoutModuleData']),
        _.omit(this.module, ['markets', 'knockoutModuleData', 'categoryIDs'])
      );
    }

    return !this.originalModel || areModelsEqual || areGroupAllModelsEqual;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeModule();
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

  private saveOriginalModel(module: CompetitionModule): void {
    this.originalModel = _.defaultsDeep({}, module);
  }

  private renderModuleComponentByType(type: string): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.modulesComponentsMap[type]),
      isOutrights = type === 'OUTRIGHTS',
      isKnockouts = type === 'KNOCKOUTS';

    this.viewContainerRef.remove();
    this.componentRef = this.viewContainerRef.createComponent(componentFactory);
    // Pass parameter into component
    if (isKnockouts) {
      (<any>this.componentRef.instance).module = _.extend({}, this.module);
      (<any>this.componentRef.instance).changed.subscribe(this.onModuleChangedHandler.bind(this));
    } else if (isOutrights) {
      (<any>this.componentRef.instance).module = _.extend({}, this.originalModel);
    } else {
      (<any>this.componentRef.instance).module = this.module;
    }
  }

  public onModuleChangedHandler(data) {
    if (data.type === 'KNOCKOUTS') {
      this.module.knockoutModuleData.rounds = data.knockoutModuleData.rounds;
      this.module.knockoutModuleData.events = data.knockoutModuleData.events;
    }
  }

  public trackSportById(bets: any): string {
   return bets.id;
  }

  /**
   * 
   * @param typeId {number}
   * fetch surface bets for API
   */ 
   private getSurfaceBetsBySport(typeId: number): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().findAllByBrandAndSport(this.brandService.brand, 'sport', typeId, 'Universal')
      .map((response: HttpResponse<SurfaceBet[]>) => {
        // filter only active for current sport id
        const bets = _.filter(response.body, bet => {
          return _.some(bet.references, { refId: typeId.toString(), relatedTo: 'sport', enabled: true });
        });
        return bets
      })
      .subscribe((bets: SurfaceBet[]) => {
        this.getRequestCallback(bets);
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  /**
   * 
   * @param bets {SurfaceBet}
   */
  private getRequestCallback(bets: SurfaceBet[]): void {
   this.filterBetsByDate(bets);
    this.globalLoaderService.hideLoader();
  }

  /**
   * 
   * @param allBets {SurfaceBet}
   * @returns {SurfaceBet} active bets
   * sets active bets to service
   * 
   */
  private filterBetsByDate(allBets: SurfaceBet[]): void {
    const currentDate = (new Date()).getTime();
    this.activeBets = _.filter(allBets, bet => {
      return (new Date(bet.displayTo)).getTime() >= currentDate;
    });
    this.surfaceBetsData = this.activeBets;
    // this.bigCompetitionService.setSurfaceBetsData(this.activeBets);
  }

  /**
   * 
   * @param typeId {number}
   * Fetch hihlight carousel data from API and set in service
   */
  private getHighlightscaraouselData(typeId: number): void {
    this.apiClientService.sportsHighlightCarousel().findAllByBrandAndSport(this.brandService.brand, typeId, 'sport')
    .map((response: HttpResponse<SportsHighlightCarousel[]>) => response.body)
    .subscribe((carousels: SportsHighlightCarousel[]) => {
      this.highlighCarouselData = carousels;
    });
  }
}
