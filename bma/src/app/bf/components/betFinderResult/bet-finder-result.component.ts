import { UserService } from '@core/services/user/user.service';
import { from, Observable, of } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { ChangeDetectorRef, Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { CommandService } from '@core/services/communication/command/command.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { ISystemConfig } from '@core/services/cms/models';
import { IRunner } from '@app/bf/models/races-list.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IBreadcrumb } from '@app/shared/models/breadcrumbs.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'bet-finder-result',
  templateUrl: 'bet-finder-result.component.html'
})
export class BetFinderResultComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  maxBetsAmount: number;
  window: any;
  foundResult: string;
  runners: IRunner[];
  sortingOrder: string;
  timer1: any = null;
  timer2: any = null;
  breadcrumbsItems: IBreadcrumb[];
  runnersData: IRunner[];
  readonly IMAGES_ENDPOINT: string = environment.IMAGES_ENDPOINT;
  private document: HTMLElement;
  private timeOutListener;
  private intervalValue: number = 500;

  constructor(
    private storageService: StorageService,
    private deviceService: DeviceService,
    private cmsService: CmsService,
    private betSlipSelectionsDataService: BetslipSelectionsDataService,
    private commandService: CommandService,
    private windowRefService: WindowRefService,
    private localeService: LocaleService,
    private filtersService: FiltersService,
    private domToolsService: DomToolsService,
    private pubSubService: PubSubService,
    private gtm: GtmService,
    private betFinderHelperService: BetFinderHelperService,
    private changeDetRef: ChangeDetectorRef,
    private userService: UserService,
    private raceOutcomeDetailsService: RaceOutcomeDetailsService
  ) {
    super()/* istanbul ignore next */;
    this.window = this.windowRefService.nativeWindow;
    this.document = this.windowRefService.document.documentElement || this.windowRefService.document.body;
  }

  ngOnInit(): void {
    this.addChangeDetection();
    this.sortingOrder = this.storageService.get('bfResultsSorting') || 'time';
    this.pubSubService.subscribe('bet_finder', this.pubSubService.API.RELOAD_COMPONENTS, () => this.init());

    this.initializeBreadcrumbs();
    this.init();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('bet_finder');
    this.timeOutListener && this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
  }

  @HostListener('window:scroll', [])
  onWindowScroll(): void {
    this.finishAnimation();
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * addToBetSlip.
   *
   * Handle click on the price odds button.
   * @param {object} event
   * @param {string} outcomeId
   */
  addToBetSlip(event: Event, outcomeId: string): void {
    const isInIFrame = this.window.frameElement && this.window.frameElement.nodeName === 'IFRAME';

    this.animation(event, outcomeId)
      .subscribe((addToBetSlipObject: IQuickbetSelectionModel) => {
        if (addToBetSlipObject) {
          if (!isInIFrame) {
            this.pubSubService.publish(this.pubSubService.API.ADD_TO_BETSLIP_BY_SELECTION, addToBetSlipObject);
          } else {
            // send betObject to betSlip in parent window if this directive runs from iFrame,
            // preparation for inPlay App in iFrame
            parent.postMessage(`iFrame:bet:${JSON.stringify(addToBetSlipObject)}`, '*');
          }
        }
      });
  }

  /**
   * Return active button class if selection is added to betslip.
   * @return {string}
   */
  applyButtonClasses(outcomeId: string): string {
    const selections = this.betSlipSelectionsDataService.getSelectionsByOutcomeId(outcomeId);

    return !_.isEmpty(selections) ? 'active' : '';
  }

  /**
   * Sort Results.
   * Calls the method in the directive for sorting the results.
   *
   * @param {string} order
   */
  sortResults(order: string): void {
    const sortOrder = order === 'time' ? 'time' : 'odds';

    if (this.sortingOrder !== order) {
      this.sortingOrder = order;
      this.triggerSortResults(order);
      this.storageService.set('bfResultsSorting', order);

      this.gtm.push('trackEvent', {
        eventCategory: 'bet finder',
        eventAction: 'sorting',
        eventLabel: `sort - by ${sortOrder}`
      });
    }
  }

  private addChangeDetection() {
    this.changeDetRef.detach();
    this.timeOutListener = this.windowRefService.nativeWindow.setInterval(() => {
      this.changeDetRef.detectChanges();
    }, this.intervalValue);
  }

  /**
   * Add css styles to display silks using aggregated image sprite
   */
  private updateSilksStyle(): void {
    const racingIds = this.runners.filter(item => item.silkID).map(item => {
      return { racingFormOutcome: { silkName: item.silkID }};
    });

    this.runners.filter(item => item.silkID).forEach((runner: IRunner) => {
      runner.silkStyle = this.raceOutcomeDetailsService.getSilkStyle(racingIds,
        { racingFormOutcome: { silkName: runner.silkID }} as IOutcome, '0');
    });
  }

  private init(): void {
    this.showSpinner();
    this.betFinderHelperService.getRunners()
      .subscribe((res: IRunner[]) => {
        _.each(res, (runner: IRunner) => {
          runner.horseName = this.filtersService.removeLineSymbol(runner.horseName);
        });
        this.runnersData = res;
        this.runners = _.sortBy(this.runnersData, 'time');
        this.triggerSortResults(this.sortingOrder);
        this.setResultsNumber(this.runners.length);
        this.userService.oddsFormat === 'dec' ?
          this.runners.map(r => r.oddsToDisplay = r.decimalOdds ? r.decimalOdds.toFixed(2) : 'SP')
          : this.runners.map(r => r.oddsToDisplay = r.odds || 'SP');
        this.updateSilksStyle();
        this.hideSpinner();
        this.hideError();
        }, () => {
        this.showError();
      });

    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        if (config.Betslip) {
          this.maxBetsAmount = Number(config.Betslip.maxBetNumber);
        }
      });
  }

  /**
   * Sort Results.
   *
   * @param {string} order
   */
  private triggerSortResults(order: string): void {
    this.runners = _.sortBy(this.runnersData, order);
  }

  /**
   * Set Selection Number.
   * Create a string that will be displayed on the "Find bets" button indicating a number of selections.
   * @param {number} length - number of filtered selections.
   * @private
   */
  private setResultsNumber(length: number): void {
    const selectStr = length === 0 ? this.localeService.getString('bf.noresult') : this.localeService.getString('bf.results');
    const plural = length === 1 ? '' : 's';
    this.foundResult = `${length || ''} ${selectStr}${plural}`;
  }

  /**
   * Display animation for adding selection to betSlip.
   * @param {object} eventArg - click event
   * @param {string} outcomeId
   * @return {object} - promise
   */
  private animation(eventArg: Event, outcomeId: string): Observable<any> {
    const animatedElement = this.document.querySelector('.bet-animation');
    const currentTarget = <HTMLElement>eventArg.currentTarget;
    const dropzone = this.domToolsService.getOffset(this.document.querySelector('.user-bets'));

    if (this.deviceService.isMobile && animatedElement &&
      !this.domToolsService.hasClass(currentTarget, 'active') &&
      this.betSlipSelectionsDataService.count() < this.maxBetsAmount &&
      !this.storageService.get('overaskIsInProcess') && // can not add to betslip if overask in progress
      dropzone) {
      const scrollY = this.window.pageYOffset;
      const currentTargetOffset = this.domToolsService.getOffset(currentTarget);
      const space = 10;
      const startPositionValue = `translate(${currentTargetOffset.left}px, ${currentTargetOffset.top - scrollY}px)`;
      const endPositionValue = `translate(${(dropzone.left - space)}px, ${(dropzone.top - window.scrollY - space)}px) scale(.2, .2)`;

      this.domToolsService.addClass(currentTarget, 'active');
      this.domToolsService.css(animatedElement, 'transform', startPositionValue);
      this.domToolsService.addClass(animatedElement, 'bet-visible');

      this.timer1 = setTimeout(() => {
        this.domToolsService.css(animatedElement, 'transform', endPositionValue);

        this.timer2 = setTimeout(() => {
          this.finishAnimation();
        }, 480);
      }, 20);
    } else if (this.domToolsService.hasClass(currentTarget, 'active')) {
      this.domToolsService.removeClass(currentTarget, 'active');
    }

    return from(this.commandService.executeAsync(this.commandService.API.GET_EVENTS_BY_OUTCOME_IDS,
        [outcomeId], [])).pipe(
      mergeMap(res => {
        if (!res) {
          return of(null);
        }
        return of(this.addGTMObject(res[0], outcomeId));
      }));
  }

  /**
   * Finish add to betslip animation.
   */
  private finishAnimation(): void {
    const animatedElement = this.document.querySelector('.bet-animation');
    this.domToolsService.removeClass(animatedElement, 'bet-visible');
    clearTimeout(this.timer1);
    clearTimeout(this.timer2);
  }

  /**
   * Add GTM object to the BS object.
   * @param {object} addToBetSlipObject
   * @param {string} outcomeId
   * @return {object}
   */
  private addGTMObject(addToBetSlipObject: IQuickbetSelectionModel, selectionID: string): IQuickbetSelectionModel {
    return _.extend(addToBetSlipObject, { GTMObject: { selectionID } });
  }

  private initializeBreadcrumbs(): void {
    const targetUri = '/horse-racing';
    this.breadcrumbsItems = [{
      name: this.localeService.getString(`sb.horseracing`),
      targetUri
    }, {
      name: this.localeService.getString(`bf.betFinderResults`),
    }];
  }
}
