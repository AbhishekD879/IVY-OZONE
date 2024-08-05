import { MarketSortService } from './market-sort.service';
import { eventsMock } from './events-mock';

describe('MarketSortService ', () => {
  let service: MarketSortService;
  let iTypeSegmentMock: any;
  let marketIndex: number;

  beforeEach(() => {
    service = new MarketSortService();
    marketIndex = 0;
    iTypeSegmentMock = eventsMock.data;
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('setMarketFilterForOneSection void', () => {
    it('should filter markets', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[0], 'Match Betting');

      expect(iTypeSegmentMock[0].defaultValue).toBe('Match Betting');
      expect(iTypeSegmentMock[0].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[0].deactivated).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[1].deactivated).toBe(true);
      marketIndex = 1;
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].hidden).toBe(true);
      expect(iTypeSegmentMock[0].groupedByDate[0].deactivated).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[1].deactivated).toBe(true);
    });

    it('should not filter markets', () => {
      service['hideSectionIfNoVisibleEvents'] = jasmine.createSpy('hideSectionIfNoVisibleEvents');

      service.setMarketFilterForOneSection([] as any, 'Match Betting');
      expect(service['hideSectionIfNoVisibleEvents']).not.toHaveBeenCalled();
    });
    it('should filter markets and marketIndex is equal to 1 when there is handicap value', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[0], 'Total Points');
      marketIndex = 1;
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].hidden).toBe(false);
    });
    it('should filter markets and marketIndex is greater than 1 when there is handicap value', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[2], 'Total Points');
      marketIndex = 2;
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[0].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[1].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[1].hidden).toBe(true);
    });
    it('should filter markets and no change in marketIndex when there is no handicap value', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[3], 'Match Betting');
      expect(iTypeSegmentMock[3].groupedByDate[0].events[0].markets[0].rawHandicapValue).toBeFalsy();
      expect(marketIndex).toBe(0);
    });
    it('should set deactivated true when market is Current Set Winner and of Inplay category', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[4], 'Current Set Winner');
      expect(iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
    });
    it('should set deactivated false when market is Current Set Winner and of pre-match category', () => {
      service.setMarketFilterForOneSection(iTypeSegmentMock[5], 'Current Set Winner');
      expect(iTypeSegmentMock[5].groupedByDate[0].events[0].markets[1].hidden).toBe(true);
    });
  });

  describe('setMarketFilterForMultipleSections void', () => {
    it('should filter markets', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Match Betting');

      expect(iTypeSegmentMock[0].defaultValue).toBe('Match Betting');
      expect(iTypeSegmentMock[1].defaultValue).toBe('Match Betting');
      expect(iTypeSegmentMock[0].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[0].deactivated).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[1].deactivated).toBe(true);
      expect(iTypeSegmentMock[1].groupedByDate[0].deactivated).toBe(false);
      expect(iTypeSegmentMock[1].groupedByDate[1].deactivated).toBe(true);
      marketIndex = 1;
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].hidden).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[0].deactivated).toBe(false);
      expect(iTypeSegmentMock[0].groupedByDate[1].deactivated).toBe(true);
    });

    it('should not filter markets for group', () => {
      service['hideSectionIfNoVisibleEvents'] = jasmine.createSpy('hideSectionIfNoVisibleEvents');

      service.setMarketFilterForMultipleSections([{}] as any, 'Match Betting');

      expect(service['hideSectionIfNoVisibleEvents']).toHaveBeenCalledTimes(1);
      expect(service['hideSectionIfNoVisibleEvents'])
        .toHaveBeenCalledWith({ defaultValue: 'Match Betting' } as any, 'Match Betting');
    });

    it('should filter markets and marketIndex is equal to 1 when there is handicap value', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Total Points');
      marketIndex = 1;
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[0].groupedByDate[1].events[0].markets[0].hidden).toBe(false);
    });
    it('should filter markets and marketIndex is greater than 1 when there is handicap value', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Total Points');
      marketIndex = 2;
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[0].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[1].rawHandicapValue).toBeTruthy();
      expect(iTypeSegmentMock[2].groupedByDate[0].events[0].markets[1].hidden).toBe(true);
    });
    it('should filter markets and no change in marketIndex when there is no handicap value', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Match Betting');
      expect(iTypeSegmentMock[3].groupedByDate[0].events[0].markets[0].rawHandicapValue).toBeFalsy();
      expect(marketIndex).toBe(0);
    });
    it('should set deactivated true when market is Current Set Winner and of Inplay category', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Current Set Winner');
      expect(iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
    });
    it('should set deactivated false when market is Current Set Winner and of pre-match category', () => {
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Current Set Winner');
      expect(iTypeSegmentMock[5].groupedByDate[0].events[0].markets[1].hidden).toBe(true);
    });
    it('should call setMarketFilterForMultipleSections when market is Set 1 Winner with set Index', () => {
      iTypeSegmentMock[4].groupedByDate[0].events[0].comments = {runningSetIndex: 2};
      iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].name = 'Set 1 Winner';
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Current Set Winner');
      expect(iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
    });
    it('should call setMarketFilterForMultipleSections when market is Set 1 Winner and hidden false', () => {
      iTypeSegmentMock[4].groupedByDate[0].events[0].comments = {runningSetIndex: 1};
      iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].name = 'Set 1 Winner';
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Current Set Winner');
      expect(iTypeSegmentMock[4].groupedByDate[0].events[0].markets[0].hidden).toBe(false);
    });
    it('should call setMarketFilterForMultipleSections when Frame X Winner', () => {
      iTypeSegmentMock[5].groupedByDate[0].events[0] = {
        id: 10, eventIsLive: true,comments: {runningSetIndex: 0}, markets: [{
          id: 10, templateMarketName: 'Frame X Winner', name: 'Frame 1 Winner', displayOrder: 1, hidden: false
        },
        {
          id: 11, templateMarketName: 'Frame X Winner', name: 'Frame 2 Winner', displayOrder: 2, hidden: false
        }]
      };
      service.setMarketFilterForMultipleSections(iTypeSegmentMock, 'Frame X Winner');
      expect(iTypeSegmentMock[5].groupedByDate[0].events[0].markets[1].hidden).toBe(true);
    });
  });
});
