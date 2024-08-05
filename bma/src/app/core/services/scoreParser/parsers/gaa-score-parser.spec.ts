import { GaaScoreParser } from '@core/services/scoreParser/parsers/gaa-score-parser';
import { ITeamScoreData } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('GaaScoreParser', () => {
  let parser: GaaScoreParser;
  let eventNamePipe: EventNamePipe;

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new GaaScoreParser(eventNamePipe);
  });

  describe('should match and parse strings:', () => {
    let testString: string,
      expectedHome: ITeamScoreData,
      expectedAway: ITeamScoreData;

    it('as home-team, home-score, away-score, away-team', () => {
      testString = 'TeamA 3-1-2-4 TeamB';
      expectedHome = { name: 'TeamA', score: '3-1' };
      expectedAway = { name: 'TeamB', score: '2-4' };
    });

    it('the trailing (BG) substring is ignored', () => {
      testString = 'TeamA 3-1-2-4 TeamB(BG)';
      expectedHome = { name: 'TeamA', score: '3-1' };
      expectedAway = { name: 'TeamB', score: '2-4' };
    });

    it('the trailing (BG) substring is ignored regardless of spaces', () => {
      testString = 'TeamA 3-1-2-4 TeamB  (BG)  ';
      expectedHome = { name: 'TeamA', score: '3-1' };
      expectedAway = { name: 'TeamB', score: '2-4' };
    });

    it('trailing and leading spaces in names are trimmed', () => {
      testString = '   Team A   30-10-20-40  Team  B   ';
      expectedHome = { name: 'Team A', score: '30-10' };
      expectedAway = { name: 'Team  B', score: '20-40' };
    });

    it('any space-separated Z numbers next to X-Y-U-V score group is treated as part of the name', () => {
      testString = 'TeamA 100 3-1-2-4 13 TeamB';
      expectedHome = { name: 'TeamA 100', score: '3-1' };
      expectedAway = { name: '13 TeamB', score: '2-4' };
    });

    it('any space-separated (Z) number next to X-Y-U-V score group is treated as part of name', () => {
      testString = 'TeamA (1) 3-1-2-4 (2) TeamB';
      expectedHome = { name: 'TeamA (1)', score: '3-1' };
      expectedAway = { name: '(2) TeamB', score: '2-4' };
    });

    it('first X-Y-U-V number pair is treated as score', () => {
      testString = 'TeamA 3-1-2-4 7-5-6-8 TeamB';
      expectedHome = { name: 'TeamA', score: '3-1' };
      expectedAway = { name: '7-5-6-8 TeamB', score: '2-4' };
    });

    afterEach(() => {
      expect(parser.parse(testString)).toEqual({
        home: expectedHome,
        away: expectedAway,
        type: 'GAA'
      });
    });
  });

  describe('should not match strings and return null', () => {
    it('if general pattern is not matched (no valid X-Y-U-V score group)', () => {
      expect(parser.parse('TeamA vs TeamB')).toEqual(null);
      expect(parser.parse('TeamA 1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1-2 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1-2-4-0 TeamB')).toEqual(null);
    });

    it('if any number of X-Y-U-V score group is missing)', () => {
      expect(parser.parse('TeamA -1-2-4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3--2-4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1--4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1-2- TeamB')).toEqual(null);
    });

    it('if there is unexpected space in X-Y-U-V score group', () => {
      expect(parser.parse('TeamA 3- 1-2-4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1- 2-4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1-2- 4 TeamB')).toEqual(null);
    });

    it('if there is no space between X-Y-U-V score group and team name', () => {
      expect(parser.parse('TeamA3-1-2-4 TeamB')).toEqual(null);
      expect(parser.parse('TeamA 3-1-2-4TeamB')).toEqual(null);
    });
  });
});
