import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('ScoreParserService', () => {
  let service: ScoreParserService,
    scoreParsersSpies;
  let cmsService: any;
  let eventNamePipe: EventNamePipe;

  function expectCalls(name: string, calledWith, notCalled) {
    calledWith.forEach(spy => expect(spy).toHaveBeenCalledWith(name));
    notCalled.forEach(spy => expect(spy).not.toHaveBeenCalled());
  }

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(''))
    };
    eventNamePipe = new EventNamePipe();

    service = new ScoreParserService(
      cmsService,
      eventNamePipe
    );
    scoreParsersSpies = [
      spyOn(service['scoreParsers'][0], 'parse').and.callThrough(),
      spyOn(service['scoreParsers'][1], 'parse').and.callThrough(),
      spyOn(service['scoreParsers'][2], 'parse').and.callThrough(),
      spyOn(service['scoreParsers'][3], 'parse').and.callThrough(),
      spyOn(service['scoreParsers'][4], 'parse').and.callThrough(),
      spyOn(service['scoreParsers'][5], 'parse').and.callThrough()
    ];
  });

  describe('when created', () => {
    it('should set fallbackScoreTypes if they are enabled in systemConfig', fakeAsync(() => {
      const systemConfig = {
        FallbackScoreboard: {
          enabled: true,
          Simple: '1,2,3',
          SetsLegs: '13'
        }
      };
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(systemConfig));
      service = new ScoreParserService(cmsService, eventNamePipe);
      tick();
      expect(service['fallbackScoreTypes']).toEqual({
        '1': 'Simple',
        '2': 'Simple',
        '3': 'Simple',
        '13': 'SetsLegs'
      });
    }));

    it('should not set fallbackScoreTypes if they are disabled in systemConfig', fakeAsync(() => {
      const systemConfig = {
        FallbackScoreboard: {
          enabled: false,
          Simple: '1,2,3,13',
        }
      };
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(systemConfig));
      service = new ScoreParserService(cmsService, eventNamePipe);
      tick();
      expect(service['fallbackScoreTypes']).toEqual({});
    }));

    it('should not set fallbackScoreTypes if they are not defined in systemConfig', fakeAsync(() => {
      const systemConfig = {};
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(systemConfig));
      service = new ScoreParserService(cmsService, eventNamePipe);
      tick();
      expect(service['fallbackScoreTypes']).toEqual({});
    }));
  });

  describe('parseScores when called with existing template type', () => {
    let eventName,
      type,
      expectedResult,
      parserIndex;

    it('should parse the simple score template, return the score data and skip other parsers', () => {
      type = 'Simple';
      eventName = 'TeamA 1-2 TeamB';
      expectedResult = {
        home: { score: '1', name: 'TeamA' },
        away: { score: '2', name: 'TeamB' },
        type
      };
      parserIndex = 0;
    });

    it('should parse the GAA score template, return the score data and skip other parsers', () => {
      type = 'GAA';
      eventName = 'TeamA 3-1-2-4 TeamB';
      expectedResult = {
        home: { score: '3-1', name: 'TeamA' },
        away: { score: '2-4', name: 'TeamB' },
        type
      };
      parserIndex = 1;
    });

    it('should parse the sets-points score template, return the score data and skip other parsers', () => {
      type = 'SetsPoints';
      eventName = 'TeamA* (3) 1-2 (4) TeamB';
      expectedResult = {
        home: { name: 'TeamA', score: '3', currentPoints: '1', isServing: true },
        away: { name: 'TeamB', score: '4', currentPoints: '2', isServing: false },
        type
      };
      parserIndex = 2;
    });

    it('should parse the sets-points score template, return the score data and skip other parsers', () => {
      type = 'GamesPoints';
      eventName = 'TeamA* (3) 1-2 (4) TeamB';
      expectedResult = {
        home: { name: 'TeamA', score: '3', currentPoints: '1', isServing: true },
        away: { name: 'TeamB', score: '4', currentPoints: '2', isServing: false },
        type
      };
      parserIndex = 3;
    });

    it('should parse the sets-game-points score template, return the score data and skip other parsers', () => {
      type = 'SetsGamesPoints';
      eventName = 'TeamA (5) 3 1-2 4 (6) *TeamB';
      expectedResult = {
        home: { name: 'TeamA', score: '5', periodScore: '3', currentPoints: '1', isServing: false },
        away: { name: 'TeamB', score: '6', periodScore: '4', currentPoints: '2', isServing: true },
        type
      };
      parserIndex = 4;
    });

    it('should parse the box-score (cricket) score template, return the score data and skip other parsers', () => {
      type = 'BoxScore';
      eventName = 'TeamA 10 20/30 v TeamB 40/50 60/70d';
      expectedResult = {
        home: { name: 'TeamA', score: '10 20/30', inn1: '10', inn2: '20/30' },
        away: { name: 'TeamB', score: '40/50 60/70d', inn1: '40/50', inn2: '60/70d' },
        type
      };
      parserIndex = 5;
    });

    afterEach(() => {
      expect(service.parseScores(eventName, type)).toEqual(expectedResult);
      expectCalls(eventName, scoreParsersSpies.splice(parserIndex, 1), scoreParsersSpies);
    });
  });

  describe('parseScores when called with non existing template type', () => {
    it('should return null and not call any parser', () => {
      const type = 'foobar';
      const eventName = 'TeamA 1-2 TeamB';
      const expectedResult = null;

      expect(service.parseScores(eventName, type as any)).toEqual(expectedResult);
      expectCalls(eventName, [], scoreParsersSpies);
    });
  });

  describe('getScoreType', () => {
    it('should return score type if defined in fallbackScoreTypes', () => {
      service['fallbackScoreTypes'] = {
        '1': 'Simple'
      };
      expect(service.getScoreType('1')).toBe('Simple');
    });
  });

  describe('getScoreHeaders', () => {
    it('should return score headers if they are defined for score type', () => {
      service['fallbackScoreTypes'] = {
        '1': 'GamesPoints'
      };
      expect(service.getScoreHeaders('1')).toEqual(['G', 'P']);
    });

    it('should not score headers if they are not defined for score type', () => {
      service['fallbackScoreTypes'] = {
        '1': 'Simple'
      };
      expect(service.getScoreHeaders('1')).toBeUndefined();
    });
  });

  describe('parseTypeAndScores', () => {
    it('should define simple type', () => {
      expect((service.parseTypeAndScores('TeamA 1-1 TeamB') as any).scoreType).toEqual('Simple');
    });
    it('should define SetsPoints type', () => {
      expect((service.parseTypeAndScores('TeamA (1) 2-3 (4) TeamB') as any).scoreType)
        .toEqual('SetsPoints');
    });
    it('should define SetsGamesPoints type', () => {
      expect((service.parseTypeAndScores('TeamA (1) 2 3-4 5 (6) TeamB') as any).scoreType)
        .toEqual('SetsGamesPoints');
    });
    it('should define GAA type', () => {
      expect((service.parseTypeAndScores('TeamA 1-2-3-4 TeamB') as any).scoreType).toEqual('GAA');
    });
    it('should define simple type', () => {
      expect((service.parseTypeAndScores('TeamA 10/20 30/40 v TeamB 40/50 60/70', 'CRICKET') as any).scoreType)
        .toEqual('BoxScore');
    });
    it('should return null for undefined type', () => {
      expect((service.parseTypeAndScores('--**--') as any))
        .toBeNull();
    });
  });
});
