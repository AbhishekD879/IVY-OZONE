import { InplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';


describe('InplayAllSportsPageComponent', () => {
  let component: InplayAllSportsPageComponent,
    inplayMainService,
    cmsService,
    pubsubService,
    changeDetector,
    inplayConnectionService;


  beforeEach(() => {
    inplayMainService = {
      clearDeletedEventFromSport: jasmine.createSpy('clearDeletedEventFromSport'),
      getSportUri: jasmine.createSpy().and.returnValue(true),
      getStructureData: jasmine.createSpy('getStructureData')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf([
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
    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };

  component = new InplayAllSportsPageComponent(
    pubsubService,
    inplayMainService,
    cmsService,
    inplayConnectionService,
    changeDetector
    );
  });


  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayAllSportsPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#ngOnInit with error', () => {
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
    expect(inplayMainService.getStructureData).not.toHaveBeenCalled();
    expect(changeDetector.detectChanges).toHaveBeenCalled();
  });

  it('#ngOnInit', () => {
    inplayMainService.getSportUri.and.returnValue(false);
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
    expect(inplayMainService.getStructureData).toHaveBeenCalled();
    expect(changeDetector.detectChanges).toHaveBeenCalled();
  });

  it('OnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayAllSportsPage');
  });
});
