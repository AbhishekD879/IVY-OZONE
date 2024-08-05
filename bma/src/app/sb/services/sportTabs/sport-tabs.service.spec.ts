import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';

describe('SportTabsService', () => {
  let service;
  let templateService;
  let filtersService;
  let competitionsMock;
  let viewTypes;
  let sportInstance;

  beforeEach(() => {
    competitionsMock = [
      {
        id: 'id1', typeDisplayOrder: -2, classDisplayOrder: -3, categoryName: 'categoryName', events: [
          { id: '1', name: 'abc', startTime: 500, displayOrder: -4 },
          { id: '2', name: 'bc', startTime: 700, displayOrder: -1}
        ], typeName: 'typeName1'
      },
      {
        id: 'id2', typeDisplayOrder: - 1, classDisplayOrder: -7, categoryName: 'categoryName2', events: [
          { id: '4', name: 'nbc', startTime: 800, displayOrder: -3 },
          { id: '3', name: 'zbc', startTime: 700, displayOrder: -7}
        ], typeName: 'typeName'
      }
    ];
    viewTypes = { className: false, outrights: false };
    templateService = {
      getSportViewTypes: jasmine.createSpy('getSportViewTypes').and.returnValue(viewTypes)
    };
    filtersService = {
      clearSportClassName: jasmine.createSpy('clearSportClassName').and.returnValue('clearSportClassName'),
      orderBy: jasmine.createSpy('orderBy').and.returnValue(competitionsMock)
    };
    sportInstance = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection').and.returnValue(competitionsMock)
    };

    service = new SportTabsService(templateService, filtersService);
  });

  describe('@deleteEvent', () => {
    it('should delete event from Events data and grouped data', () => {
      const eventMock = { id: 111 };
      const eventMockTwo = { id: 222 };

      const sections = [
        {
          events: [
            eventMock,
            eventMockTwo
          ],
          groupedByDate: [
            {
              title: 'today',
              events: [
                eventMock,
                eventMockTwo
              ]
            }
          ]
        }
      ];
      service.deleteEvent('111', sections);

      expect(sections[0].events.length).toBe(1);
      expect(sections[0].groupedByDate.length).toBe(1);
    });

    it('should delete event ad group from Sections data', () => {
      const eventMock = { id: 111 };
      const eventMockTwo = { id: 222 };

      const sections = [
        {
          events: [
            eventMock,
            eventMockTwo
          ],
          groupedByDate: [
            {
              title: 'today',
              events: [
                eventMock
              ]
            },
            {
              title: 'tomorrow',
              events: [
                eventMockTwo
              ]
            }
          ]
        }
      ];
      service.deleteEvent('111', sections);

      expect(sections[0].events.length).toBe(1);
      expect(sections[0].groupedByDate.length).toBe(1);
    });

    it('should not delete event', () => {
      const eventMock = { id: 111 };

      const sections = [
        {
          events: [
            eventMock
          ],
          groupedByDate: [
            {
              title: 'today',
              events: [
                eventMock
              ]
            }
          ]
        }
      ];
      service.deleteEvent('3333', sections);

      expect(sections.length).toBe(1);
    });

    it('should not delete group when no grouped data', () => {
      const eventMock = { id: 111 };
      const eventMockTwo = { id: 222 };

      const sections = [
        {
          events: [
            eventMock,
            eventMockTwo
          ]
        }
      ];
      service.deleteEvent('111', sections);

      expect(sections[0].events.length).toBe(1);
    });

    it('should do nothing when no sections', () => {
      const sections = [];
      service.deleteEvent('3333', sections);

      expect(sections.length).toBe(0);
    });

    it('should delete event even if it is single in the list', () => {
      const sections = [{ events: [{ id: 111 }] }];

      service.deleteEvent('111', sections);

      expect(sections.length).toBe(0);
    });

    it('should do nothing if sections data is corrupted', () => {
      const sections = [undefined];

      service.deleteEvent('111', sections);

      expect(sections.length).toBe(1);
    });
  });

  describe('@eventsBySections', () => {
    it('should sort competitions and events within competition', () => {
      const res = service.eventsBySections(competitionsMock, sportInstance);

      expect(sportInstance.arrangeEventsBySection).toHaveBeenCalled();
      expect(res[0].sectionTitle).toBe('categoryName - typeName1');
      expect(res[1].sectionTitle).toBe('categoryName2 - typeName');
      expect(res[0].id).toBe('id1');
      expect(res[0].events[0].id).toBe('1');
      expect(res[1].events[0].id).toBe('3');
    });

    it('should set sectionTitle using clearSportClassName', () => {
      viewTypes.className = 'className';

      service.eventsBySections(competitionsMock, sportInstance);

      expect(filtersService.clearSportClassName).toHaveBeenCalled();
      expect(filtersService.orderBy).toHaveBeenCalledWith(competitionsMock, ['typeDisplayOrder', 'classDisplayOrder', 'sectionTitle']);
    });

  });

  describe('@sortSportEventsData', () => {
    const golfEvents = [
      { id: '1', name: 'abc', startTime: 500, displayOrder: -4, categoryId: '18', eventSortCode: 'MTCH' },
      { id: '2', name: 'bc', startTime: 700, displayOrder: -1, categoryId: '18', eventSortCode: 'TNMT'}
    ];

    const otherEvents = [
      { id: '1', name: 'abc', startTime: 500, displayOrder: -4, eventSortCode: 'MTCH' },
      { id: '2', name: 'bc', startTime: 700, displayOrder: -1, eventSortCode: 'TNMT'}
    ];

    it('should sort events for golf as outrights followed by matches', () => {

      const res = service.sortSportEventsData(golfEvents);

      expect(res[0].id).toBe('2');
      expect(res[1].id).toBe('1');
    });

    it('should sort events for other sports as matches followed by outrights', () => {

      const res = service.sortSportEventsData(otherEvents);

      expect(res[0].id).toBe('1');
      expect(res[1].id).toBe('2');
    });

  });
});
