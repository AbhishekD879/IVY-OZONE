import { Injectable } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import * as _ from 'underscore';
import { RacingService as coralRacingService } from '@core/services/sport/racing.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { TimeFormService } from '@core/services/racing/timeForm/time-form.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { DailyRacingService } from '@core/services/racing/dailyRacing/daily-racing.service';
import { EventService } from '@sb/services/event/event.service';
import { TemplateService } from '@shared/services/template/template.service';
import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LiveUpdatesWSService } from '@core/services/liveUpdatesWS/liveUpdatesWS.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { LpAvailabilityService } from '@core/services/lpAvailability/lp-availability.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RacingPostService } from '@coreModule/services/racing/racingPost/racing-post.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

@Injectable()
export class RacingService extends coralRacingService {
  constructor(
    protected timeformService: TimeFormService,
    protected ukToteService: UkToteService,
    protected dailyRacingService: DailyRacingService,
    protected eventFactory: EventService,
    protected templateService: TemplateService,
    protected timeService: TimeService,
    protected filtersService: FiltersService,
    protected liveUpdatesWSService: LiveUpdatesWSService,
    protected channelService: ChannelService,
    protected lpAvailabilityService: LpAvailabilityService,
    protected commandService: CommandService,
    protected localeService: LocaleService,
    protected racingYourcallService: RacingYourCallService,
    protected pubSubService: PubSubService,
    protected cmsService: CmsService,
    protected racingPostService: RacingPostService,
    protected routingHelperService: RoutingHelperService
  ) {
    super(
      timeformService,
      ukToteService,
      dailyRacingService,
      eventFactory,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      lpAvailabilityService,
      commandService,
      localeService,
      racingYourcallService,
      pubSubService,
      cmsService,
      racingPostService,
      routingHelperService
    );
  }

  sortRacingMarketsByTabs(markets: IMarket[], eventId: string) {
    const raceMarkets: any = this.initRaceMarketsObj();
    let marketsArray = [];

    _.forEach(markets, (market: IMarket) => {
      if (market.eventId === eventId) {
        market.label = market.templateMarketName === 'Win or Each Way' ?
          this.localeService.getString('sb.winOrEachWay') : market.name;
        if (raceMarkets.mainMarkets.hasOwnProperty(market.templateMarketName)) {
          market.path = raceMarkets.mainMarkets[market.templateMarketName].path;
          marketsArray.push(market);
        } else if (this.checkTemplateMarketName(raceMarkets.topFinishMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'topFinishMarkets', 'isTopFinish');
          this.setGroupedMarketHeader(raceMarkets.topFinishMarkets, market);
        } else if (this.checkTemplateMarketName(raceMarkets.toFinishMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'toFinishMarkets', 'isToFinish');
          this.setGroupedMarketHeader(raceMarkets.toFinishMarkets, market);
        } else if (this.checkTemplateMarketName(raceMarkets.insuranceMarkets, market)) {
          this.setupMarket(market, raceMarkets, 'insuranceMarkets', 'insuranceMarkets');
          this.setGroupedMarketHeader(raceMarkets.insuranceMarkets, market);
        } else {
          market.path = this.routingHelperService.encodeUrlPart(market.name);
          marketsArray.push(market);
        }
      }
    });

    this.collectSubMarkets(raceMarkets, marketsArray);
    const order = ['customOrder', 'displayOrder', 'name'];

    marketsArray = this.filtersService.orderBy(marketsArray, order);
    return marketsArray;
  }

  sortMarketsName(eventEntity: ISportEvent, sortOrderArray) {
    if (!sortOrderArray) { return eventEntity; }
    _.forEach(eventEntity.markets, market => {
      for (let j = 0; j < sortOrderArray.length; j++) {
        if (market.name === sortOrderArray[j] || sortOrderArray[j].indexOf(market.templateMarketName) > -1) {
          market.customOrder = j;
          break;
        }
      }
      market.displayOrder = Number((market as any).displayOrder);
      market.terms = this.templateService.genTerms(market);
    });

    eventEntity.uiClass = this.templateService.genClass(eventEntity);

    return eventEntity;
  }
}
