import { GermanSupportInPlayService } from './german-support-inplay.service';

describe('GermanSupportInPlayService', () => {
  let service: GermanSupportInPlayService;
  let germanSupportService;
  let structureData, ribbonDataItems;

  beforeEach(() => {
    germanSupportService = {
      isGermanUser: jasmine.createSpy().and.returnValue(true),
      restrictedSportsCategoriesIds: ['19', '21', '161'] // 19 - GH, 21 - HR, 161 - INT TOTE
    };

    service = new GermanSupportInPlayService(germanSupportService);
    structureData = {
      livenow: {
        eventCount: 10,
        eventsBySports: [
          { categoryId: 19, eventCount: 1, eventsIds: [1] },
          { categoryId: 21, eventCount: 2, eventsIds: [2, 3] },
          { categoryId: 16, eventCount: 3, eventsIds: [4, 5, 6] },
          { categoryId: 161, eventCount: 4, eventsIds: [7, 8, 9, 10] }
        ],
        eventsIds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      },
      upcoming: {
        eventCount: 3,
        eventsBySports: [{ categoryId: 16, eventCount: 3, eventsIds: [11, 12, 13] }],
        eventsIds: [11, 12, 13]
      }
    };
    ribbonDataItems = [
      {
        id: 1,
        categoryId: 0,
        categoryName: 'allsports',
        liveEventCount: 13,
        upcomingEventCount: 13,
        liveStreamEventCount: 13,
        upcommingLiveStreamEventCount: 13
      },
      {
        id: 2,
        categoryId: 19,
        categoryName: 'GH',
        liveEventCount: 2,
        upcomingEventCount: 2,
        liveStreamEventCount: 2,
        upcommingLiveStreamEventCount: 2
      },
      {
        id: 3,
        categoryId: 21,
        categoryName: 'HR',
        liveEventCount: 3,
        upcomingEventCount: 3,
        liveStreamEventCount: 3,
        upcommingLiveStreamEventCount: 3
      },
      {
        id: 4,
        categoryId: 161,
        categoryName: 'INT TOTE',
        liveEventCount: 4,
        upcomingEventCount: 4,
        liveStreamEventCount: 4,
        upcommingLiveStreamEventCount: 4
      },
      {
        id: 5,
        categoryId: 16,
        categoryName: 'football',
        liveEventCount: 5,
        upcomingEventCount: 5,
        liveStreamEventCount: 5,
        upcommingLiveStreamEventCount: 5
      }
    ];
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#getGeFilteredRibbonItemsForInPlay', () => {
    it(`should NOT filter ribbonDataItems when user is NOT german`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);

      expect(service.getGeFilteredRibbonItemsForInPlay(ribbonDataItems)).toEqual(ribbonDataItems);
    });

    it(`should NOT filter ribbonDataItems and NOT calculate filtered sportS eventsCount and sum should NOT be populated
        to first item in the list (all-sports) when user is NOT german and the first item in list with categoryId !== 0`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);

      ribbonDataItems.shift();
      // @ts-ignore
      expect(service.getGeFilteredRibbonItemsForInPlay(ribbonDataItems)).toEqual(ribbonDataItems);
    });

    it(`should filter ribbonDataItems and calculate filtered sportS eventsCount and sum should be populated
        to first item in the list (all-sports) when user is german and the first item in list with categoryId === 0`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(true);
      const expectedResult = [
        {
          id: 1,
          categoryId: 0,
          categoryName: 'allsports',
          liveEventCount: 5,
          upcomingEventCount: 5,
          liveStreamEventCount: 5,
          upcommingLiveStreamEventCount: 5
        },
        {
          id: 5,
          categoryId: 16,
          categoryName: 'football',
          liveEventCount: 5,
          upcomingEventCount: 5,
          liveStreamEventCount: 5,
          upcommingLiveStreamEventCount: 5
        }
      ];

      // @ts-ignore
      expect(service.getGeFilteredRibbonItemsForInPlay(ribbonDataItems)).toEqual(expectedResult);
    });

    it(`should filter ribbonDataItems and NOT calculate filtered sportS eventsCount and sum should NOT be populated
        to first item in the list (all-sports) when user is german and the first item in list with categoryId !== 0`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(true);
      const expectedResult = [{
        id: 5,
        categoryId: 16,
        categoryName: 'football',
        liveEventCount: 5,
        upcomingEventCount: 5,
        liveStreamEventCount: 5,
        upcommingLiveStreamEventCount: 5
      }];

      ribbonDataItems.shift();
      // @ts-ignore
      expect(service.getGeFilteredRibbonItemsForInPlay(ribbonDataItems)).toEqual(expectedResult);
    });

    it(`should NOT filter if NO ribbonDataItems(does not metter whether user is German or not!)`, () => {
      // @ts-ignore
      expect(service.getGeFilteredRibbonItemsForInPlay([])).toEqual([]);
    });
  });

  describe('#getGeFilteredRibbonItems', () => {
    it(`should NOT filter ribbonDataItems when user is NOT german`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);

      expect(service.getGeFilteredRibbonItems(ribbonDataItems)).toEqual(ribbonDataItems);
    });

    it(`should filter ribbonDataItems when user is german and there are restricted sports in ribbonDataItems`, () => {
      const expectedResult = [
          {
            id: 1,
            categoryId: 0,
            categoryName: 'allsports',
            liveEventCount: 13,
            upcomingEventCount: 13,
            liveStreamEventCount: 13,
            upcommingLiveStreamEventCount: 13
          },
          {
            id: 5,
            categoryId: 16,
            categoryName: 'football',
            liveEventCount: 5,
            upcomingEventCount: 5,
            liveStreamEventCount: 5,
            upcommingLiveStreamEventCount: 5
          }
        ],
        result = service.getGeFilteredRibbonItems(ribbonDataItems);

      expect(service['userWasGerman']).toBeTruthy();

      // @ts-ignore
      expect(result).toEqual(expectedResult);
    });

    it(`should NOT filter ribbonDataItems when user is german and there are NO restricted sports in ribbonDataItems`, () => {

      const expectedResult = [
          {
            id: 1,
            categoryId: 0,
            categoryName: 'allsports',
            liveEventCount: 13,
            upcomingEventCount: 13,
            liveStreamEventCount: 13,
            upcommingLiveStreamEventCount: 13
          },
          {
            id: 5,
            categoryId: 16,
            categoryName: 'football',
            liveEventCount: 5,
            upcomingEventCount: 5,
            liveStreamEventCount: 5,
            upcommingLiveStreamEventCount: 5
          }
        ],
        // @ts-ignore
        result = service.getGeFilteredRibbonItems(expectedResult);

      expect(service['userWasGerman']).toBeTruthy();
      // @ts-ignore
      expect(result).toEqual(expectedResult);
    });
  });

  describe('#isNewUserFromOtherCountry', () => {
    it('should should return TRUE when previously logged-in user was not german and current user is german', () => {
      const result = service.isNewUserFromOtherCountry();

      expect(service['userWasGerman']).toBeTruthy();
      expect(result).toBeTruthy();
    });

    it('should should return TRUE when previously logged-in user was german and current user is not german', () => {
      service['userWasGerman'] = true;
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
      const result = service.isNewUserFromOtherCountry();

      expect(service['userWasGerman']).toBeFalsy();
      expect(result).toBeTruthy();
    });

    it('should should return FALSE when previously logged-in user was not german and current user is not german', () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
      const result = service.isNewUserFromOtherCountry();

      expect(service['userWasGerman']).toBeFalsy();
      expect(result).toBeFalsy();
    });

    it('should should return FALSE when previously logged-in user was german and current user is german', () => {
      service['userWasGerman'] = true;
      const result = service.isNewUserFromOtherCountry();

      expect(result).toBeFalsy();
    });
  });

  describe('#applyFiltersToStructureData', () => {
    it(`should NOT apply Filters To StructureData when user is NOT german`, () => {
      service['isGermanUser'] = jasmine.createSpy().and.returnValue(false);
      const expectedModifiedStructureData = JSON.parse(JSON.stringify(structureData));

      service.applyFiltersToStructureData(structureData);

      expect(structureData).toEqual(expectedModifiedStructureData);
    });

    it(`should apply Filters To StructureData when user is german and there are restricted sports in structure`, () => {
      const expectedModifiedStructureData = {
        livenow: {
          eventCount: 3,
          eventsBySports: [{ categoryId: 16, eventCount: 3, eventsIds: [4, 5, 6] }],
          eventsIds: [4, 5, 6]
        },
        upcoming: {
          eventCount: 3,
          eventsBySports: [{ categoryId: 16, eventCount: 3, eventsIds: [11, 12, 13] }],
          eventsIds: [11, 12, 13]
        }
      };

      service.applyFiltersToStructureData(structureData);

      expect(service['userWasGerman']).toBeTruthy();

      expect(structureData).toEqual(expectedModifiedStructureData);
    });

    it(`should NOT apply Filters To StructureData when user is german and there are NO restricted sports in structure`, () => {
      const localStructureData = {
          livenow: {
            eventCount: 3,
            eventsBySports: [{ categoryId: 16, eventCount: 3, eventsIds: [4, 5, 6] }],
            eventsIds: [4, 5, 6]
          },
          upcoming: {
            eventCount: 3,
            eventsBySports: [{ categoryId: 16, eventCount: 3, eventsIds: [11, 12, 13] }],
            eventsIds: [11, 12, 13]
          }
        },
        expectedModifiedStructureData = JSON.parse(JSON.stringify(localStructureData));

      // @ts-ignore
      service.applyFiltersToStructureData(localStructureData);

      expect(service['userWasGerman']).toBeTruthy();

      expect(localStructureData).toEqual(expectedModifiedStructureData);
    });
  });
});
