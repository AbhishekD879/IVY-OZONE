import { Injectable, NgZone } from '@angular/core';
import { pubSubApi } from './pubsub-api.constant';

@Injectable({
  providedIn: 'root'
})

export class PubSubService {
  private subscriptions: { [key: string]: any } = {};
  constructor (private ngZone: NgZone) {}
  /**
   * Get available APIs which pubsub can execute
   * @constructor
   */
  get API(): { [key: string]: string } {
      return pubSubApi;
  }
set API(value:{ [key: string]: string }){}
  /**
   * Publish event to channel
   * @param {string} channel
   * @param {*|[*]} channelFunctionArguments
   * @param {Boolean} isAsync
   */
  publish(channel: string, channelFunctionArguments: any | Array<any> = [], isAsync: boolean = true) {
      const channelFunctionsBySubscriberName = this.subscriptions[channel];
      const channelFunctionArgumentsArray = Array.isArray(channelFunctionArguments)
          ? channelFunctionArguments : [channelFunctionArguments];

      if (channelFunctionsBySubscriberName) {
          if (isAsync) {
              setTimeout(() => {
                  this.executeFns(channelFunctionsBySubscriberName, channelFunctionArgumentsArray);
              }, 0);
          } else {
              this.executeFns(channelFunctionsBySubscriberName, channelFunctionArgumentsArray);
          }
      }
  }

  /**
   * Subscribe to one or more channels
   * @param {string} subscriberName
   * @param {string|[string]} channel
   * @param {function} channelFunction
   */
  subscribe(subscriberName: string, channel: any, channelFunction: Function) {
      const channels = Array.isArray(channel) ? channel : [channel];

      channels.forEach((channelName: string) => {
          if (!this.subscriptions[channelName]) {
              this.subscriptions[channelName] = {};
          }

          this.subscriptions[channelName][subscriberName] = channelFunction;
      });
  }

  /**
   * Unsubscribe from all channels
   * @param {string} subscriberName
   */
  unsubscribe(subscriberName: string) {
    let subscribersCount = 0;

    for (const channelFunctionsBySubscriberName in this.subscriptions) {
      if (Object.prototype.hasOwnProperty.call(this.subscriptions, channelFunctionsBySubscriberName)) {
        if (this.subscriptions[channelFunctionsBySubscriberName][subscriberName]) {
          subscribersCount++;
          delete this.subscriptions[channelFunctionsBySubscriberName][subscriberName];
        }
      }
    }

    if (!subscribersCount) {
      console.warn(`Subscriptions for: "${subscriberName}" doesn't exist`);
    }
  }

  /**
   * publish to sync function executing
   * @param channel
   * @param channelFunctionArguments
   */
  publishSync(channel: string, channelFunctionArguments: any | Array<any> = []) {
      this.publish(channel, channelFunctionArguments, false);
  }

  /**
   * Executes functions with arguments in sync or async mode
   * @param {Object} fns with functions list
   * @param {*} args - arguments for functions
   * @private
   */
  private executeFns(fns: { [key: string]: Function }, args: Array<any>) {
    for (const fn in fns) {
      if (Object.prototype.hasOwnProperty.call(fns, fn)) {
        this.ngZone.runOutsideAngular(() => {
          fns[fn](...args);
        });
      }
    }
  }
}
