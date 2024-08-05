import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { ISportEvent } from '../../models/sport-event.model';
import { IMarket } from '../../models/market.model';
import { IOutcome, IRacingFormOutcome } from '../../models/outcome.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISilkStyleModel } from './silk-style.model';
import { ISystemConfig } from '../cms/models/system-config';
import { SILK } from '@coreModule/constants/silk.constant';
import { UNNAMED_FAVOURITES } from '@core/services/raceOutcomeDetails/race-outcome.constant';

@Injectable()
export class RaceOutcomeDetailsService {

  private readonly IMAGES_RACE_ENDPOINT: string = environment.IMAGES_RACE_ENDPOINT;
  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private readonly IMAGES_ENDPOINT: string = environment.IMAGES_ENDPOINT;
  private readonly TYPE_GREYHOUNDS: string = 'GREYHOUNDS';
  private readonly SILK_IMAGE_HEIGHT: number = SILK.imageHeight;
  private readonly SILK_IMAGE_SMALL_HEIGHT: number = SILK.imageHeightSmall;
  private readonly SILK_POSITION: string = SILK.position;
  private readonly SILK_POSITION_SMALL: string = SILK.positionSmall;
  private readonly SILK_SB_WIDTH: string = SILK.streamBetWidth;
  private isAggregationMSEnabled: boolean = true;
  private isSilkSmall: boolean;

  constructor(
    private cmsService: CmsService
  ) {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isAggregationMSEnabled = !!(config.aggregationMS && config.aggregationMS.enabled);
    });

    this.isNumberNeeded = this.isNumberNeeded.bind(this);
    this.isGenericSilk = this.isGenericSilk.bind(this);
    this.isGreyhoundSilk = this.isGreyhoundSilk.bind(this);
    this.getSilkStyle = this.getSilkStyle.bind(this);
  }

  getSilkStyle(raceData: any, outcome: IOutcome, imgPosition?: string, isSmall: boolean = false, isStreamBet: boolean = false): ISilkStyleModel {
    let outcomes;
    this.isSilkSmall = isSmall;

    if (!_.isArray(raceData)) {
      outcomes = raceData.outcomes ? raceData.outcomes : _.flatten(_.pluck(_.flatten(_.pluck(raceData, 'markets')), 'outcomes'));
    } else {
      outcomes = raceData;
    }

    const racingIds = _.uniq(_.map(_.filter(_.pluck(_.pluck(outcomes, 'racingFormOutcome'), 'silkName'), img => img),
      img => img.replace(/.(gif|png)/g, ''))).sort((a, b) => a > b ? 1 : -1);

    return this.getSilkStyles(racingIds, outcome, imgPosition, isStreamBet);
  }

  isGenericSilk(event: ISportEvent, outcome: IOutcome): boolean {
    if (event.categoryCode === this.TYPE_GREYHOUNDS) {
      return this.isSilkAvailable(event) && !this.isValidNumber(outcome.runnerNumber);
    }
    return this.isSilkAvailable(event) && (!this.isValidSilkName(outcome.racingFormOutcome))
      && (!outcome.racingFormOutcome || !outcome.racingFormOutcome.silkName);
  }

  isGreyhoundSilk(event: ISportEvent, outcome: IOutcome): boolean {
    return event.categoryCode === this.TYPE_GREYHOUNDS && this.isValidNumber(outcome.runnerNumber);
  }

  isGroupSilkNeeded(outcome: IOutcome): boolean {
    return outcome.name === 'Odd' || outcome.name === 'Even' || outcome.name === 'Inside' || outcome.name === 'Outside';
  }

  getOutcomeClass(outcome: IOutcome): string {
    return outcome.name.toLowerCase();
  }

  isSilkAvailable(event: ISportEvent): boolean {
    let available = false;
    _.each(event.markets, (market: IMarket) =>
      _.each(market.outcomes, (outcome: IOutcome) => {
        if (this.isGreyhoundSilk(event, outcome)) {
          available = true;
        } else {
          if (outcome.racingFormOutcome ? !!outcome.racingFormOutcome.silkName : !!outcome.racingFormOutcome) {
            available = true;
          }
        }
      }));

    return available;
  }

  isNumberNeeded(event: ISportEvent, outcome: IOutcome): boolean {
    const isDraw = outcome.racingFormOutcome && outcome.racingFormOutcome.draw && this.isValidNumber(outcome.racingFormOutcome.draw);
    const allowedEvent = event.categoryCode !== this.TYPE_GREYHOUNDS;
    return (this.isValidNumber(outcome.runnerNumber) || this.isValidNumber(outcome.silkName) || isDraw) && allowedEvent;
  }

  getsilkNamesForEvents(events: ISportEvent[]) {
    return _.chain(events)
      .filter(event => event.categoryId === this.HORSE_RACING_CATEGORY_ID)
      .pluck('markets')
      .flatten()
      .pluck('outcomes')
      .flatten()
      .pluck('racingFormOutcome')
      .compact()
      .pluck('silkName')
      .compact()
      .value();
  }

  getSilkStyleForPage(outcomeId: string, event: ISportEvent, allSilkNames: string[], isSmall: boolean = false): ISilkStyleModel {
    this.isSilkSmall = isSmall;
    const outcome = this.getOutcomeData(outcomeId, event).outcome,
      racingIds = _.map(allSilkNames, img => img.replace(/.(gif|png)/g, '')).sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
    return this.getSilkStyles(racingIds, outcome);
  }

  isSilkAvailableForOutcome(outcomeId: string, event: ISportEvent): boolean {
    const outcomeData = this.getOutcomeData(outcomeId, event),
      outcome = outcomeData && outcomeData.outcome,
      racingFormPresent = outcome && outcome.racingFormOutcome;
    let available = false;
    if (racingFormPresent ? !!outcome.racingFormOutcome.silkName : !!racingFormPresent) {
      available = this.isValidSilkName(outcome.racingFormOutcome);
    }

    return available;
  }

  isUnnamedFavourite(outcomeId: string, event: ISportEvent): boolean {
    const outcomeData = this.getOutcomeData(outcomeId, event),
      outcome = outcomeData && outcomeData.outcome;
    return outcome && outcome.name && _.contains(UNNAMED_FAVOURITES, outcome.name.toLowerCase());
  }

  isValidSilkName(outcome: { silkName: string }): boolean {
    return outcome && (/\.(gif|jpg|jpeg|png)$/i).test(outcome.silkName);
  }

  formatJockeyWeight(racingFormOutcome: IRacingFormOutcome): string { 
    return (racingFormOutcome.allowance && racingFormOutcome.allowance>0) ? racingFormOutcome.jockey + ' (' + racingFormOutcome.allowance + ')' : racingFormOutcome.jockey;
  }

  isJockeyAndTrainer(racingFormOutcome: IRacingFormOutcome):boolean  {
    return _.has(racingFormOutcome, 'jockey') && _.has(racingFormOutcome, 'trainer');
  }

  private getOutcomeData(outcomeId: string, event: ISportEvent): { outcome: IOutcome; market: IMarket } {
    let outcomeData: { outcome: IOutcome; market: IMarket };

    if (!event) {
      return undefined;
    }

    _.forEach(event.markets, (market: IMarket) => {
      _.forEach(market.outcomes, (outcome: IOutcome) => {
        if (outcome.id === outcomeId) {
          outcomeData = { outcome, market };
        }
      });
    });

    return outcomeData;
  }

  private getSilkStyles(racingIds: string[], outcome: IOutcome, imgPosition?: string, isStreamBet?: boolean): ISilkStyleModel {
    const stylesObject = {
      'background-image': `url(${this.IMAGES_RACE_ENDPOINT}/${racingIds.join(',')})`,
      'background-position': `${isStreamBet ? '0' : imgPosition || this.isSilkSmall ? this.SILK_POSITION_SMALL : this.SILK_POSITION} ${
        this.getRacingPostImagePostion(racingIds, outcome.racingFormOutcome.silkName)}px`,
    }
    if(isStreamBet) {
      stylesObject['width'] = this.SILK_SB_WIDTH;
    } else {
      stylesObject['background-size'] =(this.isSilkSmall ? `100% ${racingIds.length * this.SILK_IMAGE_SMALL_HEIGHT}px` : '')
    }
    
    return this.isAggregationMSEnabled && outcome.racingFormOutcome.silkName
      ? stylesObject
      : { 'background-image': `url(${this.IMAGES_ENDPOINT}/racing_post/${outcome.racingFormOutcome.silkName})` };
  }

  private getRacingPostImagePostion(racingIds: string[], id: string): number {
    return -racingIds.indexOf(id.replace(/.(gif|png)/g, '')) * (this.isSilkSmall ? this.SILK_IMAGE_SMALL_HEIGHT : this.SILK_IMAGE_HEIGHT);
  }

  private isValidNumber(outcomeNumber: string | number): boolean {
    const runnerNumber = Number(outcomeNumber);
    return isFinite(runnerNumber) && runnerNumber > 0;
  }
}
