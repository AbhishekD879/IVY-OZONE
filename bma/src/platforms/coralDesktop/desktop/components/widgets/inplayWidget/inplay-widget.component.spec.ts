import { of } from 'rxjs';
import { InplayWidgetComponent } from './inplay-widget.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CDInplayWidgetComponent', () => {
  let component: InplayWidgetComponent;
  let inplayHelperService, routingHelperService, pubSubService, userService, storageService,
    sportEventHelperService, carouselService, router;
  beforeEach(() => {
    inplayHelperService = {
      sendGTM: jasmine.createSpy('sendGTM').and.callFake((label, sport) => {
        return console.warn(label, sport);
      }),
      getData: jasmine.createSpy('getData').and.returnValue(of([])),
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    } as any;
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/football')
    } as any;
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('subscrunsubscribeibe'),
      publish: jasmine.createSpy('publish')
    } as any;
    userService = {
      username: 'testUser'
    } as any;
    storageService = {
      remove: jasmine.createSpy('remove'),
      set: jasmine.createSpy('set')
    } as any;

    sportEventHelperService = {} as any;
    carouselService = {} as any;
    router = {} as any;

    spyOn(console, 'warn');

    component = new InplayWidgetComponent(inplayHelperService, routingHelperService, sportEventHelperService, pubSubService,
      router, carouselService, storageService, userService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send GTM tracking and clear last remember tab on In-play page', () => {
    component.sportName = 'football';
    component.sendViewAllGTM();
    expect(inplayHelperService.sendGTM).toHaveBeenCalledWith('view all', 'football');
    expect(storageService.remove).toHaveBeenCalledWith(`inPlay-${userService.username}`);
  });

  it('should send GTM tracking and set new remember tab on In-play page', () => {
    component.sportName = 'football';
    component.events.length = 5;
    component.sendViewAllGTM();
    expect(inplayHelperService.sendGTM).toHaveBeenCalledWith('view all', 'football');
    expect(storageService.set).toHaveBeenCalledWith(`inPlay-${userService.username}`, 'football');
  });

  describe('ngOnit', () => {
    it('should unsubscribe for undislayed event', () => {
      pubSubService.subscribe.and.callFake((a, event, cb) => {
        if (event === pubSubService.API.DELETE_EVENT_FROM_CACHE) {
          spyOn(component as any,'checkWidgetVisibility').and.callThrough();

          cb(111);

          expect(inplayHelperService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([{ id: 111 }]);
          expect(component['checkWidgetVisibility']).toHaveBeenCalled();
        }
      });

      inplayHelperService.getData.and.returnValue(of([{ id: 111} as any]));

      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'inPlayWidget',
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
    });

    it('should not unsubscribe for undislayed event', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (b === pubSubService.API.DELETE_EVENT_FROM_CACHE) {
          spyOn(component as any,'checkWidgetVisibility').and.callThrough();

          cb(222);

          expect(inplayHelperService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
          expect(component['checkWidgetVisibility']).not.toHaveBeenCalled();
        }
      });
      inplayHelperService.getData.and.returnValue(of([{ id: 111} as any]));

      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'inPlayWidget',
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
    });

    it('should reload component after sleep mode', () => {
      pubSubService.subscribe.and.callFake((a, b, cb) => {
        if (b === pubSubService.API.RELOAD_IN_PLAY) {
          spyOn(component as any,'ngOnDestroy');
          spyOn(component as any,'ngOnInit');

          cb();

          expect(component.ngOnInit).toHaveBeenCalled();
          expect(component.ngOnDestroy).toHaveBeenCalled();
        }
      });
      inplayHelperService.getData.and.returnValue(of([{ id: 111} as any]));

      component.ngOnInit();
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('inPlayWidget');
  });
});
