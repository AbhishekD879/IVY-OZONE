import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LiveServIframeService } from '../liveServ/live-serv-iframe.service';
import { ISubscribersRouteUpdate, ILsSubscribeParams, ILsUnsubscribeParams } from '@core/models/subscribe-route.model';

@Injectable()
export class SubscribersRouteService {

  private updates: ISubscribersRouteUpdate = {};
  private cache: any[] = [];
  private appIsLoaded: boolean = false;

  constructor(
    private pubsub: PubSubService,
    private liveServe: LiveServIframeService
  ) {
  }

  init(): void {
    this.pubsub.subscribe('SubscribersRouteService', this.pubsub.API.SUBSCRIBE_LS, (data: ILsSubscribeParams) => {
      this.cacheCheck(data.channel, data.module, data.group);
    });

    this.pubsub.subscribe('SubscribersRouteService', this.pubsub.API.UNSUBSCRIBE_LS, (data: string | ILsUnsubscribeParams) => {
      this.unsubscribeEventHandler(data, true);
    });

    // Wait for APP_IS_LOADED and then subscribe for updates if any Live Channels in cache
    this.pubsub.subscribe('SubscribersRouteService', this.pubsub.API.APP_IS_LOADED, () => {
      if (this.cache.length) {
        this.liveServe.psRegister('oxygenApp', data => this.eventListener(data), this.cache, '0');
      }
      this.appIsLoaded = true;
    });
  }

  private subscribeHandler(): void {
    if (this.appIsLoaded) {
      this.liveServe.psRegister('oxygenApp', data => this.eventListener(data), this.cache, '0');
    }
  }

  private unsubscribeEventHandler(data: string | ILsUnsubscribeParams, isForced?: boolean): void {
    if (data) {
      if (typeof data === 'string') {
        delete this.updates[data];
      } else {
        // remove sport
        if (data.group && this.updates[data.module]) {
          delete this.updates[data.module][data.group];
        } else {
          // remove full group
          delete this.updates[data.module];
        }
      }

      this.cache = [];

      for (const moduleName of Object.keys(this.updates)) {
        for (const groupName of Object.keys(this.updates[moduleName])) {
          this.cache = this.cache.concat(this.updates[moduleName][groupName]);
        }
      }

      this.cache = _.uniq(this.cache);
    }

    if (this.cache.length || isForced) {
      this.subscribeHandler();
    }
  }

  /*
 * Check if there was a change in a cache after subscribe, if yes, then we return true that mean to do resubscribe
 *
 * @params {Array} events
 * @params {String} module
 *
 * @return {Boolean} doSubscribe
 */
  private cacheCheck(events: string[], module: string, group: string = 'all'): void {
    if (!this.updates[module]) {
      this.updates[module] = {};
    }

    if (!this.updates[module][group]) {
      this.updates[module][group] = [];
    }

    const moduleEventsCount = this.updates[module][group].length;
    this.updates[module][group] = _.union(this.updates[module][group], events);

    if (moduleEventsCount !== this.updates[module][group].length) {
      this.cache = _.union(this.cache, events);
      this.subscribeHandler();
    }
  }

  /**
   * This method will be triggered by liveServe in case of updates
   * @param {array || object} args ?
   */
  private eventListener(...args) {
    const liveUpdate = args[0];
    if (_.isArray(liveUpdate)) {
      _.each(liveUpdate, arg => {
        arg.payload = JSON.parse(arg.payload);
      });
    } else {
      liveUpdate.payload = JSON.parse(liveUpdate.payload);
    }

    document.dispatchEvent(
      new CustomEvent('LIVE_SERVE_UPDATE', { detail: { liveUpdate }}));
  }
}
