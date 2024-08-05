import {
  CompetitionSpecialsOverviewComponent
} from '@app/bigCompetitions/components/competitionSpecialsOverview/competition-specials-overview.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CompetitionSpecialsOverviewComponent', () => {

  let component: CompetitionSpecialsOverviewComponent;

  let bigCompetitionsSpecialsService;
  let pubSubService;

  let moduleConfig;
  let events;

  beforeEach(() => {
    moduleConfig = {
      events: [],
      specialModuleData: {
        linkUrl: 'specialModuleData.url'
      },
      linkUrl: 'moduleConfig.linkUrl'
    };
    events = [];

    bigCompetitionsSpecialsService = {
      getEventsBySections: jasmine.createSpy().and.returnValue(events),
      removeEvent: jasmine.createSpy().and.returnValue([])
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    component = new CompetitionSpecialsOverviewComponent(bigCompetitionsSpecialsService, pubSubService);
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.showLimit).toBe(10);
    expect(component.inner).toBeTruthy();
    expect(component.openMarketTabs.length).toBe(0);
  });

  describe('#ngOnInit', () => {
    it('should initialize fields', () => {
      component.ngOnInit();
      expect(component.initialData).toEqual(component.moduleConfig.events);
      expect(component.viewAllUrl).toBe(component.moduleConfig.specialModuleData.linkUrl);
      expect(component.eventsBySections).toBe(events);
      expect(bigCompetitionsSpecialsService.getEventsBySections).toHaveBeenCalledWith(component.initialData);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        `CompetitionSpecialsOverviewComponent${component.moduleConfig.id}`,
        pubSubService.API.DELETE_EVENT_FROM_CACHE,
        jasmine.any(Function)
      );
    });

    it('should not define viewAllUrl if no specialModuleData and linkUrl', () => {
      component.viewAllUrl = undefined;
      component.moduleConfig = {
        events: [],
        specialModuleData: undefined,
        linkUrl: undefined
      };
      component.ngOnInit();

      expect(component.viewAllUrl).toBeUndefined();
    });

    it('should define viewAllUrl as moduleConfig.linkUrl', () => {
      component.viewAllUrl = undefined;
      component.moduleConfig = {
        events: [],
        specialModuleData: undefined,
        linkUrl: 'moduleConfig.linkUrl'
      };
      component.ngOnInit();

      expect(component.viewAllUrl).toBe(component.moduleConfig.linkUrl);
    });
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe)
      .toHaveBeenCalledWith(`CompetitionSpecialsOverviewComponent${component.moduleConfig.id}`);
  });
});
