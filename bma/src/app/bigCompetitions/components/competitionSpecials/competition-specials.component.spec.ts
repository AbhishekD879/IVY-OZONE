import {
  CompetitionSpecialsComponent
} from '@app/bigCompetitions/components/competitionSpecials/competition-specials.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CompetitionSpecialsComponent', () => {

  let component: CompetitionSpecialsComponent;

  let bigCompetitionsSpecialsService;
  let pubSubService;

  let moduleConfig;
  let eventsBySections;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      events: []
    };
    eventsBySections = [];

    bigCompetitionsSpecialsService = {
      getEventsBySections: jasmine.createSpy().and.returnValue(eventsBySections),
      removeEvent: jasmine.createSpy().and.returnValue([])
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    component = new CompetitionSpecialsComponent(bigCompetitionsSpecialsService, pubSubService);
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.showLimit).toBe(10);
    expect(component.openMarketTabs.length).toBe(0);
    expect(component.eventsBySections.length).toBe(0);
  });

  it('#ngOnInit', () => {
    component.ngOnInit();
    expect(component.initialData).toEqual(component.moduleConfig.events);
    expect(component.eventsBySections).toBe(eventsBySections);
    expect(bigCompetitionsSpecialsService.getEventsBySections).toHaveBeenCalledWith(component.initialData);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      `CompetitionSpecialsComponent${component.moduleConfig.id}`,
      pubSubService.API.DELETE_EVENT_FROM_CACHE,
      jasmine.any(Function)
    );
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe)
      .toHaveBeenCalledWith(`CompetitionSpecialsComponent${component.moduleConfig.id}`);
  });
});
