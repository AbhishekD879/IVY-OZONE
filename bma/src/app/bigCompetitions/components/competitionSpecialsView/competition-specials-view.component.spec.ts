import {
  CompetitionSpecialsViewComponent
} from '@app/bigCompetitions/components/competitionSpecialsView/competition-specials-view.component';
import { IGroupedByDateItem, IGroupedByDateObj, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

describe('CompetitionSpecialsViewComponent', () => {

  let component: CompetitionSpecialsViewComponent;

  let bigCompetitionsSpecialsService;
  let filtersService;

  const viewAllUrl = 'some/view/all/url';

  beforeEach(() => {
    bigCompetitionsSpecialsService = {
      isShowButtonForGroupedByDateEnabled: jasmine.createSpy().and.returnValue(true)
    };
    filtersService = {
      filterLink: jasmine.createSpy().and.returnValue('viewAllUrl')
    };

    component = new CompetitionSpecialsViewComponent(bigCompetitionsSpecialsService, filtersService);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    const groupedByDateObj = {};
    const eventsBySections = [
      {
        categoryId: '',
        typeName: '',
        groupedByDate: {}
      },
      {
        categoryId: '',
        typeName: 'Enhanced Multiples',
        groupedByDate: groupedByDateObj
      }
    ] as ITypeSegment[];
    const groupedByDate = {
      key: {
        deactivated: false,
        startTime: 0,
        events: [],
        title: '',
        marketsAvailability: null
      }
    } as IGroupedByDateObj;
    const defaultEvents = [];
    component.eventsBySections = defaultEvents;
    component.openMarketTabs = [];
    component.showLimit = 0;
    component.orderedSections = jasmine.createSpy().and.returnValue(eventsBySections);
    component.groupedEvents = jasmine.createSpy().and.returnValue(groupedByDate);
    component.viewAllUrl = viewAllUrl;
    component.ngOnInit();

    expect(component.openMarketTabs[0]).toBeTruthy();
    expect(component['showAllGroupedByDate']).toBeTruthy();
    expect(component.eventsBySections).toBe(eventsBySections);
    expect(component['orderedSections']).toHaveBeenCalledWith(defaultEvents);
    expect(component.eventsBySections[1].groupedByDate).toBe(groupedByDate);
    expect(component['groupedEvents']).toHaveBeenCalledWith(groupedByDateObj);
    expect(filtersService.filterLink).toHaveBeenCalledWith(viewAllUrl);
    expect(component.viewAllUrl).toEqual('viewAllUrl');
  });

  it('should return true', () => {
    const eventsBySection = {
      categoryId: '',
      typeName: '',
      events: [{}, {}]
    } as ITypeSegment;
    component.showLimit = 1;
    expect(component.isShowButtonEnabled(eventsBySection)).toBeTruthy();
  });

  it('should return false', () => {
    const eventsBySection = {
      categoryId: '',
      typeName: 'Enhanced Multiples',
      events: [{}, {}]
    } as ITypeSegment;
    component.showLimit = 1;
    expect(component.isShowButtonEnabled(eventsBySection)).toBeFalsy();
  });

  it('should return false', () => {
    const eventsBySection = {
      categoryId: '',
      typeName: '',
      events: [{}, {}]
    } as ITypeSegment;
    component.showLimit = 0;
    expect(component.isShowButtonEnabled(eventsBySection)).toBeFalsy();
  });

  it('should return false', () => {
    const eventsBySection = {
      categoryId: '',
      typeName: 'Enhanced Multiples',
      events: []
    } as ITypeSegment;
    component.showLimit = 1;
    expect(component.isShowButtonEnabled(eventsBySection)).toBeFalsy();
  });

  it('should call correct method and return true', () => {
    component.showLimit = 5;
    const groupedByDate = [];
    expect(component.isShowButtonForGroupedByDateEnabled(groupedByDate)).toBeTruthy();
    expect(bigCompetitionsSpecialsService.isShowButtonForGroupedByDateEnabled)
      .toHaveBeenCalledWith(groupedByDate, component.showLimit);
  });

  it('should return passed number', () => {
    const index = 42;
    expect(component.trackByIndex(index)).toBe(index);
  });

  it('should return correct result', () => {
    const event = { id: 5 } as ISportEvent;
    const index = 1;
    expect(component.trackById(index, event)).toBe('15');
  });

  it('should return correct result', () => {
    const eventsBySection = [
      { typeDisplayOrder: 5 },
      { typeDisplayOrder: 3 },
      { typeDisplayOrder: 9 },
      { typeDisplayOrder: 1 }
    ] as ITypeSegment[];
    const result = component.orderedSections(eventsBySection);
    expect(result[0].typeDisplayOrder).toBe(1);
    expect(result[1].typeDisplayOrder).toBe(3);
    expect(result[2].typeDisplayOrder).toBe(5);
    expect(result[3].typeDisplayOrder).toBe(9);
  });

  it('should return correct result', () => {
    const eventsBySection = {
      events: [{}, {}, {}]
    } as ITypeSegment;
    expect(component.limitTo(eventsBySection).length).toBe(3);
  });

  it('should return correct result', () => {
    const eventsBySection = {
      events: [{}, {}, {}]
    } as ITypeSegment;
    component.showLimit = 2;
    expect(component.limitTo(eventsBySection).length).toBe(2);
  });

  it('should set correct properties', () => {
    const events = [
      {
        markets: [
          {
            outcomes: [{}, {}, {}] as IOutcome[]
          }
        ]
      }
    ] as ISportEvent[];
    const groupedEvents = {
      key: {
        deactivated: false,
        startTime: 0,
        title: '',
        marketsAvailability: null,
        events,
      }
    } as IGroupedByDateObj;
    component.groupedLimit = 5;
    component.groupedEvents(groupedEvents);
    expect(component.groupedLimit).toBe(2);
    expect(groupedEvents.key.events[0].groupedLimit).toBe(3);
  });

  it('should set correct properties', () => {
    const events = [
      {
        markets: [
          {
            outcomes: [{}, {}, {}] as IOutcome[]
          }
        ]
      }
    ] as ISportEvent[];
    const groupedEvents = {
      key: {
        deactivated: false,
        startTime: 0,
        title: '',
        marketsAvailability: null,
        events,
      }
    } as IGroupedByDateObj;
    component.groupedLimit = 2;
    component.groupedEvents(groupedEvents);
    expect(component.groupedLimit).toBe(0);
    expect(groupedEvents.key.events[0].groupedLimit).toBe(2);
  });

  it('should return true', () => {
    const grouped = {
      events: [
        { groupedLimit: 5 }
      ]
    } as IGroupedByDateItem;
    component.showAllGroupedByDate = false;
    expect(component.showGroupedHeader(grouped)).toBeTruthy();
  });

  it('should return true', () => {
    const grouped = {
      events: [
        { groupedLimit: 0 }
      ]
    } as IGroupedByDateItem;
    component.showAllGroupedByDate = true;
    expect(component.showGroupedHeader(grouped)).toBeTruthy();
  });

  it('should return false', () => {
    const grouped = {
      events: [
        { groupedLimit: 0 }
      ]
    } as IGroupedByDateItem;
    component.showAllGroupedByDate = false;
    expect(component.showGroupedHeader(grouped)).toBeFalsy();
  });
});
