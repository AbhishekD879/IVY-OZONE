import { BigCompetitionsSpecialsService } from '@app/bigCompetitions/services/bigCompetitionsSpecials/big-competitions-specials-service';

describe('BigCompetitionsSpecialsService', () => {
  let service;
  let gamingService;
  let templateService;
  let srvUtil;
  let filtersService;

  beforeEach(() => {
    gamingService = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection').and.returnValue([{}])
    };

    templateService = {
      getSportViewTypes: jasmine.createSpy('getSportViewTypes').and.returnValue('categoryName')
    };

    srvUtil = {
      filterEventsWithPrices: jasmine.createSpy('filterEventsWithPrices').and.returnValue([{ categoryName: 'category Name'}])
    };

    filtersService = {
      orderBy: jasmine.createSpy('orderBy').and.returnValue([{}]),
      clearSportClassName: jasmine.createSpy('clearSportClassName').and.returnValue('className')
    };

    service = new BigCompetitionsSpecialsService(gamingService, templateService, srvUtil, filtersService);
  });

  describe('@getRemovedEventLevels', () => {
    let eventsBySections,
      actualResult;

    beforeEach(() => {
      eventsBySections = [
        {
          events: [{ id: 1 }],
          groupedByDate: [{ events: [{ id: 1 }] }]
        }
      ];
    });

    it('should search event in 2 levels arrays by event id and return object with found levels indexes', () => {
      actualResult = service['getRemovedEventLevels'](eventsBySections, 1);

      expect(actualResult).toEqual({ section: 0, event: 0, groupedByDateKey: 0, groupedByDateEvent: 0 });
    });

    it('should search event by event id and return object', () => {
      actualResult = service['getRemovedEventLevels'](eventsBySections, 2);

      expect(actualResult).toEqual({ section: null, event: null, groupedByDateKey: null, groupedByDateEvent: null });
    });

    it('should search event in 2 levels arrays by event id and return object', () => {
      eventsBySections[0].groupedByDate[0].events[0].id = 2;

      actualResult = service['getRemovedEventLevels'](eventsBySections, 1);

      expect(actualResult).toEqual({ section: 0, event: 0, groupedByDateKey: null, groupedByDateEvent: null });
    });
  });

  describe('@removeEmptyGropedByDateSection', () => {
    let eventsBySections,
      levels;

    beforeEach(() => {
      eventsBySections = [{
        events: [{ id: 1 }],
        groupedByDate: [{ events: [] }]
      }];
      levels = { section: 0, event: 0, groupedByDateKey: 0, groupedByDateEvent: 0 };
    });

    it('should remove grouped by date section', () => {
      service['removeEmptyGropedByDateSection'](eventsBySections, levels);

      expect(eventsBySections[0].groupedByDate.length).toEqual(0);
    });

    it('should not remove grouped by date section', () => {
      eventsBySections[0].groupedByDate[0].events = [{}];

      service['removeEmptyGropedByDateSection'](eventsBySections, levels);

      expect(eventsBySections[0].groupedByDate.length).toEqual(1);
    });
  });

  describe('@removeEmptySection', () => {
    let eventsBySections,
      deletedEventIndexes;

    beforeEach(() => {
      eventsBySections = [{
        events: [{}]
      }];
      deletedEventIndexes = {
        section: 0
      };
    });

    it('should not remove section from array by provided level(index)', () => {
      service['removeEmptySection'](eventsBySections, deletedEventIndexes);

      expect(eventsBySections.length).toEqual(1);
    });

    it('should remove empty section from array by provided level(index)', () => {
      eventsBySections[0].events = [];

      service['removeEmptySection'](eventsBySections, deletedEventIndexes);

      expect(eventsBySections.length).toEqual(0);
    });
  });

  describe('@removeEventFromGropedByDate', () => {
    it('should remove event from groped by date', () => {
      const eventsBySections = [{
        groupedByDate: [{
          events: [{}]
        }]
      }],
      indexes = {
        section: 0,
        groupedByDateKey: 0,
        groupedByDateEvent: 0
      };

      service['removeEventFromGropedByDate'](eventsBySections, indexes);

      expect(eventsBySections[0].groupedByDate[0].events.length).toEqual(0);
    });
  });

  describe('@removeEventFromLevel', () => {
    it('should removes event from array by provided level(index)', () => {
      const eventsBySections = [{
        events: [{}, {}]
      }],
      deletedEventIndexes = {
        section: 0,
        event: 0
      };

      service['removeEventFromLevel'](eventsBySections, deletedEventIndexes);

      expect(eventsBySections[0].events.length).toEqual(1);
    });
  });

  describe('@selectionsCount', () => {
    let keysArray,
      groupedByDate,
      result;

    beforeEach(() => {
      keysArray = ['0'];
      groupedByDate = [{
        events: [{
          markets: [{
            outcomes: []
          }]
        }]
      }];
    });

    it('should return 0', () => {
      result = service['selectionsCount'](keysArray, groupedByDate);

      expect(result).toEqual(0);
    });

    it('should returns selections count in GroupedByDate structure by keys(dates) list', () => {
      groupedByDate[0].events[0].markets[0].outcomes = [{}];

      result = service['selectionsCount'](keysArray, groupedByDate);

      expect(result).toEqual(1);
    });
  });

  describe('@eGbDSelectionsCount', () => {
    it('should events grouped by date', () => {
      const groupedByDate = [{}, {}];
      service.selectionsCount = jasmine.createSpy('selectionsCount');

      service['eGbDSelectionsCount'](groupedByDate, 1);

      expect(service.selectionsCount).toHaveBeenCalledWith(['0', '1'], groupedByDate);
    });
  });

  describe('@sectionTitle', () => {
    let sportsViewTypes,
      section,
      result;

    beforeEach(() => {
      sportsViewTypes = {
        className: 'className'
      };
      section = {
        className: 'className',
        categoryName: 'categoryName',
        typeName: 'typeName'
      };
    });

    it('should return forms sections title for section(className)', () => {
      result = service['sectionTitle'](sportsViewTypes, section);

      expect(filtersService.clearSportClassName).toHaveBeenCalledWith(sportsViewTypes.className, section.categoryName);
      expect(result).toEqual('className - typeName');
    });

    it('should return forms sections title for section(categoryName)', () => {
      sportsViewTypes.className = '';
      result = service['sectionTitle'](sportsViewTypes, section);

      expect(filtersService.clearSportClassName).not.toHaveBeenCalled();
      expect(result).toEqual('categoryName - typeName');
    });
  });

  describe('@removeEvent', () => {
    let eventsBySections,
      deletedEventIndexes,
      result;

    beforeEach(() => {
      deletedEventIndexes = { section: 0 };
      service['getRemovedEventLevels'] = jasmine.createSpy('getRemovedEventLevels').and.returnValue(deletedEventIndexes);
      service['removeEventFromLevel'] = jasmine.createSpy('removeEventFromLevel');
      service['removeEventFromGropedByDate'] = jasmine.createSpy('removeEventFromGropedByDate');
      service['removeEmptyGropedByDateSection'] = jasmine.createSpy('removeEmptyGropedByDateSection');
      service['removeEmptySection'] = jasmine.createSpy('removeEmptySection');
      eventsBySections = [{}];
    });

    it('should remove event and section', () => {
      result = service.removeEvent(eventsBySections, 0);

      expect(service['removeEventFromLevel']).toHaveBeenCalledWith(eventsBySections, deletedEventIndexes);
      expect(service['removeEventFromGropedByDate']).toHaveBeenCalledWith(eventsBySections, deletedEventIndexes);
      expect(service['removeEventFromGropedByDate']).toHaveBeenCalledWith(eventsBySections, deletedEventIndexes);
      expect(service['removeEventFromGropedByDate']).toHaveBeenCalledWith(eventsBySections, deletedEventIndexes);
    });

    it('should not remove event and section', () => {
      service['getRemovedEventLevels'] = jasmine.createSpy('getRemovedEventLevels').and.returnValue({ section: null });
      result = service.removeEvent(eventsBySections, 0);

      expect(service['removeEventFromLevel']).not.toHaveBeenCalled();
      expect(service['removeEventFromGropedByDate']).not.toHaveBeenCalled();
      expect(service['removeEventFromGropedByDate']).not.toHaveBeenCalled();
      expect(service['removeEventFromGropedByDate']).not.toHaveBeenCalled();
    });

    afterEach(() => {
      expect(service['getRemovedEventLevels']).toHaveBeenCalledWith(eventsBySections, '0');
      expect(result).toEqual(eventsBySections);
    });
  });

  describe('@isShowButtonForGroupedByDateEnabled', () => {
    let result,
      groupedByDate;

    beforeEach(() => {
      groupedByDate = [{}];
      service['eGbDSelectionsCount'] = jasmine.createSpy('eGbDSelectionsCount').and.returnValue(2);
    });

    it('all buttons should be shown for grouped by date selections section', () => {
      result = service.isShowButtonForGroupedByDateEnabled(groupedByDate, 1);

      expect(service['eGbDSelectionsCount']).toHaveBeenCalledWith(groupedByDate, 1);
      expect(result).toEqual(true);
    });

    it('all buttons should not be shown for grouped by date selections section', () => {
      result = service.isShowButtonForGroupedByDateEnabled(groupedByDate, 0);

      expect(service['eGbDSelectionsCount']).not.toHaveBeenCalled();
      expect(result).toEqual(0);
    });
  });

  describe('@getEventsBySections', () => {
    let eventsArray;

    beforeEach(() => {
      eventsArray = [{}];
      service['sectionTitle'] = jasmine.createSpy('sectionTitle');
    });

    it('should get events by sections', () => {
      service.getEventsBySections(eventsArray);

      expect(srvUtil.filterEventsWithPrices).toHaveBeenCalledWith(eventsArray);
      expect(gamingService.arrangeEventsBySection).toHaveBeenCalledWith([{ categoryName: 'category Name' }], true);
      expect(filtersService.orderBy).toHaveBeenCalledWith([{}], ['classDisplayOrder', 'typeDisplayOrder']);
      expect(templateService.getSportViewTypes).toHaveBeenCalledWith('categoryname');
      expect(service['sectionTitle']).toHaveBeenCalled();
    });

    it('should return []', () => {
      eventsArray = [];
      const result = service.getEventsBySections(eventsArray);

      expect(srvUtil.filterEventsWithPrices).not.toHaveBeenCalled();
      expect(gamingService.arrangeEventsBySection).not.toHaveBeenCalled();
      expect(filtersService.orderBy).not.toHaveBeenCalled();
      expect(templateService.getSportViewTypes).not.toHaveBeenCalled();
      expect(service['sectionTitle']).not.toHaveBeenCalled();
      expect(result).toEqual([]);
    });
  });
});
