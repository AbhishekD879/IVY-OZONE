import { Injectable } from '@angular/core';
import { SubscriptionsManager } from './subscriptions-manager';

@Injectable()
export class SubscriptionsManagerService {

  create() {
    return new SubscriptionsManager();
  }
}
