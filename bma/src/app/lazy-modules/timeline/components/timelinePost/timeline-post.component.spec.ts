import { TimelinePostComponent } from '@lazy-modules/timeline/components/timelinePost/timeline-post.component';

describe('TimelinePostComponent', () => {
  let component;
  let navigationService;
  let timelineService;

  beforeEach(() => {
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    timelineService = {
      gtm: jasmine.createSpy('gtm')
    };
    component = new TimelinePostComponent(navigationService, timelineService);
    component.stateChange.emit = jasmine.createSpy('stateChangeEmit');
  });

  it('#ngOnInit should not get promo image url when no template', () => {
    component.post = {} as any;
    component['getPromoImgUrl'] = jasmine.createSpy('getPromoImgUrl');
    component.ngOnInit();
    expect(component['getPromoImgUrl']).not.toHaveBeenCalled();
  });

  it('#ngOnInit should not get promo image url when no topRightCornerImagePath', () => {
    component.post = {
      template: {}
    } as any;
    component['getPromoImgUrl'] = jasmine.createSpy('getPromoImgUrl');
    component.ngOnInit();
    expect(component['getPromoImgUrl']).not.toHaveBeenCalled();
  });

  it('#ngOnInit should get promo image url', () => {
    const imageUrl = 'https://cms-dev0.ladbrokes.com/cms/images/some-image.png';
    component.post = {
      template: {
        topRightCornerImagePath: '/images/some-image.png'
      }
    } as any;
    component['getPromoImgUrl'] = jasmine.createSpy('getPromoImgUrl').and.returnValue(imageUrl);
    component.ngOnInit();
    expect(component['getPromoImgUrl']).toHaveBeenCalled();
    expect(component.promoImageUrl).toBe(imageUrl);
  });

  it('#getPromoImgUrl', () => {
    const imageUrl = 'https://cms-dev0.ladbrokes.com/cms/images/some-image.png';
    component.post = {
      template: {
        topRightCornerImagePath: '/images/some-image.png'
      }
    } as any;
    component.cmsUri = 'https://cms-dev0.ladbrokes.com/cms';
    expect(component['getPromoImgUrl']()).toBe(imageUrl);
  });

  it('#openUrl redirect url is present', () => {
    component.gtm = jasmine.createSpy('gtm');
    component.post = {
      template: {
        name: 'headerText',
        id: '123'
      }
    };
    component.gtmModuleBrandName = 'event category';
    component.openUrl('test');
    expect(navigationService.openUrl).toHaveBeenCalledWith('test', true);
    expect(timelineService.gtm).toHaveBeenCalledWith('navigation', {
      eventLabel: 'test',
      dimension114: 'headerText',
      dimension115: '123'
    }, 'event category');
    expect(component.stateChange.emit).toHaveBeenCalled();
  });

  it('#openUrl no redirect url', () => {
    component.openUrl(null);
    expect(navigationService.openUrl).not.toHaveBeenCalled();
  });

  describe('ngOnChanges', () => {
    it('event has selection', () => {
      component['checkIfSelnAvailable'] = jasmine.createSpy();
      component.post = {
        selectionEvent: {}
      };

      component.ngOnChanges();
      expect(component.checkIfSelnAvailable).toHaveBeenCalled();
    });

    it('event without selection', () => {
      component['checkIfSelnAvailable'] = jasmine.createSpy();
      component.post = {};

      component.ngOnChanges();
      expect(component.checkIfSelnAvailable).not.toHaveBeenCalled();
    });
  });

  describe('checkIfSelnAvailable', () => {
    beforeEach(() => {
      component.post = {
        selectionEvent: {
          obEvent: {
            markets: [{
              outcomes: [{}]
            }]
          }
        }
      };
    });

    it('isNA falsy by default', () => {
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeFalsy();
    });

    it('outcome isDisplayed === false', () => {
      component.post.selectionEvent.obEvent.markets[0].outcomes[0].isDisplayed = false;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('outcome isResulted = true', () => {
      component.post.selectionEvent.obEvent.markets[0].outcomes[0].isResulted = true;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('market isDisplayed === false', () => {
      component.post.selectionEvent.obEvent.markets[0].isDisplayed = false;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('market isResulted = true', () => {
      component.post.selectionEvent.obEvent.markets[0].isResulted = true;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('market isMarketBetInRun === false, rawIsOffCode === `Y`', () => {
      component.post.selectionEvent.obEvent.markets[0].isMarketBetInRun = false;
      component.post.selectionEvent.obEvent.rawIsOffCode = 'Y';
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('market isMarketBetInRun === false, rawIsOffCode === `N`', () => {
      component.post.selectionEvent.obEvent.markets[0].isMarketBetInRun = false;
      component.post.selectionEvent.obEvent.rawIsOffCode = 'N';
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeFalsy();
    });

    it('event isDisplayed === false', () => {
      component.post.selectionEvent.obEvent.isDisplayed = false;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });

    it('event isResulted = true', () => {
      component.post.selectionEvent.obEvent.isResulted = true;
      component['checkIfSelnAvailable']();
      expect(component.post.selectionEvent.isNA).toBeTruthy();
    });
  });
});
