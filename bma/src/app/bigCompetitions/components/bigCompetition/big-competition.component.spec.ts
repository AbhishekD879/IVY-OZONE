import { of as observableOf, throwError } from 'rxjs';
import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';
import {
  IBCData,
  ICompetitionTab
} from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BigCompetitionComponent', () => {
  let component: BigCompetitionComponent;

  let competitionsService;
  let participantsService;
  let pubsubService;
  let liveUpdatesService;
  let routingState;
  let route;
  let router;
  let competition;
  let tab;
  let user;
  const updateEventService = {} as any;

  beforeEach(() => {
    competition = {
      hasSubtabs: false,
      id: 'id',
      path: 'path',
      title: 'title',
      uri: 'uri',
      categoryId: 10,
      competitionModules: [],
      competitionTabs: [],
      competitionParticipants: []
    } as IBCData;

    tab = {
      id: 'id',
      path: 'path',
      url: '',
      competitionSubTabs: []
    } as ICompetitionTab;

    competitionsService = {
      getTabs: jasmine.createSpy().and.returnValue(observableOf(competition)),
      storeCategoryId: jasmine.createSpy(),
      findTab: jasmine.createSpy().and.returnValue({
        id: 'id',
        path: 'path',
        url: '',
        competitionSubTabs: []
      })
    };
    participantsService = {
      store: jasmine.createSpy(),
      getFlagsList: jasmine.createSpy()
    };
    user = {
      bonusSuppression: true
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe')
        .and.callFake((a: string, b: string[] | string, fn: Function) => {
          if (b !==  'RELOAD_BIG_COMPETITIONS') {
            spyOn(component, 'ngOnDestroy');
            fn();
          }
        }),
      unsubscribe: jasmine.createSpy(),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      }
    };
    liveUpdatesService = {
      reconnect: jasmine.createSpy().and.returnValue(observableOf(null))
    };
    routingState = {
      getRouteParam: jasmine.createSpy().and.returnValue('')
    };
    route = {
      url: observableOf([]),
      navigateByUrl: jasmine.createSpy(),
      snapshot: {
        paramMap: { get: () => 'premier-league' }
      }
    };
    router = {
      events: {
        subscribe: jasmine.createSpy()
      },
      navigateByUrl: jasmine.createSpy()
    };

    component = new BigCompetitionComponent(
      competitionsService,
      participantsService,
      pubsubService,
      liveUpdatesService,
      routingState,
      route,
      router,
      user,
      updateEventService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  xit('#ngOnInit', fakeAsync(() => {
    component.setActiveTab = jasmine.createSpy();

    component.ngOnInit();
    tick();

    expect(component.competition).toBe(competition);
    expect(component.competitionName).toBe(competition.name);
    expect(component.competitionTabs).toBe(competition.competitionTabs);
    expect(competitionsService.storeCategoryId).toHaveBeenCalledWith(component.competition.categoryId.toString());
    expect(participantsService.store).toHaveBeenCalledWith(component.competition.competitionParticipants);
    expect(participantsService.getFlagsList).toHaveBeenCalled();
    expect(user.bonusSuppression).toBeTruthy();

  }));

  xit('#ngOnInit if competition = undefined', fakeAsync(() => {
    competition.competitionParticipants = undefined;
    component.ngOnInit();
    expect(participantsService.store).toHaveBeenCalledWith([]);
  }));


  xit('#ngOnInit error case', fakeAsync(() => {
    component['showError'] = jasmine.createSpy();
    competitionsService.getTabs = jasmine.createSpy().and.returnValue(throwError('error'));
    component.ngOnInit();
    expect(component['showError']).toHaveBeenCalled();
  }));

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsubService.unsubscribe).toHaveBeenCalled();
  });

  it('should call correct methods and set properties', () => {
    const expectedArray = ['liveServe.ws.reconnectSuccess', 'RELOAD_COMPONENTS'];
    component.subscribe();

    expect(component.subscriptionName).toBe('BigCompetitionCtrl');
    expect(pubsubService.subscribe)
      .toHaveBeenCalledWith(component.subscriptionName, jasmine.arrayContaining(expectedArray), jasmine.any(Function));
  });

  it('should call subscribe methods and event not instance of NavigationEnd', () => {
    const expectedArray = ['liveServe.ws.reconnectSuccess', 'RELOAD_COMPONENTS'];
    component.subscribe();

    expect(component.subscriptionName).toBe('BigCompetitionCtrl');
    expect(pubsubService.subscribe)
      .toHaveBeenCalledWith(component.subscriptionName, jasmine.arrayContaining(expectedArray), jasmine.any(Function));
  });

  xit('should call correct methods', () => {
    component.ngOnInit = jasmine.createSpy();
    component.ngOnDestroy = jasmine.createSpy();
    component.showSpinner = jasmine.createSpy();
    component['reloadComponent']();
    expect(liveUpdatesService.reconnect).toHaveBeenCalled();
    expect(component.ngOnInit).toHaveBeenCalled();
    expect(component.ngOnDestroy).toHaveBeenCalled();
    expect(component.showSpinner).toHaveBeenCalled();
  });

  it('should call correct methods and set properties', () => {
    component.setActiveTab();
    expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', route.snapshot);
    expect(competitionsService.findTab).toHaveBeenCalled();
    expect(component.activeTab).toEqual(jasmine.objectContaining({ id: tab.id }));
  });

  it('should call setActiveTab and findTab = undefined', () => {
    competitionsService.findTab = jasmine.createSpy('findTab').and.returnValue(undefined);

    component.setActiveTab();
    expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', route.snapshot);
    expect(competitionsService.findTab).toHaveBeenCalled();
    expect(component.activeTab).toBeUndefined();
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });

  it('should call setActiveTab and getRouteParam is exist', () => {
    routingState.getRouteParam = jasmine.createSpy('getRouteParam').and.returnValue('tabName');

    component.setActiveTab();
    expect(routingState.getRouteParam).toHaveBeenCalledWith('tab', route.snapshot);
    expect(competitionsService.findTab).toHaveBeenCalled();
    expect(component.activeTab).toEqual(jasmine.objectContaining({ id: tab.id }));
    expect(router.navigateByUrl).not.toHaveBeenCalled();
  });

  it('should call getTabsData', () => {
    competition.competitionTabs = [
      {
        uri: '/promotions1'
      }
    ];
    component.getTabsData('competition');
    expect(component.competitionTabs.length).toEqual(1);
  });
});
