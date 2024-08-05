import {
  CompetitionNextEventsComponent
} from '@app/bigCompetitions/components/competitionNextEvents/competition-next-events.component';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('CompetitionNextEventsComponent', () => {

  let component: CompetitionNextEventsComponent;

  let pubSubService;
  let bigCompetitionsService;
  let bigCompetitionLiveUpdatesService;
  let sportsConfigService;
  let moduleConfig;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      name: 'name',
      type: '',
      maxDisplay: 10,
      viewType: 'inplay',
      aemPageName: '',
      isExpanded: false,
      markets: [],
      specialModuleData: {
        typeIds: [],
        eventIds: [],
        linkUrl: ''
      },
      groupModuleData: {
        sportId: 12,
        areaId: 32,
        competitionId: 34,
        seasonId: 43,
        numberQualifiers: 11,
        details: null,
        data: [
          {
            competitionId: 32,
            seasonId: 32443,
            tableId: 43,
            tableName: '',
            teams: [],
            ssEvents: []
          }
        ]
      },
      events: [
        {
          name: 'name',
          displayOrder: 0,
          startTime: '',
          markets: [
            { outcomes: [{}] }
          ]
        }
      ],
      errors: [],
      results: []
    };

    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    bigCompetitionsService = {
      activeCategoryId: 'activeCategoryId',
      addOutcomeMeaningMinorCode: jasmine.createSpy('addOutcomeMeaningMinorCode')
    };

    bigCompetitionLiveUpdatesService = {
      addOutcomeMeaningMinorCode: jasmine.createSpy('addOutcomeMeaningMinorCode'),
      removeEventEntity: jasmine.createSpy('removeEventEntity'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribeBigCompetitionLiveUpdatesService')
    };
    sportsConfigService = {
      getSportByCategoryId: jasmine.createSpy('getSportByCategoryId').and.returnValue(of(100))
    };

    component = new CompetitionNextEventsComponent(
      pubSubService,
      bigCompetitionsService,
      bigCompetitionLiveUpdatesService,
      sportsConfigService
    );
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    const view = {
      id: 'competitionModule-id',
      type: 'list'
    };
    component['subscribeForLiveUpdates'] = jasmine.createSpy('subscribeForLiveUpdates');
    pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback(view));
    component.ngOnInit();
    expect(component.categoryId).toBe(bigCompetitionsService.activeCategoryId);
    expect(bigCompetitionsService.addOutcomeMeaningMinorCode).toHaveBeenCalledWith(component.events);
    expect(component['subscribeForLiveUpdates']).toHaveBeenCalled();
    expect(sportsConfigService.getSportByCategoryId).toHaveBeenCalled();
  });

  it('#ngOnDestroy', () => {
    component.moduleId = 'moduleId';
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component.moduleId);
  });

  it('should call correct methods and set properties', () => {
    component['subscribeOnExpand'] = jasmine.createSpy('subscribeOnExpand');
    component.isExpanded = false;
    component.accordionHandler();
    expect(component.isExpanded).toBeTruthy();
    expect(component['subscribeOnExpand']).toHaveBeenCalled();
  });

  it('should call correct methods and set properties', () => {
    component['unsubscribeOnCollapse'] = jasmine.createSpy('unsubscribeOnCollapse');
    component.isExpanded = true;
    component.accordionHandler();
    expect(component.isExpanded).toBeFalsy();
    expect(component['unsubscribeOnCollapse']).toHaveBeenCalledWith(component.moduleConfig.events);
  });

  it('should call correct methods', () => {
    component.moduleId = 'moduleId';
    component['subscribeForLiveUpdates']();
    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith(component.moduleId, pubSubService.API.MOVE_EVENT_TO_INPLAY, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.moduleId, pubSubService.API.LIVE_SERVE_MS_UPDATE, jasmine.any(Function));
  });

  describe('removeEventEntity', () => {
    it('should call correct methods', () => {
      component.events = [
        {  id: 1 },
        {  id: 2 },
        {  id: 3 }
      ] as IBigCompetitionSportEvent[];
      component['unsubscribeOnCollapse'] = jasmine.createSpy('unsubscribeOnCollapse');
      const event = { id: '2' } as any;
      component['removeEventEntity'](event);
      expect(component.events.length).toBe(2);
      expect(component.events[0]).toEqual(jasmine.objectContaining({ id: 1 }));
      expect(component.events[1]).toEqual(jasmine.objectContaining({ id: 3 }));
      expect(component['unsubscribeOnCollapse']).toHaveBeenCalledWith(jasmine.arrayContaining([event]));
    });

    it('should not remove event from list if update not related to stored evetns', () => {
      const event = { id: '4' } as any;

      component.events = [
        {  id: 1 },
        {  id: 2 },
        {  id: 3 }
      ] as IBigCompetitionSportEvent[];

      component['removeEventEntity'](event);

      expect(component.events.length).toBe(3);
    });
  });

  it('should call correct method', () => {
    component['subscribeOnExpand']();
    expect(bigCompetitionLiveUpdatesService.subscribe).toHaveBeenCalledWith(component.moduleConfig.events);
  });

  it('should call correct methods', () => {
    const events = [];
    component['unsubscribeOnCollapse'](events);
    expect(bigCompetitionLiveUpdatesService.unsubscribe).toHaveBeenCalledWith(events);
  });

  describe('#getComparatorByProperty', () => {
    it('property values for both items are equal', () => {
      const a = { value: 3 };
      const b = { value: 3 };
      const comparator = component['getComparatorByProperty']('value');
      const result = comparator(a, b);
      expect(result).toBe(0);
    });

    it('property values of the first item is bigger', () => {
      const a = { value: 4 };
      const b = { value: 2 };
      const comparator = component['getComparatorByProperty']('value');
      const result = comparator(a, b);
      expect(result).toBe(1);
    });

    it('property values of the second item is bigger', () => {
      const a = { value: 1 };
      const b = { value: 5 };
      const comparator = component['getComparatorByProperty']('value');
      const result = comparator(a, b);
      expect(result).toBe(-1);
    });
  });
});
