import { of as observableOf, throwError as observableThrowError } from 'rxjs';
import { PromotionDialogComponent } from './promotion-dialog.component';
import { ISpPromotion } from '@promotions/models/sp-promotion.model';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('PromotionDialogComponent', () => {
  let component, deviceService, windowRef, data, pubSubService;
  const testStr = 'TestString';

  beforeEach(() => {
    data = [{ marketLevelFlag: testStr, eventLevelFlag: testStr }];
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('classList.add'),
            remove: jasmine.createSpy('classList.remove')
          }
        }
      }
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    component = new PromotionDialogComponent(deviceService, windowRef, pubSubService);
    component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') } };
  });

  it(`should be instance of 'AbstractDialog'`, () => {
    expect(AbstractDialogComponent).isPrototypeOf(component);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('open', () => {
    it('should get data', () => {
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      const openSpy = spyOn(PromotionDialogComponent.prototype['__proto__'], 'open');
      component.open();

      expect(openSpy).toHaveBeenCalled();
      expect(component.promo).toEqual(data[0] as ISpPromotion);
      expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('promotion-modal-open');
    });
  });

  describe('getPromotion', () => {
    it('should get data', () => {
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.promo).toEqual(data[0] as ISpPromotion);
    });

    it(`property 'loaded' should be Truthy if loaded data`, () => {
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.loaded).toBeTruthy();
    });

    it(`should get data if 'marketLevelFlag' is equal 'flag'`, () => {
      data[0].eventLevelFlag = null;
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.promo).toEqual(data[0] as ISpPromotion);
    });

    it(`should NOT get data if 'marketLevelFlag' and 'eventLevelFlag' are NOT equal 'flag'`, () => {
      data[0].marketLevelFlag = null;
      data[0].eventLevelFlag = null;
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.promo).toBeUndefined();
    });


    it(`property 'loaded' should be Falsy if NOT loaded data`, () => {
      data[0].marketLevelFlag = null;
      data[0].eventLevelFlag = null;
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.loaded).toBeFalsy();
    });

    it(`should get data if 'eventLevelFlag' is equal 'flag'`, () => {
      data[0].eventLevelFlag = testStr;
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };
      component.getPromotion();

      expect(component.promo).toEqual(data[0] as ISpPromotion);
    });

    it(`htmlMarkup in cmsContent  should be empty  if 'promo' has NOT 'promotionText'`, () => {
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };

      component.getPromotion();

      expect(component.cmsContent).toEqual(jasmine.objectContaining({htmlMarkup : ''}));
      expect(component.params.getSpPromotionData).toHaveBeenCalled();
      expect(component.loaded).toBeTruthy();
    });

    it(`htmlMarkup in cmsContent  should be transformed  if 'promo' has 'promotionText'`, () => {
      data[0]['promotionText'] = `<a href='http://google.com'>Google</a>`;
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf(data))
      };

      component.getPromotion();

      expect(component.cmsContent).toEqual(jasmine.objectContaining(
        {
          htmlMarkup : `<a href='http://google.com'>Google</a>`
        }
      ));
      expect(component.params.getSpPromotionData).toHaveBeenCalled();
      expect(component.loaded).toBeTruthy();
    });

    it('should call error', async() => {
      component.params = {
        flag: testStr,
        getSpPromotionData: jasmine.createSpy().and.returnValue(observableThrowError(null))
      };
      component.getPromotion();

      expect(component.loaded).toBeTrue();
    });
  });

  describe('openOverlay', () => {
    it(`should call 'openPromotionOverlay`, () => {
      component.params = {
        openPromotionOverlay: jasmine.createSpy()
      };
      component.openOverlay();

      expect(component.params.openPromotionOverlay).toHaveBeenCalledTimes(1);
    });
  });

  it(`closeThisDialog`, () => {
    component.promo = {templateMarketName:'test market'}
    const closeDialogSpy = spyOn(PromotionDialogComponent.prototype['__proto__'], 'closeDialog');
    component.closeThisDialog();
    expect(closeDialogSpy).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TWO_UP_TRACKING, { action: 'close', marketName: 'test market' });
    expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('promotion-modal-open');
  });
});
