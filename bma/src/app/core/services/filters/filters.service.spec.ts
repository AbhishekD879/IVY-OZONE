import { LocaleService } from '@core/services/locale/locale.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';
import { BehaviorSubject } from 'rxjs';
import { FiltersService } from '@core/services/filters/filters.service';

describe('FiltersService', () => {
  let service: FiltersService;

  let locale: LocaleService;
  let currencyPipe;
  let datePipe;
  let userService;
  let coreToolsService;
  let eventNamePipe;
  let greyhoundConfig,pubsub,callbackHandler;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.callFake(() => '')
    } as any;

    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    datePipe = {
      transform: jasmine.createSpy('transform').and.callFake(() => '2019-06-11')
    };

    userService = {};

    coreToolsService = new CoreToolsService;

    eventNamePipe = new EventNamePipe();

    greyhoundConfig = {
      config: {
        request: {
          categoryId: '19'
        }
      }
    };
    callbackHandler = (ctrlName: string, eventName: string, callback) => {
      if(eventName === 'USER_CLOSURE_PLAY_BREAK') {
        callback('val');
      }
    };

    pubsub = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake(callbackHandler),
      unsubscribe: jasmine.createSpy(),
      API :{USER_CLOSURE_PLAY_BREAK:'USER_CLOSURE_PLAY_BREAK'}
    };
    service = new FiltersService(
      locale,
      currencyPipe,
      datePipe,
      userService,
      coreToolsService,
      eventNamePipe,pubsub,
      greyhoundConfig
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#getComplexTranslation should call locale service for translating string by locale token', () => {
    service.getComplexTranslation('test', 'test2', 'test3');
    expect(locale.getString).toHaveBeenCalledWith('test');
  });

  describe('#chainSort', () => {
    it('#chainSort should sort array in correct way', () => {
      const arr = [
        { order: -5, name: 'web' },
        { order: 1, name: 'ftp' },
        { order: -5, name: 'bills' },
        { order: 2, name: 'test' },
        { order: 1, name: 'arch' }
      ];

      expect(service.chainSort(arr, ['order', 'name'])).toBe(arr);
      expect(arr).toEqual([
        { order: -5, name: 'bills' },
        { order: -5, name: 'web' },
        { order: 1, name: 'arch' },
        { order: 1, name: 'ftp' },
        { order: 2, name: 'test' }
      ]);
    });

    it('#chainSort should sort array in correct way', () => {
      const arr = [
        { order: 1, name: 'ftp' },
        { order: 2, name: 'test' }
      ];

      expect(service.chainSort(arr, [])).toEqual([{ order: 2, name: 'test'}, { order: 1, name: 'ftp' } ]);
    });
  });

  describe('#sportCatIcon', () => {
    it('#sportCatIcon should delete service symbols', () => {
      const givenIconPath = 'https://bitbucket.org/symphonydevelopers/bma/wiki/',
        expectedIconPath = 'httpsbitbucketorgsymphonydevelopersbmawiki';

      expect(service.sportCatIcon(givenIconPath)).toBe(expectedIconPath);
    });

    it('#sportCatIcon should delete white spaces and dots', () => {
      const givenName = '9:00 Cranbourne',
        clearedName = '900Cranbourne';

      expect(service.sportCatIcon(givenName)).toBe(clearedName);
    });

    it('#should return empty string', () => {
      expect(service.sportCatIcon(undefined)).toEqual('');
    });
  });

  describe('#currencyPosition', () => {
    it('#should return result', () => {
      const res = service.currencyPosition(2, 'se');
      expect(res).toEqual('se2');
    });

    it('#should return null', () => {
      const res = service.currencyPosition(undefined, 'se');
      expect(res).toEqual(null);
    });
  });

  describe('#date', () => {
    it('#should return result', () => {
      const res = service.date('June 11 2019', 'YYYY-MM-DD');
      expect(res).toEqual('2019-06-11');
    });
  });

  describe('#clearEventName', () => {
    it('should not remove asterisk', () => {
      const givenName = '|Player A *| (0) 1 2-3 4 (5) |Player B|',
        clearedName = '|Player A *| v |Player B|';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores for Tennis', () => {
      const givenName = '|Player A| (0) 1 2-3 4 (5) |Player B|',
        clearedName = '|Player A| v |Player B|';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores for cricket', () => {
      const givenName0 = 'Sri Lanka U19 1/2d v Sri Lanka U21 15',
        givenName1 = 'Sri Lanka 239 546/6d v England 342 155/5',
        givenName2 = '|Team A1| 217 9/9d v |Team B1| 77 56/0d',
        givenName3 = '|Team A2| 217 9/9d v |Team B2| 234/5d 430/10',
        givenName4 = '|Team A3| 217 9/9d v |Team B3| 77 56/0',
        givenName5 = '|Team A4| 217 v |Team B4|';

      expect(service.clearEventName(givenName0, 'CRICKET')).toBe('Sri Lanka U19 v Sri Lanka U21');
      expect(service.clearEventName(givenName1, 'CRICKET')).toBe('Sri Lanka v England');
      expect(service.clearEventName(givenName2, 'CRICKET')).toBe('|Team A1| v |Team B1|');
      expect(service.clearEventName(givenName3, 'CRICKET')).toBe('|Team A2| v |Team B2|');
      expect(service.clearEventName(givenName4, 'CRICKET')).toBe('|Team A3| v |Team B3|');
      expect(service.clearEventName(givenName5, 'CRICKET')).toBe('|Team A4| v |Team B4|');
    });

    it('should remove scores with Adv for Player 1 for Tennis', () => {
      const givenName = '|Player A| (0) 1 Adv-3 4 (5) |Player B|',
        clearedName = '|Player A| v |Player B|';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores with Adv for Player 2 for Tennis', () => {
      const givenName = '|Player A| (0) 1 5-Adv 4 (5) |Player B|',
        clearedName = '|Player A| v |Player B|';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores for GAA Gealic football', () => {
      const givenName = '|Player A| 1-2-4-123 |Player B|',
        clearedName = '|Player A| v |Player B|';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores for football + basketball + snooker case 1', () => {
      const givenName = 'NorthPort Batang Pier U21 17-9 Rain',
        clearedName = 'NorthPort Batang Pier U21 v Rain';

      expect(service.clearEventName(givenName)).toBe(clearedName);
    });

    it('should remove scores for football + basketball + snooker case 1', () => {

      expect(service.clearEventName(undefined, '')).toBe(undefined);
    });
  });

  describe('#setCurrency', () => {
    it('#setCurrency should add currency for number and use display property equal to code', () => {
      expect(service.setCurrency(5.90, )).toEqual('5.9£');
      expect(currencyPipe.transform).toHaveBeenCalledWith(5.90, '£', 'code');
    });

    it('#setCurrency should add currency for number and use display property equal to code', () => {
      userService.currencySymbol = '$';
      expect(service.setCurrency(3.70, )).toEqual('3.7$');
      expect(currencyPipe.transform).toHaveBeenCalledWith(3.70, '$', 'code');
    });

    it('#setCurrency should add currency for number and use display property equal to code', () => {
      expect(service.setCurrency(5.88, '£')).toEqual('5.88£');
      expect(currencyPipe.transform).toHaveBeenCalledWith(5.88, '£', 'code');
    });
  });

  describe('#setFreebetCurrency', ()=>{
    it('#setCurrencyWihtoutDecimal should display currency value without zeros after decimal', ()=>{
      expect(service.setFreebetCurrency(5.00, )).toEqual('5£');
      expect(currencyPipe.transform).toHaveBeenCalledWith(5.00, '£', 'code', '1.0');
    })
  })

  it('#setCurrencySymbol should set currency symbol in correct place', () => {
    const givenNumber = 5,
      givenNumberAsString = '5',
      givenCurrencySymbol = '$';

    expect(service.setCurrencySymbol(givenNumber, givenCurrencySymbol)).toBe('$ 5');
    expect(service.setCurrencySymbol(givenNumberAsString, givenCurrencySymbol)).toBe('5');
  });

  describe('#filterAddScore', () => {
    it('should filter market name', () => {
      const givenMarketName = 'Match tackles',
        givenOutcomeName = ' to West Indies 7+ (H)';

      expect(service.filterAddScore(givenMarketName, givenOutcomeName)).toBe('7+ Match tackles');
    });

    it('should filter market name', () => {
      const givenMarketName = 'Match Betting',
        givenOutcomeName = 'West Indies';

      expect(service.filterAddScore(givenMarketName, givenOutcomeName)).toBe(givenMarketName);
    });
  });

  it('#filterAlphabetsOnly should extract only alphabets from give string', () => {
    const givenInput = 'Score 2-4';

    expect(service.filterAlphabetsOnly(undefined)).toBe(null);
    expect(service.filterAlphabetsOnly(givenInput)).toBe('Score');
  });

  it('#filterAlphabetsOnlyTrimUnderscore should extract only alphabets from give string', () => {
    expect(service.filterAlphabetsOnlyTrimUnderscore(undefined)).toBe(null);
    expect(service.filterAlphabetsOnlyTrimUnderscore('Score 2-4')).toBe('Score');
  });

  it('#filterAlphabetsOnlyTrimUnderscore should trim last underscore', () => {
    expect(service.filterAlphabetsOnlyTrimUnderscore('Score-2-4')).toBe('Score');
  });

  describe('#filterNumbersOnly', () => {
    it('#filterNumbersOnly should extract only score from give string', () => {
      const givenInput = 'Score 2-4';

      expect(service.filterNumbersOnly(undefined)).toBe('');
      expect(service.filterNumbersOnly(givenInput)).toBe('2-4');
    });

    it('#should retun empty string', () => {
      const givenInput = 'Score';

      expect(service.filterNumbersOnly(givenInput)).toBe('');
    });
  });

  describe('#distance', () => {
    it('should convert distance in correct format', () => {
      const givenDistance = '12.34 meter';

      expect(service.distance(givenDistance)).toBe(' 12y');
    });

    it('should get formatted distance string', () => {
      const distanceMockMeters = '10 Meters';
      const distanceMockYards = '10 yards';

      const resultMeters = service.distance(distanceMockMeters);
      const resultYards = service.distance(distanceMockYards);

      expect(resultMeters).toBe(' 11y');
      expect(resultYards).toBe(' 10y');
    });

    it('should return empty string', () => {
      const givenDistance = '0.7';

      expect(service.distance(givenDistance)).toBe(' ');
    });

    it('should get formatted distance string', () => {

      const res = service.distance('100000 Meters');

      expect(res).toBe(' 62m 1f 21y');
    });
  });

  it('#removeLineSymbol should remove line symbols', () => {
    const givenLineSymbol = '12.34|meter';

    expect(service.removeLineSymbol(undefined)).toBe(undefined);
    expect(service.removeLineSymbol(givenLineSymbol)).toBe('12.34meter');
  });

  it('#removenNonRunnerFromHorseName should remove line symbols and N/R', () => {
    const givenLineSymbol = '12.34|meter N/R';
    expect(service.removenNonRunnerFromHorseName(undefined)).toBe('');
    expect(service.removenNonRunnerFromHorseName(givenLineSymbol)).toBe('12.34meter ');
  });

  describe('#numberWithCurrency', () => {
    it('should format positive number', () => {
      expect(service.numberWithCurrency(12)).toBe('£12.00');
    });

    it('should format negative number with given symbol', () => {
      expect(service.numberWithCurrency(-0.1, '$')).toBe('- $0.10');
    });

    it('should format undefined param with userService.currencySymbol', () => {
      userService.currencySymbol = 'Kr';
      expect(service.numberWithCurrency(undefined)).toBe('Kr0.00');
    });
  });

  describe('#numberSuffix', () => {
    it(' should choose correct suffix', () => {
      const givenNumber = 245;

      expect(service.numberSuffix(undefined)).toBe('sb.numSuffixTh');
      expect(service.numberSuffix(givenNumber)).toBe('sb.numSuffixTh');
    });

    it('should choose correct suffix, case with string', () => {
      const givenNumber = '245';

      expect(service.numberSuffix(givenNumber)).toBe('sb.numSuffixTh');
    });
  });

  describe('#makeHandicapValue', () => {
    beforeEach(() => {
      locale = {
        getString: jasmine.createSpy().and.callFake(() => 'HL')
      } as any;
      service = new FiltersService(
        locale,
        currencyPipe,
        datePipe,
        userService,
        coreToolsService,
        eventNamePipe,pubsub,
        greyhoundConfig
      );
    })
    it('#makeHandicapValue should transform string', () => {
      const givenStringWithMinus = 'Test+ string - 1',
        givenStringWithoutMines = 'Test+ string 2';

      expect(service.makeHandicapValue(givenStringWithMinus, null)).toBe(' (Teststring-1)');
      expect(service.makeHandicapValue(givenStringWithoutMines, null)).toBe(' (+Teststring2)');
    });

    it('#makeHandicapValue should have outcome with outcomeMeaningMajorCode|eventMarketSort', () => {
      const givenStringWithMinus = 'Test+ string1',
        givenStringWithoutMines = 'Test+ string2';
      expect(service.makeHandicapValue(givenStringWithMinus, { outcomeMeaningMajorCode: 'HL' })).toBe(' (Teststring1)');
      expect(service.makeHandicapValue(givenStringWithoutMines, { eventMarketSort: 'HL' } as any)).toBe(' (Teststring2)');
    });
    it('#makeHandicapValue should have outcome but no under/over', () => {
      const givenStringWithMinus = 'Test+ string - 1',
        givenStringWithoutMines = 'Test+ string 2';

      expect(service.makeHandicapValue(givenStringWithMinus, { outcomeMeaningMajorCode: 'AH', eventMarketSort: '' })).toBe(' (Teststring-1)');
      expect(service.makeHandicapValue(givenStringWithoutMines, { eventMarketSort: 'AH', outcomeMeaningMajorCode: '' })).toBe(' (+Teststring2)');
    });
  })
  describe('#getScoreFromName', () => {
    it('should extract game score', () => {
      const givenStringWithScore = ' Arsenal 3-2 Sampdoria  ';

      expect(service.getScoreFromName(undefined)).toBe('');
      expect(service.getScoreFromName(givenStringWithScore)).toBe('3-2');
    });

    it('should return empty string', () => {
      const givenStringWithScore = 'Arsenal';

      expect(service.getScoreFromName(givenStringWithScore)).toBe('');
    });
  });

  describe('#filterPlayerName', () => {
    it('should filter player name, home case', () => {
      const givenString = 'String part 1 to home away (H) string',
        givenStringWrong = 'String part 1 to home away (W) string';

      expect(service.filterPlayerName(givenString)).toBe('String part 1');
      expect(service.filterPlayerName(givenStringWrong)).toBe(givenStringWrong);
    });

    it('should filter player name, away case', () => {
      const givenString = 'String part 1 to away (A) string';

      expect(service.filterPlayerName(givenString)).toBe('String part 1');
    });
  });

  describe('#filterLink', () => {
    it('should delete wrong symbols from URL', () => {
      const givenString = '//bm-tst1.coral . co .uk/test ? catch  = 25';

      expect(service.filterLink(givenString)).toBe('/bm-tst1.coral.co.uk/test?catch=25');
    });

    it('#should delete wrong symbols from URL', () => {
      const givenString = '/bm-tst1.coral . co .uk/test ?+ % h';

      expect(service.filterLink(givenString)).toBe('/bm-tst1.coral.co.uk/test?+%25h');
    });

    it('#should return that same URL', () => {
      const givenString = 'www.4+Uo4RYSvH7cP2xapT9YaxHrfk4oV.8_EXof.YL';

      expect(service.filterLink(givenString)).toBe('www.4+Uo4RYSvH7cP2xapT9YaxHrfk4oV.8_EXof.YL');
    });

    it('#should case without link', () => {

      expect(service.filterLink(undefined)).toBe(undefined);
    });
  });

  describe('#getTeamName', () => {
    it('should select correct name of team name', () => {
      const givenTeamName1 = 'home vs away',
        givenTeamName2 = 'home v away',
        givenTeamName3 = 'home @ away',
        givenTeamName4 = 'home / away',
        givenTeamName5 = 'home - away';

      expect(service.getTeamName(givenTeamName1, 0)).toBe('home');
      expect(service.getTeamName(givenTeamName1, 1)).toBe('away');
      expect(service.getTeamName(givenTeamName2, 0)).toBe('home');
      expect(service.getTeamName(givenTeamName2, 1)).toBe('away');
      expect(service.getTeamName(givenTeamName3, 0)).toBe('home');
      expect(service.getTeamName(givenTeamName3, 1)).toBe('away');
      expect(service.getTeamName(givenTeamName4, 0)).toBe('home ');
      expect(service.getTeamName(givenTeamName4, 1)).toBe(' away');
      expect(service.getTeamName(givenTeamName5, 0)).toBe('home');
      expect(service.getTeamName(givenTeamName5, 1)).toBe('away');
    });

    it('getTeamName for gaelic football', () => {
      const eventName = '|Player A| 1-2-4-123 |Player B|';

      expect(service.getTeamName(eventName, 0)).toEqual('|Player A|');
      expect(service.getTeamName(eventName, 1)).toEqual('|Player B|');
    });

    it('getTeamName for simple scores', () => {
      const eventName = '|Player A| 2-3 |Player B|';

      expect(service.getTeamName(eventName, 0)).toEqual('|Player A|');
      expect(service.getTeamName(eventName, 1)).toEqual('|Player B|');
    });

    it('should return empty string', () => {
      const eventName = '';

      expect(service.getTeamName(eventName, 0)).toEqual('');
    });
  });

  it('#getTimeFromName should extract time from name', () => {
    const givenWrongTime = 'testTest',
      givenRightTime = '12:00TEST';

    expect(service.getTimeFromName(givenWrongTime)).toBe('');
    expect(service.getTimeFromName(givenRightTime)).toBe('12:00');
  });

  it('#numberTranslatedSuffix should get translated suffix', () => {
    const stNumberMock = 1;
    const ndNumberMock = 2;
    const rdNumberMock = 3;
    const thNumberMock = 20;

    service.numberTranslatedSuffix(stNumberMock);
    expect(locale.getString).toHaveBeenCalledWith('sb.numSuffixSt');

    service.numberTranslatedSuffix(ndNumberMock);
    expect(locale.getString).toHaveBeenCalledWith('sb.numSuffixNd');

    service.numberTranslatedSuffix(rdNumberMock);
    expect(locale.getString).toHaveBeenCalledWith('sb.numSuffixRd');

    service.numberTranslatedSuffix(thNumberMock);
    expect(locale.getString).toHaveBeenCalledWith('sb.numSuffixTh');
  });

  it('#clearSportClassName should clear class name', () => {
    const className = 'Football',
      categoryName = 'England';

    expect(service.clearSportClassName(undefined, categoryName)).toBe('');
    expect(service.clearSportClassName('England', categoryName)).toBe(categoryName);
    expect(service.clearSportClassName(className, categoryName)).toBe('Football');
  });

  describe('orderBy', () => {
    const array = [
      { date: '123456', displayOrder: 0, name: 'A', id: 1 },
      { date: 323456, displayOrder: '0', name: 'B', id: 2 },
      { date: '223456', displayOrder: 0, name: 'E', id: 3 },
      { date: '023456', displayOrder: '0', name: 'C', id: 4 },
    ];

    const arraySameDateAndDisplayOrder = [
      { date: '123456', displayOrder: '0', name: 'A', id: 1 },
      { date: '123456', displayOrder: 0, name: 'B', id: 2 },
      { date: 123456, displayOrder: '0', name: 'E', id: 3 },
      { date: '123456', displayOrder: 0, name: 'C', id: 4 },
    ];

    it(`should order by 'date' if 'date' is Not the same`, () => {
      const arrOrdered = service.orderBy(array, ['date', 'displayOrder', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([4, 1, 3, 2]);
    });

    it(`should Not modifuy order of current array`, () => {
      service.orderBy(array, ['date', 'displayOrder', 'name']);

      expect(array.map(el => el.id)).toEqual([1, 2, 3, 4]);
    });

    it(`should order by 'displayOrder' if 'date' is the same`, () => {
      const arraySameDate = [
        { date: '123456', displayOrder: '-1', name: 'A', id: 1 },
        { date: '123456', displayOrder: '1', name: 'B', id: 2 },
        { date: '123456', displayOrder: -3, name: 'E', id: 3 },
        { date: '123456', displayOrder: '0', name: 'C', id: 4 },
      ];

      const arrOrdered = service.orderBy(arraySameDate, ['date', 'displayOrder', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([3, 1, 4, 2]);
    });

    it(`should order by 'name' if 'date' and 'displayOrder'is the same`, () => {
      const arrOrdered = service.orderBy(arraySameDateAndDisplayOrder, ['date', 'displayOrder', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([1, 2, 4, 3]);
    });

    it(`should order by 'name' if fields equal 'name'`, () => {
      const arrOrdered = service.orderBy(arraySameDateAndDisplayOrder, ['date', 'displayOrder', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([1, 2, 4, 3]);
    });

    it(`should order by 'name' if fields equal 'name'`, () => {
      const arrayDifferentProps = [
        { date: 123456, displayOrder: -3, name: 'A', id: 1 },
        { date: '423456', displayOrder: '0', name: 'B', id: 2 },
        { date: '023456', displayOrder: '0', name: 'E', id: 3 },
        { date: 323456, displayOrder: '0', name: 'C', id: 4 },
      ];

      const arrOrdered = service.orderBy(arrayDifferentProps, ['name']);

      expect(arrOrdered.map(el => el.id)).toEqual([1, 2, 4, 3]);
    });

    it(`should order by 'arr[1]'`, () => {
      const arrayWithPropArray = [
        { date: 123456, arr: [1, -3], name: 'A', id: 1 },
        { date: '423456', arr: [3, 0], name: 'B', id: 2 },
        { date: 123456, arr: [3, '0'], name: 'B', id: 3 },
        { date: '023456', arr: [-8, 11], name: 'E', id: 4 },
        { date: 323456, arr: [0, -7], name: 'C', id: 5 },
      ];

      const arrOrdered = service.orderBy(arrayWithPropArray, ['arr[1]', 'date']);

      expect(arrOrdered.map(el => el.id)).toEqual([5, 1, 3, 2, 4]);
    });

    it(`should order by 'date' and 'name' with fixed to 1 after point`, () => {
      const arrayWithPropDecimal = [
        { date: 1.199999, arr: [1, -3], name: 'B', id: 1 },
        { date: 1.188888, arr: [3, 0], name: 'A', id: 2 },
        { date: -2.23, arr: [3, '0'], name: 'd', id: 3 },
        { date: '-2.22', arr: [-8, 11], name: 'c', id: 4 },
        { date: 0.89, arr: [0, -7], name: 'f', id: 5 },
        { date: 0.88, arr: [0, -7], name: 'g', id: 6 },
      ];

      const arrOrdered = service.orderBy(arrayWithPropDecimal, ['date', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([4, 3, 5, 6, 2, 1]);
    });

    it(`should sort by 'defaultField' if prop is empty does Not has this prop`, () => {
      const arr = [{ time: 1, name: 'A', id: 1 },
        { name: 'F', id: 2 },
        { time: 3, name: 'A', id: 3 },
        { time: -3, name: 'A', id: 4 },
        { time: -1, name: 'A', id: 5 },
        { name: 'D', id: 6 }];
      const arrOrdered = service.orderBy(arr, ['time', 'name'], '0');

      expect(arrOrdered.map(el => el.id)).toEqual([4, 5, 6, 2, 1, 3]);
    });

    it(`should omit object if it doesn't have property under which we're sorting, case of numbers`, () => {
      const arr = [
        { displayOrder: 7, customOrder: 7, name: 'A', id: 7 },
        { displayOrder: 1, customOrder: 10, name: 'A', id: 1 },
        { displayOrder: 5, name: 'E', id: 2 },
        { displayOrder: 0, customOrder: 6, name: 'B', id: 4 },
        { displayOrder: 2, name: 'K', id: 3 },
      ];
      const expectedArr = [
        { displayOrder: 0, customOrder: 6, name: 'B', id: 4 },
        { displayOrder: 7, customOrder: 7, name: 'A', id: 7 },
        { displayOrder: 1, customOrder: 10, name: 'A', id: 1 },
        { displayOrder: 2, name: 'K', id: 3 },
        { displayOrder: 5, name: 'E', id: 2 },
      ];
      const arrOrdered = service.orderBy(arr, ['customOrder', 'displayOrder']);

      expect(arrOrdered).toEqual(expectedArr);
    });

    it(`should omit object if it doesn't have property under which we're sorting, case of strings`, () => {
      const arr = [
        { displayOrder: 7, customOrder: 'bb', name: 'B', id: 7 },
        { displayOrder: 1, customOrder: 'kk', name: 'A', id: 1 },
        { displayOrder: 4, name: 'K', id: 3 },
        { displayOrder: 2, name: 'L', id: 2 },
      ];
      const expectedArr = [
        { displayOrder: 7, customOrder: 'bb', name: 'B', id: 7 },
        { displayOrder: 1, customOrder: 'kk', name: 'A', id: 1 },
        { displayOrder: 2, name: 'L', id: 2 },
        { displayOrder: 4, name: 'K', id: 3 },
      ];
      const arrOrdered = service.orderBy(arr, ['customOrder', 'displayOrder']);

      expect(arrOrdered).toEqual(expectedArr);
    });

    it(`should order reverse`, () => {
      const arrOrdered = service.orderBy(array, ['-date', 'displayOrder', 'name']);

      expect(arrOrdered.map(el => el.id)).toEqual([2, 3, 1, 4]);
    });
  });

  describe('isGreyhoundsEvent', () => {
    it('should return true', () => {
      expect(service['isGreyhoundsEvent']('19')).toBe(true);
    });

    it('should return false', () => {
      expect(service['isGreyhoundsEvent']('1')).toBe(false);
    });
  });

  describe('initialClassIds', () => {
    it('should return class id', () => {
      const allClasses = {
        result: [{class: {id: '345'}}],
        id: '345'
      } as  any;
      const res = service.initialClassIds(allClasses, '345');
      expect(res).toEqual({class: { id: '345' }} as any);
    });

    it('should empty string', () => {
      const res = service.initialClassIds({} as any, undefined);
      expect(res).toEqual('');
    });
  });

  describe('orderRightMenuBySection', () => {
    it('should order menu by section', () => {
      const input = [
        {section: 'bottom'},
        {section: 'top'},
        {section: 'center'},
      ];
      const res = service.orderRightMenuBySection(input);
      expect(res).toEqual([
        {section: 'top'},
        {section: 'center'},
        {section: 'bottom'}
      ]);
    });

    it('should return undefined', () => {
      const res = service.orderRightMenuBySection(undefined);
      expect(res).toEqual(undefined);
    });
  });

  describe('objectPromise', () => {
    it('should return objectPromise', () => {
      const sportEvents = [{
        id: '12343',
        typeId: 'type1',
        name: 'Football Event',
        markets: [{
          id: '345345',
          name: 'Total Goals Over/Under',
          templateMarketName: 'market template 1',
          outcomes: [{
            id: '1257',
            name: 'Eibar',
          }]
        }]
      }, {
        typeId: 'type1',
        id: '2423',
        name: 'Real Madrid',
        markets: []
      }] as any;

      service.objectPromise(sportEvents[1]);

      expect(sportEvents[1]).toEqual({ id: '2423', markets: [], name: 'Real Madrid', typeId: 'type1'});
    });
  });

  describe('groupBy', () => {
    it('should return undefined', () => {
      const res = service.groupBy(undefined, '2');
      expect(res).toEqual(undefined);
    });

    it('should groupBy', () => {
      const input = [
        { 2: [345]},
        { 1: [3], 2: [77], 3: [''] }
      ];
      const res = service.groupBy(input, '2');
      expect(res).toEqual({ 1: [], 2: [], 3: [] });
    });

    it('should groupBy and push res' , () => {
      const input = [
        { 2: [345]},
        { 1: [3], 2: [77], 3: [''] }
      ];
      const res = service.groupBy(input, '1');
      expect(res).toEqual({ 1: [], 2: [], 3: [{ 1: [ 3 ], 2: [ 77 ], 3: [ '' ] }] });
    });
  });
  describe('#filterLinksForRss', () => {
  it('#filterLinksForRss should filter the link for RSS', () => {
    service['filterLinkforRSS']('racingsuperseries');
    const callbacks = {};
    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    const rssUrl =  new BehaviorSubject('racingsuperseries');
      expect(rssUrl.asObservable).toEqual(jasmine.any(Function));
  });
  
});
});
