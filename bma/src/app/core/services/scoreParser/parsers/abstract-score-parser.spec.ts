import { AbstractScoreParser } from '@core/services/scoreParser/parsers/abstract-score-parser';
import { IScoreData, ITypedScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('AbstractScoreParser', () => {
  let parser: TestScoreParser;
  let eventNamePipe: EventNamePipe;

  class TestScoreParser extends AbstractScoreParser {
    protected type: IScoreType = 'Simple';
    protected pattern: RegExp = /^(.*) vs (.*)$/;
    protected matcher(matchArray: string[]): IScoreData {
      return { home: { name: matchArray[1] }, away: { name: matchArray[2] } } as IScoreData;
    }
  }

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new TestScoreParser(eventNamePipe);
  });

  describe('@getType', () => {
    it('should return parser type', () => {
      expect(parser.getType()).toEqual('Simple');
    });
  });

  describe('@parse', () => {
    describe('should return null if', () => {
      it('non-string argument is provided', () => {
        const result = [undefined, null, true, 1, {}].every(v => parser.parse(v as any) === null);
        expect(result).toEqual(true);
      });

      describe('string argument is provided', () => {
        it('and pattern is not an instance of RegExp', () => {
          parser['pattern'] = 'not-a-reg-exp' as any;
          expect(parser.parse('team1 vs team2')).toEqual(null);
        });
        it('and string argument does not match parser pattern', () => {
          expect(parser.parse('team1 v team2')).toEqual(null);
        });
        it('and matcher returns falsy value', () => {
          parser['matcher'] = () => undefined;
          expect(parser.parse('team1 vs team2')).toEqual(null);
        });
      });
    });

    it('should pass the match array to the matcher method of a parser', () => {
      parser['matcher'] = jasmine.createSpy('matcherSpy');
      parser.parse('team1 vs team2');
      expect(parser['matcher']).toHaveBeenCalledWith(jasmine.objectContaining(['team1 vs team2', 'team1', 'team2']));
    });

    it('should return parsed data object from the match array, extended with type property', () => {
      expect(parser.parse('team1 vs team2')).toEqual(
        { home: { name: 'team1' }, away: { name: 'team2' }, type: 'Simple' } as ITypedScoreData);
    });
  });

  describe('scoreRegExp', () => {
    it('should return null by default', () => {
      expect(parser.scoreRegExp).toBeNull();
    });

    it('should return scorePattern', () => {
      parser['scorePattern'] = new RegExp('/*/');

      expect(parser.scoreRegExp).toBe(parser['scorePattern']);
    });
  });

  describe('test', () => {
    it('should return false if no pattern for test', () => {
      parser['pattern'] = null;

      expect(parser.test('Some Event')).toEqual(false);
    });

    it('should return false if not match pattern', () => {
      parser['pattern'] = /123/;

      expect(parser.test('321')).toEqual(false);
    });

    it('should return true if match pattern', () => {
      parser['pattern'] = /123/;

      expect(parser.test('123')).toEqual(true);
    });
  });

  describe('replaceScores', () => {
    it('should value as is if no parser fo score', () => {
      parser['scorePattern'] = null;

      expect(parser.replaceScores('Some Event')).toEqual('Some Event');
    });

    it('should replace search value on default by pattern', () => {
      parser['scorePattern'] = /123/;

      expect(parser.replaceScores('Some 123 Event')).toEqual('Some  Event');
    });

    it('should replace search value', () => {
      parser['scorePattern'] = /123/;

      expect(parser.replaceScores('Some 123 Event', 'replacer')).toEqual('Some replacer Event');
    });
  });
});
