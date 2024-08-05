import { tick, fakeAsync } from '@angular/core/testing';
import { DailyRacingService } from '@core/services/racing/dailyRacing/daily-racing.service';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';

describe('DailyRacingService', () => {
  let service;
  let eventFactory;
  let templateService;

  const dailyRacingEvents = [];
  const groupEventsByTypeNameResult = {};

  beforeEach(() => {
    eventFactory = {
      getDailyRacingEvents: jasmine.createSpy().and.returnValue(Promise.resolve(dailyRacingEvents))
    };
    templateService = {
      filterEventsWithoutMarketsAndOutcomes: jasmine.createSpy(),
      groupEventsByTypeName: jasmine.createSpy().and.returnValue(groupEventsByTypeNameResult)
    };
    service = new DailyRacingService(eventFactory, templateService);
  });

  it('getDailyRacingEvents when id was passed', fakeAsync(() => {
    const classId = '38921';
    service.getDailyRacingEvents(classId);
    expect(service['dailyRacingConfig']['classIds']).toEqual(jasmine.arrayContaining([classId]));
    expect(eventFactory.getDailyRacingEvents).toHaveBeenCalledWith(service['dailyRacingConfig']);

    tick();

    expect(templateService.filterEventsWithoutMarketsAndOutcomes).toHaveBeenCalledWith(dailyRacingEvents);
  }));

  it('getDailyRacingEvents when array of ids was passed', fakeAsync(() => {
    const classIds = ['38921'];
    service.getDailyRacingEvents(classIds);
    expect(service['dailyRacingConfig']['classIds']).toBe(classIds);
    expect(eventFactory.getDailyRacingEvents).toHaveBeenCalledWith(service['dailyRacingConfig']);

    tick();

    expect(templateService.filterEventsWithoutMarketsAndOutcomes).toHaveBeenCalledWith(dailyRacingEvents);
  }));

  it('filterBySectionsList when no sectionsList was passed', () => {
    const eventsBySections = { categoryId: '768372' } as ITypeSegment;
    const result = service.filterBySectionsList(eventsBySections, null);
    expect(result).toBe(eventsBySections);
  });

  it('filterBySectionsList when sectionsList was passed', () => {
    const eventsBySections = { categoryId: '768372', className: 'name' } as ITypeSegment;
    const sectionsList = ['categoryId'];
    const result = service.filterBySectionsList(eventsBySections, sectionsList);
    expect(result).toEqual(jasmine.objectContaining({ categoryId: '768372' }));
    expect(result.className).toBeUndefined();
  });

  describe('addEvents', () => {
    it('selectedTab is not allowed', () => {
      const publicArguments = { selectedTab: 'tomorrow' };
      service.getDailyRacingEvents = jasmine.createSpy();
      service.filterBySectionsList = jasmine.createSpy();
      service.addEvents(publicArguments).then(result => {
        expect(result).toBe(publicArguments);
      });
      expect(service.getDailyRacingEvents).not.toHaveBeenCalled();
      expect(service.filterBySectionsList).not.toHaveBeenCalled();
    });

    it('selectedTab is allowed, no groupedRacing', () => {
      const publicArguments = {
        selectedTab: 'today',
        modules: {
          dailyRacing: {
            classIds: ['']
          }
        },
        events: []
      };
      const event = {};
      service.getDailyRacingEvents = jasmine.createSpy().and.returnValue(Promise.resolve([event]));
      service.filterBySectionsList = jasmine.createSpy();
      service.addEvents(publicArguments).then(() => {
        expect(publicArguments.events[0]).toBe(event);
      });
      expect(service.getDailyRacingEvents).toHaveBeenCalledWith(publicArguments.modules.dailyRacing.classIds);
      expect(service.filterBySectionsList).not.toHaveBeenCalled();
    });

    it('selectedTab is allowed, groupedRacing is in publicArguments', () => {
      const publicArguments = {
        selectedTab: 'today',
        modules: {
          dailyRacing: {
            classIds: [''],
            typeNames: [''],
            eventsBySections: []
          },
        },
        events: [],
        groupedRacing: {}
      };
      const eventsBySection = [
        {
          isStarted: true,
          rawIsOffCode: 'N'
        },
        {
          isStarted: false,
          rawIsOffCode: 'Y'
        },
        {
          isStarted: false,
          rawIsOffCode: 'N'
        }
      ];
      const events = [];
      service.getDailyRacingEvents = jasmine.createSpy().and.returnValue(Promise.resolve(events));
      service.filterBySectionsList = jasmine.createSpy().and.returnValue(eventsBySection);
      service.addEvents(publicArguments).then(() => {
        expect(templateService.groupEventsByTypeName).toHaveBeenCalledWith(events);
        expect(service.filterBySectionsList)
          .toHaveBeenCalledWith(groupEventsByTypeNameResult, publicArguments.modules.dailyRacing.typeNames);
          expect(publicArguments.modules.dailyRacing.eventsBySections).toBeNull();
      });
      expect(service.getDailyRacingEvents).toHaveBeenCalledWith(publicArguments.modules.dailyRacing.classIds);
    });

    it('selectedTab is allowed, eventsBySections should be null', () => {
      const publicArguments = {
        selectedTab: 'today',
        modules: {
          dailyRacing: {
            classIds: [''],
            typeNames: [''],
            eventsBySections: []
          },
        },
        events: [],
        groupedRacing: {}
      };
      const eventsBySection = [
        {
          isStarted: true,
          rawIsOffCode: 'N'
        },
        {
          isStarted: false,
          rawIsOffCode: 'Y'
        }
      ];
      const events = [];
      service.getDailyRacingEvents = jasmine.createSpy().and.returnValue(Promise.resolve(events));
      service.filterBySectionsList = jasmine.createSpy().and.returnValue(eventsBySection);
      service.addEvents(publicArguments).then(() => {
        expect(templateService.groupEventsByTypeName).toHaveBeenCalledWith(events);
        expect(service.filterBySectionsList)
          .toHaveBeenCalledWith(groupEventsByTypeNameResult, publicArguments.modules.dailyRacing.typeNames);
        expect(publicArguments.modules.dailyRacing.eventsBySections).toBeNull();
      });
      expect(service.getDailyRacingEvents).toHaveBeenCalledWith(publicArguments.modules.dailyRacing.classIds);
    });
  });
});
