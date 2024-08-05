import { ISubscriptionInfo } from '../models/subscriptionInfo.model';
export class SubscriptionsManager {

  private subscriptionsMap: Map<string, ISubscriptionInfo>;

  constructor() {
    this.subscriptionsMap = new Map<string, ISubscriptionInfo>();
  }

  checkForSubscribe(ids: Array<string|number>): Array<string> {
    const idsForSubscribe = [];

    [... new Set(ids)].forEach(id => {
      const stringId = String(id);
      if (this.subscriptionsMap.has(stringId)) {
        this.subscriptionsMap.get(stringId).subscribers++;
        this.subscriptionsMap.get(stringId).subscribed = true;
      } else {
        if (!this.subscriptionsMap.has(stringId)) {
          this.subscriptionsMap.set(stringId, {
            subscribers: 1,
            subscribed: true
          });
        }
      }
      // emit subscribe event only for the first subscription
      if (this.subscriptionsMap.get(stringId).subscribers === 1) {
        idsForSubscribe.push(stringId);
      }
    });

    return idsForSubscribe;
  }

  checkForUnsubscribe(ids: Array<number|string>): Array<string> {
    const idsForUnsubscribe = [];

    if(!ids) {
      return [];
    }

    ids.forEach(id => {
      const stringId = String(id);
      if (this.subscriptionsMap.has(stringId) && this.subscriptionsMap.get(stringId).subscribers > 0) {
        const subscribers: number = this.subscriptionsMap.get(stringId).subscribers -= 1;
        if (subscribers === 0) {
          this.subscriptionsMap.delete(stringId);
          idsForUnsubscribe.push(stringId);
        }
      }
    });

    return idsForUnsubscribe;
  }
}
