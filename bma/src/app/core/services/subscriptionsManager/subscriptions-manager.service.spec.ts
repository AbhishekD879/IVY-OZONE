import { SubscriptionsManager } from './subscriptions-manager';
import { SubscriptionsManagerService } from './subscriptions-manager.service';

describe('SubscriptionsManagerService', () => {
  let service: SubscriptionsManagerService;

  beforeEach(() => {
    service = new SubscriptionsManagerService();
  });

  it('create', () => {
    expect(service.create()).toBeDefined();
    expect(service.create() instanceof SubscriptionsManager).toBeTruthy();
  });

  describe('SubscriptionsManager', () => {
    let instance: SubscriptionsManager;
    beforeEach(() => {
      instance = service.create();
    });

    it('checkForSubscribe', () => {
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual(['0', '1', '2']);
      expect(instance['subscriptionsMap'].get('0')).toEqual({
        subscribers: 1,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('1')).toEqual({
        subscribers: 1,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('2')).toEqual({
        subscribers: 1,
        subscribed: true
      });
    });

    it('checkForSubscribe: multiple', () => {
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual(['0', '1', '2']);
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual([]);
      expect(instance['subscriptionsMap'].get('0')).toEqual({
        subscribers: 2,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('1')).toEqual({
        subscribers: 2,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('2')).toEqual({
        subscribers: 2,
        subscribed: true
      });
    });

    it('checkForUnsubscribe', () => {
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual(['0', '1', '2']);
      expect(instance.checkForUnsubscribe([0, 1, 2])).toEqual(['0', '1', '2']);
      expect(instance.checkForUnsubscribe(null)).toEqual([]);
      expect(instance['subscriptionsMap']).toEqual(new Map());
    });

    it('checkForUnsubscribe: muptiple', () => {
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual(['0', '1', '2']);
      expect(instance.checkForSubscribe([0, 1, 2])).toEqual([]);
      expect(instance.checkForUnsubscribe([0, 1, 2])).toEqual([]);
      expect(instance['subscriptionsMap'].get('0')).toEqual({
        subscribers: 1,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('1')).toEqual({
        subscribers: 1,
        subscribed: true
      });
      expect(instance['subscriptionsMap'].get('2')).toEqual({
        subscribers: 1,
        subscribed: true
      });
    });
  });
});
