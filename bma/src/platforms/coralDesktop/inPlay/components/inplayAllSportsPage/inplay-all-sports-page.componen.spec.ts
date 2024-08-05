import { InplayAllSportsPageComponent } from './inplay-all-sports-page.component';
import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';


describe('DesktopInplayAllSportsPageComponent', () => {
  let component: InplayAllSportsPageComponent,
    inplayMainService,
    cmsService,
    pubsubService,
    inplayConnectionService,
    changeDetectorRef;

  beforeEach(() => {
    inplayMainService = {
      clearDeletedEventFromSport: jasmine.createSpy('clearDeletedEventFromSport'),
      getSportUri: jasmine.createSpy().and.returnValue(true)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of([
        {
          InPlayCompetitionsExpanded: {
            competitionsCount: 10
          }
        }
      ])),
    };
    pubsubService = {
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a: string, eventName: string[] | string, fn: Function) => {
        if (eventName === pubsubService.API.DELETE_EVENT_FROM_CACHE) {
          fn();
        } else {
          spyOn(component, 'ngOnInit');
          spyOn(component, 'ngOnDestroy');
          fn();
        }
      }),
      API: pubSubApi
    };
    inplayConnectionService = {
      setConnectionErrorState: jasmine.createSpy('setConnectionErrorState')
    };

    component = new InplayAllSportsPageComponent(
      pubsubService,
      inplayMainService,
      cmsService,
      inplayConnectionService,
      changeDetectorRef
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayAllSportsPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#ngOnInit', () => {
    component.ngOnInit();
    expect(pubsubService.subscribe.calls.allArgs()[0]).toEqual(
      ['inplayAllSportsPage', pubsubService.API.DELETE_EVENT_FROM_CACHE, jasmine.any(Function)]
    );
    expect(pubsubService.subscribe.calls.allArgs()[1]).toEqual(
      ['inplayAllSportsPage', pubsubService.API.RELOAD_IN_PLAY, jasmine.any(Function)]
    );
    expect(inplayConnectionService.setConnectionErrorState).toHaveBeenCalledWith(false);
    expect(component.viewByFilters).toBeDefined();
    expect(inplayMainService.clearDeletedEventFromSport).toHaveBeenCalledWith({}, undefined, [ 'livenow', 'upcoming' ]);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('OnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayAllSportsPage');
  });
});
