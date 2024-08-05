import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';

import { IFreebetToken, IAccountFreebetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ISSRequestParamsModel } from '@core/models/ss-request-params.model';
import { IMarketsChildResponse, IMarketsResponse, ILiveUpdate } from '@core/models/private-markets.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { TemplateService } from '@shared/services/template/template.service';
import { EventService } from '@sb/services/event/event.service';
import { Observable, from, of, throwError } from 'rxjs';
import { catchError, map, mergeMap } from 'rxjs/operators';


@Injectable()
export class PrivateMarketsService {
  storedPrivateMarkets: IFreebetToken[];
  serviceName: string = 'PrivateMarketsService';

  constructor(
    private eventService: EventService,
    private templateService: TemplateService,
    private pubSubService: PubSubService,
    private liveServConnectionService: LiveServConnectionService,
    private nativeBridgeService: NativeBridgeService,
    private bppService: BppService,
    private userService: UserService,
    private siteServerRequestHelperService: SiteServerRequestHelperService
  ) {
    this.privateMarketsUpdateHandler = this.privateMarketsUpdateHandler.bind(this);

    // store private markets , received from auth/user during login flow.
    this.pubSubService.subscribe(this.serviceName, 'STORE_PRIVATE_MARKETS', (privateMarkets: IFreebetToken[]) => {
      this.storedPrivateMarkets = privateMarkets;

      this.setupCacheRemoveLogic();
    });
  }

  markets(): Observable<ISportEvent[]> {
    if (this.storedPrivateMarkets) {
      return this.getPrivateMarketsEvents(this.storedPrivateMarkets);
    }

    return this.getPrivateMarkets();
  }

  setupCacheRemoveLogic(): void {
    this.pubSubService.subscribe(this.serviceName, this.pubSubService.API.SESSION_LOGOUT, () => {
      // cleanup cache on logout
      this.storedPrivateMarkets = undefined;
    });

    this.pubSubService.subscribe(this.serviceName, this.pubSubService.API.BETS_COUNTER_PLACEBET, () => {
      // cleanup cache on logout
      this.storedPrivateMarkets = undefined;
    });
  }

  /**
   * Unsubscribe from LP updates
   * @param {Object} events
   */
  unsubscribe(events: ISportEvent[]): void {
    this.liveServConnectionService.unsubscribe(this.getIds(events), this.privateMarketsUpdateHandler);
  }

  /**
   * Subscribe for live price updates
   * @param {Object} events
   */
  subscribe(events: ISportEvent[]): void {
    this.liveServConnectionService.connect().subscribe(() => {
      this.liveServConnectionService.subscribe(this.getIds(events), this.privateMarketsUpdateHandler);
    });
  }

  disconnect(): void {
    this.liveServConnectionService.disconnect();
  }

  /**
   * Get Events for Private Markets events from SS
   * @param freebetTokens
   */
  getPrivateMarketsEvents(freebetTokens: IFreebetToken[]): Observable<ISportEvent[]> {
    return from(this.eventService.cachedEventsByFn(() => this.getDetailedPrivateBets(freebetTokens).toPromise(), 'privateMarkets')())
      .pipe(
        mergeMap((events: ISportEvent[]) => {
          this.nativeBridgeService.arePrivateMarketsAvailable(!!(events && events.length));

          return of(events || []);
        })
      );
  }

  /**
   * Gets private markets.
   */
  private getPrivateMarkets(): Observable<ISportEvent[]> {
    return this.bppService.send('privateMarkets')
      .pipe(
        catchError(() => {
          console.error('Private markets freeBet error');

          this.nativeBridgeService.arePrivateMarketsAvailable(false);

          return throwError([]);
        }),
        mergeMap((body: IAccountFreebetsResponse) => {
          if (!body.response.model.freebetToken) {
            return of([]);
          }

          return this.getPrivateMarketsEvents(body.response.model.freebetToken);
        })
      );
  }

  /**
   * Return detail private markets from SiteServe.
   */
  private getDetailedPrivateBets(freeBetToken: IFreebetToken[]): Observable<ISportEvent[]> {
    const request: ISSRequestParamsModel = {
      marketIds: this.getTokensIds(freeBetToken) || [],
      simpleFilters: 'includeRestricted=true&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A'
    };

    if (request.marketIds.length > 0) {
      return from(this.siteServerRequestHelperService.getEventsByMarkets(request)).pipe(
        map(ssMarkets => {
          const events = this.normalizeData(freeBetToken, ssMarkets);

          return this.templateService.filterBetInRunMarkets(events);
        }),
        catchError((error) => {
          console.error('Private markets error:', error);
          return of([]);
        })
      );
    }

    return of([]);
  }

  /**
   * Gets only tokens ids.
   */
  private getTokensIds(freeBetToken: IFreebetToken[]): number[] {
    return _.uniq(_.reduce(freeBetToken, (ids, freeBet: IFreebetToken ) => {
      ids.push(Number(freeBet.freebetTokenRestrictedSet.id));
      return ids;
    }, []));
  }

  /**
   * Normalize data for this object.
   */
  private normalizeData(freeBetToken: IFreebetToken[], ssMarkets: IMarketsResponse): ISportEvent[] {
    const events = [];

    // normalize event structure
    _.each(ssMarkets.SSResponse.children, (eventChild: IMarketsChildResponse) => {
      if (eventChild.event) {
        eventChild.event.markets = [];
        _.each(eventChild.event.children, (marketChild) => {
          marketChild.market.marketName = marketChild.market.name;
          marketChild.market.outcomes = [];
          _.each(marketChild.market.children, (outcomeChild: any) => {
            marketChild.market.outcomes.push(outcomeChild.outcome);
          });
          eventChild.event.markets.push(marketChild.market);
        });
        events.push(eventChild.event);
      }
    });

    // extend markets and outcomes with token data
    _.each(events, (event: ISportEvent) => {
      _.each(event.markets, (market: IMarket) => {
        _.each(freeBetToken, (token: IFreebetToken) => {
          const param = {
            name: token.freebetOfferName,
            freebetTokenId: token.freebetTokenId,
            id: token.freebetTokenRestrictedSet.id,
            allShown: false
          };
          if (market.id === token.freebetTokenRestrictedSet.id) {
            _.extend(market, param);
            _.each(market.outcomes, (outcome: IOutcome) => {
              outcome.amount = this.userService.currencySymbol + token.freebetTokenValue;
              delete outcome.outcomeMeaningMinorCode; // BMA-4768
              if (outcome.children && outcome.children[0].price) {
                outcome.prices = [outcome.children[0].price];
              } else {
                _.extend(outcome.prices, [ { priceType: market.priceTypeCodes } ]);
              }
            });
          }
        });
      });
    });

    return events;
  }

  /**
   * Get outcome, event, market ids
   */
  private getIds(events: ISportEvent[]): string[] {
    const ids = {
      outcomes: [],
      markets: [],
      events: []
    };
    _.each(events, (event: ISportEvent) => {
      ids.events.push(event.liveServChannels.slice(0, -1));
      _.each(event.markets, market => {
        ids.markets.push(market.liveServChannels.slice(0, -1));
        _.each(market.outcomes, outcome => {
          ids.outcomes.push(outcome.liveServChannels.slice(0, -1));
        });
      });
    });

    return _.uniq([].concat(ids.outcomes).concat(ids.markets)
      .concat(ids.events));
  }

  /**
   * Handler for updates related to private markets tab
   * @param {Object} update
   */
  private privateMarketsUpdateHandler(update: ILiveUpdate): void {
    if (update.type === 'MESSAGE') {
      const payload = update.message,
        channel = update.channel.name,
        updatedObject = { channel,
          channel_number: update.event.id,
          payload,
          subject_number: update.channel.id,
          subject_type: update.subChannel.type
        };

      this.pubSubService.publish(this.pubSubService.API.LIVE_SERVE_MS_UPDATE, [updatedObject]);
    }
  }
}

