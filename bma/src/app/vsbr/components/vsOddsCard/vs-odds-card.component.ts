import * as _ from 'underscore';
import { Component, OnInit, Input } from '@angular/core';
import { FiltersService } from '@core/services/filters/filters.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BetslipSelectionsDataService, IEmptySelectionWithPrice } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { ISystemConfig } from '@core/services/cms/models';
import { IOutcome } from '@core/models/outcome.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { IVirtualSportEventEntity } from '@app/vsbr/models/virtual-sports-event-entity.model';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import environment from '@environment/oxygenEnvConfig';
import { CommandService } from '@core/services/communication/command/command.service';
import { IHandicapOutcome } from '@betslip/models/betslip-bet-data.model';

interface IOutcomeContainer {
  outcome: IOutcome;
  outcomeMeaningMinorCode: number;
}

@Component({
  selector: 'vs-odds-card-component',
  templateUrl: 'vs-odds-card.component.html',
  styleUrls: ['./vs-odds-card.component.scss']
})

export class VsOddsCardComponent implements OnInit {
  @Input() currentEvent: IVirtualSportEventEntity;
  @Input() eventOutcomes: IOutcomeContainer[];
  @Input() eventOngoing: boolean;
  @Input() showRunnerImages: boolean;
  @Input() showRunnerNumber: boolean;
  @Input() template: string;
  @Input() gtmModuleTitle?: string;
  @Input() templateMarketName: string;

  eventData: IOutcomeContainer[];
  filterAlphabetsOnlyTrimUnderscore: Function | any;
  filterNumbersOnly: Function | any;
  correctScoreTitle:string = 'Correct Score';
  totalMatchGoalsTitle:string = 'Total Match Goals';

  private maxBetsAmount: number;
  private env = environment;

  constructor(
    private filter: FiltersService,
    private cms: CmsService,
    private user: UserService,
    private pubsub: PubSubService,
    private betSlipSelectionsData: BetslipSelectionsDataService,
    private priceOddsButtonService: PriceOddsButtonAnimationService,
    private gtmTrackingService: GtmTrackingService,
    private commandService: CommandService,
  ) {
    this.filterAlphabetsOnlyTrimUnderscore = this.filter.filterAlphabetsOnlyTrimUnderscore;
    this.filterNumbersOnly = this.filter.filterNumbersOnly;
  }

  ngOnInit(): void {
    this.eventData = this.getEventData();

    this.cms.getSystemConfig(false).subscribe((result: ISystemConfig) => {
        if (result.Betslip) {
          this.maxBetsAmount = Number(result.Betslip.maxBetNumber);
        }
      });
  }

  trackOutcomeById(index: number, item: IOutcomeContainer) {
    return `${index}_${item.outcome.id}`;
  }

  trackGroupedOutcomes(index: number, outcomesGroup: IOutcomeContainer[]) {
    return `${index}_${outcomesGroup.map(item => item.outcome.id).join('_')}`;
  }

  /**
   *
   * Common Handler for button click
   *
   * @param {object} $event
   */
  onPriceOddsButtonClick($event: Event, outcome: IOutcome): void {
    $event.stopPropagation();

    this.commandService.executeAsync(this.commandService.API.IS_ADDTOBETSLIP_IN_PROCESS).then((inProgress: boolean) => {
      if (!inProgress) {
        this.addToBetSlip($event, outcome);
      }
    });
  }

  /**
   * Adding to BetSlip.
   * @param {Object} event - click event
   * @param {Object} outcome
   */
  addToBetSlip(event: Event, outcome: IOutcome): void {
    const tracking = this.gtmTrackingService.detectVirtualSportTracking('virtual edp', this.currentEvent);
    this.priceOddsButtonService.animate(event).then(() => {
      if (this.currentEvent && this.currentEvent.event) {
        const isBuildYourBet = this.currentEvent.event && this.env && this.env.BYB_CONFIG
          && String(this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID) === String(this.currentEvent.event.typeId);

        const GTMObject = {
          categoryID: this.currentEvent.event.categoryId,
          typeID: this.currentEvent.event.typeId,
          eventID: this.currentEvent.event.id,
          selectionID: outcome.id
        };

        if (tracking) {
          GTMObject['tracking'] = tracking;
          GTMObject['betData'] = {
            name: this.currentEvent.event.originalName || this.currentEvent.event.name,
            category: String(this.currentEvent.event.categoryId),
            variant: String(this.currentEvent.event.typeId),
            brand: this.templateMarketName,
            dimension60: String(this.currentEvent.event.id),
            dimension61: outcome.id,
            dimension62: this.currentEvent.event.eventIsLive ? 1 : 0,
            dimension63: isBuildYourBet ? 1 : 0,
            dimension64: tracking.location,
            dimension65: tracking.module,
            dimension180: this.currentEvent.event.categoryId == '39' ? 'virtual' : 'normal'
          };
        }

        outcome.children[0].prices = outcome.children[0].price;

        const addToBetSlipObject = {
          outcomes: [outcome],
          price: outcome.children[0].price,
          handicap: this.getOutcomeHandicap(outcome),
          goToBetslip: false,
          GTMObject,
          isVirtual: true
        };

        this.pubsub.publish(this.pubsub.API.ADD_TO_BETSLIP_BY_SELECTION, addToBetSlipObject);
      }

      this.pubsub.publish(this.pubsub.API.LAST_MADE_BET);
    });
  }

  /**
   * Get grouped event outcomes data
   * @return {Array}
   */
  getGroupedEventsData(): IOutcomeContainer[][] {
    return _.chain(this.filter.groupBy(this.eventOutcomes, 'outcomeMeaningMinorCode'))
            .pairs()
            .sortBy((pair: [any, IOutcomeContainer[]]): number => pair[0])
            .map((pair: [any, IOutcomeContainer[]]): IOutcomeContainer[] => pair[1])
            .value();
  }

  /**
   * Return price in correct format (frac/dec).
   * @param {Object} outcomePrice
   * @return {string}
   */
  outputPrice(outcomePrice: IOutcomePrice): string {
    return this.user.oddsFormat === 'frac'
      ? `${outcomePrice.priceNum}/${outcomePrice.priceDen}`
      : Number(outcomePrice.priceDec).toFixed(2);
  }

  /**
   * Set Active Class to BetSlip Button
   * @param {string} outcomeId
   * @param {string} priceType
   * @returns {boolean}
   */
  isActiveClass(outcomeId: string, priceType: string): boolean {
    if (this.betSlipSelectionsData.count() <= this.maxBetsAmount) {
      const selections = this.betSlipSelectionsData.getSelectionsByOutcomeId(outcomeId);

      return _.some(selections, (sel: IEmptySelectionWithPrice): boolean => {
        return sel.price.priceType === priceType;
      });
    }
    return false;
  }

  /**
   * Get filtered event outcomes data
   * @return {Array}
   */
  private getEventData(): IOutcomeContainer[] {
    switch (this.template) {
      case 'WinEw':
        return _.chain(this.eventOutcomes).sortBy((event: IOutcomeContainer) => {
          return event.outcome.name;
        }).sortBy((event: IOutcomeContainer) => {
          return event.outcome.children[0].price.priceDec;
        }).value();
      case 'Column':
        return _.chain(this.eventOutcomes).sortBy((event: IOutcomeContainer) => {
          return event.outcome.outcomeMeaningMinorCode;
        }).value();
      case 'Horizontal':
        return _.chain(this.eventOutcomes).sortBy((event: IOutcomeContainer) => {
          return event.outcome.displayOrder;
        }).value();
      default:
        const isSortByTeam: boolean = this.templateMarketName && this.templateMarketName.toLocaleLowerCase() === 'correct score (game)';
        const sortedByPrice: IOutcomeContainer[] = _.chain(this.eventOutcomes)
        .sortBy((event: IOutcomeContainer) => event.outcome.children[0].price.priceDec).value();
        const sortedByTeam: IOutcomeContainer[] = _.chain(this.eventOutcomes)
          .sortBy((event: IOutcomeContainer) => event.outcome.children[0].price.priceDec)
          .sortBy((event: IOutcomeContainer) => event.outcome.name.toLowerCase().split('')[0]).value();

        return isSortByTeam ? sortedByTeam : sortedByPrice;
    }
  }

  private getOutcomeHandicap(outcome: IOutcome): IHandicapOutcome {
    const price = outcome.children[0].price;
    return price.rawHandicapValue ? {
      type: outcome.outcomeMeaningMajorCode,
      raw: price.handicapValueDec.replace(/,/g, '')
    } : undefined;
  }
}
