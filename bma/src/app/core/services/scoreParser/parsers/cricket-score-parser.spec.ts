import { CricketScoreParser } from '@core/services/scoreParser/parsers/cricket-score-parser';
import { ITeamScoreData } from '@core/services/scoreParser/models/score-data.model';
import { EventNamePipe } from '@shared/pipes/event-name/event-name.pipe';

describe('CricketScoreParser', () => {
  let parser: CricketScoreParser;
  let eventNamePipe: EventNamePipe;

  beforeEach(() => {
    eventNamePipe = new EventNamePipe();
    parser = new CricketScoreParser(eventNamePipe);
  });

  describe('should match and parse strings:', () => {
    let testString: string,
      expectedHome: ITeamScoreData,
      expectedAway: ITeamScoreData;

    it('as home-team home-inn-1 v away-team', () => {
      testString = 'Team A 169/7 v Team B';
      expectedHome = { name: 'Team A', score: '169/7', inn1: '169/7', inn2: undefined };
      expectedAway = { name: 'Team B', score: undefined, inn1: undefined, inn2: undefined };
    });


    it('as home-team home-inn-1 v away-team with "1st" text', () => {
      testString = 'Team A 1st 169/7 v Team B';
      expectedHome = { name: 'Team A 1st', score: '169/7', inn1: '169/7', inn2: undefined };
      expectedAway = { name: 'Team B', score: undefined, inn1: undefined, inn2: undefined };
    });

    it('as home-team v away-team away-inn-1', () => {
      testString = 'Team A v Team B 200/2';
      expectedHome = { name: 'Team A', score: undefined, inn1: undefined, inn2: undefined };
      expectedAway = { name: 'Team B', score: '200/2', inn1: '200/2', inn2: undefined };
    });

    it('as home-team home-inn-1 v away-team away-inn-1', () => {
      testString = 'Team A 169/7 v Team B 200/2';
      expectedHome = { name: 'Team A', score: '169/7', inn1: '169/7', inn2: undefined };
      expectedAway = { name: 'Team B', score: '200/2', inn1: '200/2', inn2: undefined };
    });

    it('as home-team home-inn-1 home-inn-2 v away-team away-inn-1', () => {
      testString = 'Team A 169/7 20/5d v Team B 200/2';
      expectedHome = { name: 'Team A', score: '169/7 20/5d', inn1: '169/7', inn2: '20/5d' };
      expectedAway = { name: 'Team B', score: '200/2', inn1: '200/2', inn2: undefined };
    });

    it('as home-team home-inn-1 v away-team away-inn-1 away-inn-2', () => {
      testString = 'Team A 169/7 v Team B 200/2 300';
      expectedHome = { name: 'Team A', score: '169/7', inn1: '169/7', inn2: undefined };
      expectedAway = { name: 'Team B', score: '200/2 300', inn1: '200/2', inn2: '300' };
    });

    it('as home-team home-inn-1 home-inn-2 v away-team away-inn-1 away-inn-2', () => {
      testString = 'Team A 169/7 400/5d v Team B 200/2 300';
      expectedHome = { name: 'Team A', score: '169/7 400/5d', inn1: '169/7', inn2: '400/5d' };
      expectedAway = { name: 'Team B', score: '200/2 300', inn1: '200/2', inn2: '300' };
    });

    it('as TeamA U21 1st 15 v TeamB U21 15/17d', () => {
      testString = ' TeamA U21 1st  15   v   TeamB U21    15/17d    ';
      expectedHome = { name: 'TeamA U21 1st', score: '15', inn1: '15', inn2: undefined };
      expectedAway = { name: 'TeamB U21', score: '15/17d', inn1: '15/17d', inn2: undefined };
    });

    afterEach(() => {
      expect(parser.parse(testString)).toEqual({
        home: expectedHome,
        away: expectedAway,
        type: 'BoxScore'
      });
    });
  });

  describe('should not match strings and return null', () => {
    it('if there is no score for at lease one innings', () => {
      expect(parser.parse('Team A v Team B')).toEqual(null);
      expect(parser.parse('Team U21 v Team U21')).toEqual(null);
    });
  });

  describe('replaceScores', () => {
    it('should keep ordinal numerals in event name', () => {
      expect(parser.replaceScores('New Zealand v England 1st T20', '')).toEqual('New Zealand v England 1st T20');
      expect(parser.replaceScores('New Zealand v England 2nd T20', '')).toEqual('New Zealand v England 2nd T20');
      expect(parser.replaceScores('New Zealand v England 3rd T20', '')).toEqual('New Zealand v England 3rd T20');
      expect(parser.replaceScores('New Zealand v England 4th T20', '')).toEqual('New Zealand v England 4th T20');
    });
  });
});
