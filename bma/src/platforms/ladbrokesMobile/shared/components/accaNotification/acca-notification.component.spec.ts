import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

import { AccaNotificationComponent } from '@ladbrokesMobile/shared/components/accaNotification/acca-notification.component';
import {
  AccaNotificationComponent as BaseAccaNotificationComponent
} from '../../../../../app/shared/components/accaNotification/acca-notification.component';

describe('LadbrokesAccaNotificationComponent', () => {
  let component: AccaNotificationComponent,
    localeService,
    nativeBridgeService,
    userService,
    fracToDec,
    domTools,
    pubsub,
    deviceService,
    GTM,
    windowRef,
    cmsService,
    changeDetectorRef,
    filterService;

  beforeEach(() => {
    fracToDec = {};
    domTools = {};
    deviceService = {};
    GTM = {};
    filterService = {};
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(a => a)
    };
    nativeBridgeService = {
      accaNotificationChanged: jasmine.createSpy('accaNotificationChanged')
    };
    userService = {
      currencySymbol: '$'
    };
    windowRef = {
      document: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    cmsService = jasmine.createSpyObj(['getSystemConfig']);

    component = new AccaNotificationComponent(
      nativeBridgeService,
      userService,
      fracToDec,
      domTools,
      pubsub,
      deviceService,
      GTM,
      windowRef,
      localeService,
      cmsService,
      changeDetectorRef,
      filterService
    );
  });

  it('should define default acca stake', () => {
    expect(component.accaBaseStake).toBe(10);
  });

  describe('updateAccaData', () => {
    let superSpy;

    beforeEach(() => {
      superSpy = spyOn(BaseAccaNotificationComponent.prototype, 'updateAccaData');
    });

    it('should execute super first and dont subscribe by itself', () => {
      component.updateAccaData({});

      expect(superSpy).toHaveBeenCalledWith({});
      expect(pubsub.subscribe).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });

    it('should define "accaPaysOfferText" if potentialPayout is present', () => {
        const ACCAData = {
          potentialPayout: 50,
          stake: 5,
          price: '10',
          translatedType: 'ACC5'
        };

        component.updateAccaData(ACCAData);

        expect(localeService.getString).toHaveBeenCalledWith('bs.accaNotificationPays');
        expect(component.accaPaysOfferText).toEqual(`$5 bs.accaNotificationPays $50.00`);
        expect(component.betType).toEqual(`Acca (5)`);
        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      }
    );

    it('should set define betType if type is Double', () => {
        const ACCAData = {
          potentialPayout: 50,
          stake: 5,
          price: '10',
          translatedType: 'Double'
        };

        component.updateAccaData(ACCAData);

        expect(component.accaPaysOfferText).toEqual(`$5 bs.accaNotificationPays $50.00`);
        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      }
    );

    it('should set a default stake', () => {
        const ACCAData = {
          potentialPayout: 10,
          stake: 0,
          price: '10',
          translatedType: 'Double'
        };

        component.updateAccaData(ACCAData);

        expect(component.accaPaysOfferText).toEqual(`$10 bs.accaNotificationPays $100.00`);
        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      }
    );

    it('should not set ‘accaPaysOfferText’ if has not potentialPayout', () => {
        component.updateAccaData({});

      expect(localeService.getString).not.toHaveBeenCalled();
      expect(component.accaPaysOfferText).toEqual(undefined);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
      }
    );
  });
});
