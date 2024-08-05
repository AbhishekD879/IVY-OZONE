import { Injectable } from '@angular/core';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import * as _ from 'underscore';
import {
  ICommentaryEventFact,
  ICommentaryEventParticipant,
  ICommentaryEventPeriod,
  ITypedScoreData,
  IScoreType
} from '@core/services/scoreParser/models/score-data.model';
import { ICommentsTeam, IPropertiesForUpdate } from '@core/models/teams.model';
import { ISportEvent, IEventComments } from '@core/models/sport-event.model';
import { ILiveClock } from '@core/models/live-clock.model';

@Injectable()
export class CommentsService {
  basketballInitParse: Function;
  basketballUpdateExtend: Function;
  volleyballUpdateExtend: Function;
  beach_volleyballUpdateExtend: Function;
  handballUpdateExtend: Function;

  footballRoleCode = {
    team_1: 'home',
    team_2: 'away'
  };

  /**
   * Define score type by category id for sports which use comments for live updates
   */
  private categoryCodeScoreTypeMap = {
    BADMINTON: 'SetsPoints',
    VOLLEYBALL: 'SetsPoints',
    HANDBALL: 'Simple',
    BEACH_VOLLEYBALL: 'SetsPoints',
    TENNIS: 'SetsGamesPoints',
    FOOTBALL: 'Simple',
    BASKETBALL: 'Simple',
    DARTS: 'SetsLegs'
  };

  private readonly PENALTIES_PERIOD: string = 'PENALTIES';
  private readonly EXTRA_TIME_PERIODS: Array<string> = ['EXTRA_TIME_FIRST_HALF', 'EXTRA_TIME_SECOND_HALF'];
  private readonly SCORE_FACT: string = 'SCORE';

  constructor(
    private timeSync: TimeSyncService,
    private liveEventClock: LiveEventClockProviderService
  ) {
    /**
     * Context bindings
     * It's needed here because context losses in such functions, like "_.partial(Fn1, Fn2, ...)"
     */
    this.gameInitParse = this.gameInitParse.bind(this);
    this.footballInitParse = this.footballInitParse.bind(this);
    this.footballClockInitParse = this.footballClockInitParse.bind(this);
    this.getCLockData = this.getCLockData.bind(this);
    this.gameUpdateExtend = this.gameUpdateExtend.bind(this);
    this.footballUpdateExtend = this.footballUpdateExtend.bind(this);
    this.badmintonUpdateExtend = this.badmintonUpdateExtend.bind(this);
    this.tennisInitParse = this.tennisInitParse.bind(this);
    this.badmintonMSInitParse = this.badmintonMSInitParse.bind(this);
    this.tennisUpdateExtend = this.tennisUpdateExtend.bind(this);
    this.getCorrectRoleCodeForFoolball = this.getCorrectRoleCodeForFoolball.bind(this);
    this.parseScoresFromName = this.parseScoresFromName.bind(this);
    this.updateSportScores = this.updateSportScores.bind(this);
    /*
    shortCuts for functions:
     */
    this.basketballInitParse = this.gameInitParse;
    this.basketballUpdateExtend = this.gameUpdateExtend;
    this.volleyballUpdateExtend = this.updateSportScores;
    this.beach_volleyballUpdateExtend = this.updateSportScores;
    this.handballUpdateExtend = this.updateSportScores;
  }

  /**
   * Extend event with score info
   * @param {ISportEvent} event
   * @param scoreInfo
   */
  extendWithScoreInfo(event: ISportEvent, scoreInfo): void {
    if (event && scoreInfo) {
      event.scoreType = scoreInfo.scoreType;
      event.comments = {
        teams: scoreInfo.score
      };
    }
  }

  /**
   * Extend event with score type
   * @param {ISportEvent} event
   * @param scoreInfo
   */
  extendWithScoreType(event: ISportEvent, categoryCode: string): void {
    if (event) {
      event.scoreType = event.scoreType ? event.scoreType : this.getScoreTypeByCategory(categoryCode);
    }
  }

  /**
   * Parse initial comments data for football/basketball
   * @param {Object} data - raw comments
   * @returns {Object} parsed comments data
   */
  gameInitParse(data: Array<ICommentaryEventParticipant | ICommentaryEventPeriod>): IEventComments {
    let facts;

    const teams = {};

    _.each(data, obj => {
      if (_.has(obj, 'eventParticipant')) {
        teams[this.getCorrectRoleCodeForFoolball((obj as any).eventParticipant.roleCode)] = (obj as any).eventParticipant;
      } else if (_.has(obj, 'eventPeriod')) {
        facts = (obj as any).eventPeriod.children;
      }
    });

    _.each(facts, fact => {
      if (_.has(fact, 'eventFact')) {
        _.each(teams, team => {
          if ((team as any).id === (fact as any).eventFact.eventParticipantId) {
            team[(fact as any).eventFact.factCode.toLowerCase()] = (fact as any).eventFact.fact;
          }
        });
      }
    });

    return {
      teams
    };
  }

  /**
   * Parse initial comments data for football by using general gameInitParse AND adding scores from extra periods.
   * @param {Array} comments
   * @returns {IEventComments} parsed comments data
   */
  footballInitParse(comments: Array<ICommentaryEventParticipant | ICommentaryEventPeriod>): IEventComments {
    const parsedComments = this.gameInitParse(comments);
    let extraTimeFacts: Array<ICommentaryEventFact> = [];
    let penaltiesFacts: Array<ICommentaryEventFact> = [];

    // main time scores are calculated in gameInitParse, need to add scores from extra time (but without penalties scores),
    // if comments were returned from ss commentary
    _.each(comments, (comment: ICommentaryEventPeriod) => {
      if (this.isEventPeriod(comment)) {
        _.each(comment.eventPeriod.children, (fact: ICommentaryEventPeriod) => {
          if (this.isEventPeriod(fact)) {
            const periodCode = fact.eventPeriod.periodCode;

            if (_.contains(this.EXTRA_TIME_PERIODS, periodCode)) {
              extraTimeFacts = extraTimeFacts.concat(this.parsePeriodFacts(fact));
            } else if (this.PENALTIES_PERIOD === periodCode) {
              penaltiesFacts = this.parsePeriodFacts(fact);
            }
          }
        });
      }
    });

    _.each(parsedComments.teams as Array<ICommentsTeam>, (team: ICommentsTeam) => {
        team.extraTimeScore = '0';
        team.penaltyScore = '0';

      _.each(extraTimeFacts, (fact: ICommentaryEventFact) => {
        if (team.id === fact.eventFact.eventParticipantId) {
          team.score = this.increaseScoreByFact(team.score, fact);
          team.extraTimeScore = this.increaseScoreByFact(team.extraTimeScore, fact);
        }
      });

      _.each(penaltiesFacts, (fact: ICommentaryEventFact) => {
        if (team.id === fact.eventFact.eventParticipantId) {
          team.penaltyScore = this.increaseScoreByFact(team.penaltyScore, fact);
        }
      });
    });

    return parsedComments;
  }

  /**
   * Parse initial comments clock data for football
   * @param {Object} data - raw comments
   * @param {Object} eventCategoryCode
   * @param {Object} eventStartTime
   * @param {Object} responseCreationTime
   * @returns {Object} parsed comments data
   */

  // TODO looks like this method is useless
  footballClockInitParse(data, eventCategoryCode, eventStartTime, responseCreationTime) {
    let clockData = null;
    const serverTimeDelta = this.timeSync.getTimeDelta();

    _.each(data, obj => {
      if (_.has(obj, 'eventPeriod')) {
        const childEventPeriods = (obj as any).eventPeriod.children.filter(childEventPeriod => {
          return _.has(childEventPeriod, 'eventPeriod');
        });

        if (childEventPeriods.length) {
          const latestPeriod = _.sortBy(childEventPeriods, period => {
            return (period as any).eventPeriod.startTime;
          })[childEventPeriods.length - 1]['eventPeriod'];

          // TODO move this initialisation to liveClock directive
          const clockInitialData: ILiveClock = this.getCLockData(_.extend(
            { startTime: (obj as any).eventPeriod.startTime },
            latestPeriod,
            {
              startTime: eventStartTime,
              sport: eventCategoryCode,
              ev_id: latestPeriod.eventId
            },
            { responseCreationTime }
          ));

          clockData = { clock: this.liveEventClock.create(
              serverTimeDelta,
              clockInitialData
            )
          };
        }
      }
    });

    return clockData;
  }

  getCLockData(period): ILiveClock {
    const periodClockState = period.children.filter(childEventPeriod => {
        return _.has(childEventPeriod, 'eventPeriodClockState');
      })[0].eventPeriodClockState,
      creationTime = new Date(period.responseCreationTime),
      periodClockStateLastUpdate = new Date(periodClockState.lastUpdate),
      deltaSeconds = Math.abs(Math.floor(((creationTime as any) - (periodClockStateLastUpdate as any)) / 1000));

    return {
      ev_id: Number(period.eventId),
      last_update: periodClockState.lastUpdate,
      period_code: period.periodCode,
      period_index: '',
      state: periodClockState.state,
      clock_seconds: periodClockState.offset,
      last_update_secs: (new Date(periodClockState.lastUpdate).getTime() / 1000).toString(),
      start_time_secs: (new Date(period.startTime).getTime() / 1000).toString(),
      offset_secs: (parseInt(periodClockState.offset, 10) + deltaSeconds).toString(),
      sport: null,
    };
  }

  /**
   * Parse LiveServ update comments data for football/basketball and extend original event with them
   * @param {Object} comments - event parsed comments
   * @param {Object} data - raw comments data
   * @returns {Object} extended event
   */
  gameUpdateExtend(comments, data) {
    _.each(data.ALL, obj => {
      const team = comments.teams[this.getCorrectRoleCodeForFoolball((obj as any).role_code)];

      if ((obj as any).code === 'SCORE' && Number(team.eventId) === Number((obj as any).ev_id)) {
        team.score = (obj as any).value;
      }
    });
  }

  /**
   * Parse LiveServ update comments data for football and extend original event with them
   * @param {Object} comments - event parsed comments
   * @param {Object} data - raw comments data
   * @returns {Object} extended event
   */
  footballUpdateExtend(comments, data) {
    // SUBPERIOD exists in comments only for Coral, when scores are fetched from commentary
    // for Ladbrokes SUBPERIOD could come but be an empty array
    //
    // In other case (when score is parsed from event name) only ALL is available,
    // so we can use generic method updateSportScores for score update
    if (data.SUBPERIOD && data.SUBPERIOD.length) {
      // reset teams scores before re calculate.
      this.resetTeamsScores(comments);

      // calculate scores for all game periods. "main time" + "extra time"
      // but without penaties scores
      _.each(data.SUBPERIOD, periodData => {
        const team = comments.teams[this.getCorrectRoleCodeForFoolball((periodData as any).role_code)];

        if ((periodData as any).period_code === this.PENALTIES_PERIOD) {
          team.penaltyScore = +(periodData as any).value;

          return;
        }

        if (team.score) {
          team.score = parseInt(team.score, 10) + parseInt((periodData as any).value, 10);
        } else {
          team.score = parseInt((periodData as any).value, 10);
        }
      });
    } else {
      /**
       * BMA-57849 - Ladbrokes scores on featured/eventHub inplay have different updates
       * for scores for some football events (events duration 8 or 12 min - eFootball in most cases).
       * They do have only ALL period and role_code = "TEAM_1" and "TEAM_2". Converting this values to
       * role_code = "home" and "away" as in codeblock above - for regular football matches with correct
       * periods - ALL, CURRENT, SUBPERIOD.
       */
      data.ALL.forEach(team => {
        team.role_code = this.getCorrectRoleCodeForFoolball(team.role_code);
      });
      this.updateSportScores(comments, data);
    }
  }

  /**
   * Reset teams scores before re calculate
   * @param {Object} comments - event parsed comments
   */
  resetTeamsScores(comments) {
    if (comments.teams.away) {
      comments.teams.away.score = 0;
    }

    if (comments.teams.home) {
      comments.teams.home.score = 0;
    }
  }

  /**
   * Parse LiveServ update comments data for badminton and extend original event with them
   * @param {Object} comments - event parsed comments
   * @param {Object} data - raw comments data
   */
  badmintonUpdateExtend(comments, data) {
    const home = 'player_1';
    const away = 'player_2';

    if (comments.teams.home && comments.teams.away) {
      comments.teams.home.score = data.ALL[0].value;
      comments.teams.away.score = data.ALL[1].value;
      if (data.CURRENT && data.CURRENT.length) {
        comments.teams.home.currentPoints = data.CURRENT[0].value;
        comments.teams.home.isActive = this.isScoreboardTeamActive(data.CURRENT[0]);
        comments.teams.away.currentPoints = data.CURRENT[1].value;
        comments.teams.away.isActive = this.isScoreboardTeamActive(data.CURRENT[1]);
      } else if (data.SUBPERIOD && data.SUBPERIOD.length) {
        const subperiod = data.SUBPERIOD.slice(data.SUBPERIOD.length - 2);
        comments.teams.home.currentPoints = subperiod[0].value;
        comments.teams.away.currentPoints = subperiod[1].value;
      }
    }

    if (comments.teams[home] && comments.teams[away]) {
      comments.teams[home].score = data.ALL[0].value;
      comments.teams[away].score = data.ALL[1].value;

      if (data.CURRENT && data.CURRENT.length) {
        comments.teams[home].currentPoints = data.CURRENT[0].value;
        comments.teams[home].isActive = this.isScoreboardTeamActive(data.CURRENT[0]);
        comments.teams[away].currentPoints = data.CURRENT[1].value;
        comments.teams[away].isActive = this.isScoreboardTeamActive(data.CURRENT[1]);
      } else if (data.SUBPERIOD && data.SUBPERIOD.length) {
        const subperiod = data.SUBPERIOD.slice(data.SUBPERIOD.length - 2);
        comments.teams[home].currentPoints = subperiod[0].value;
        comments.teams[away].currentPoints = subperiod[1].value;
      }
    }
  }

  /**
   * Parse initial comments data for tennis
   * @param {Object} data - raw comments
   * @returns {Object} parsed comments data
   */
  tennisInitParse(data) {
    const teamsAndMainFacts = this.getTeamsAndMainFacts(data),
      setScoresAndRunningSetIndex = this.getSetScoresAndRunningSetIndex(teamsAndMainFacts.facts);

    return {
      teams: teamsAndMainFacts.teams,
      setsScores: setScoresAndRunningSetIndex.setScores,
      runningSetIndex: setScoresAndRunningSetIndex.runningSetIndex,
      runningGameScores: this.getRunningGameScores(teamsAndMainFacts.facts, setScoresAndRunningSetIndex.runningSetIndex)
    };
  }

  /**
   * Parse initial comments data for badminton(events received from in-play/featured MS)
   * @param {Object} data - raw comments
   * @returns {Object} parsed comments data
   */
  badmintonMSInitParse(data) {
    const badmintonRoleCode = {
        player_1: 'home',
        player_2: 'away'
      },
      teams = {},
      isRunningSetData = data.runningSetIndex && data.setsScores[data.runningSetIndex],
      points = isRunningSetData ? data.setsScores[data.runningSetIndex] : data.setsScores[1];

    _.each(data.teams, (element, key) => {
      // adapt badminton comments to common format(volleyball, beach volleyball, handball, badminton)
      teams[badmintonRoleCode[key]] = {
        id: (element as any).id,
        score: (element as any).score,
        currentPoints: points[(element as any).id],
        name: (element as any).name,
        isActive: (element as any).isActive,
      };
    });

    return _.extend(data.teams, teams);
  }

  /**
   * Transform scores parsed from Tennis event name to comments format
   * @param {TypedScoreData} fallbackScores scores parsed by scores from name parser
   * @returns {IEventComments} scores in comments format
   */
  public tennisTransformFallback(fallbackScores: ITypedScoreData): IEventComments {
    return {
      runningSetIndex: 1,
      setsScores: {
        1: {
          '1': fallbackScores.home.periodScore,
          '2': fallbackScores.away.periodScore,
        }
      } as any,
      runningGameScores: {
        '1': fallbackScores.home.currentPoints,
        '2': fallbackScores.away.currentPoints,
      },
      teams: {
        player_1: {
          id: '1',
          score: fallbackScores.home.score,
          isActive: fallbackScores.home.isServing,
        },
        player_2: {
          id: '2',
          score: fallbackScores.away.score,
          isActive: fallbackScores.away.isServing,
        }
      }
    };
  }

  /**
   * @param {Object} comments - event parsed comments
   * @param {Object} data - raw comments data
   * @returns {Object} extended event
   */
  tennisUpdateExtend(comments, data) {
    const players = ['player_1', 'player_2'];
    const ids = players.map(item => comments.teams[item] ? comments.teams[item].id : '' );
    if (comments) {
      if (data.ALL) {
        data.ALL.forEach((item, ind) =>  {
          if (comments.teams[players[ind]]) {
            comments.teams[players[ind]].score = item.value;
          }
        });
      }
      const setId = comments.runningSetIndex || 1;

      if (data.SUBPERIOD) {
        const subperiod = data.SUBPERIOD.slice(data.SUBPERIOD.length - 2);

        subperiod.forEach((item, ind) => {
          if (ids[ind]) {
            comments.setsScores = !comments.setsScores ? {} : comments.setsScores;
            comments.setsScores[setId] = (comments.setsScores && comments.setsScores[setId]) || {};
            comments.setsScores[setId][ids[ind]] = item.value;
          }
        });
      }
      if (data.CURRENT) {
        data.CURRENT.forEach((item, ind) => {
          if (ids[ind] && comments.runningGameScores) {
            const key = ids[ind];
            comments.runningGameScores[key] = item.value;
          }
          if (comments.teams[players[ind]]) {
            comments.teams[players[ind]].isActive = this.isScoreboardTeamActive(item);
          }
        });
      }
    }
  }

  /**
   * Get correct role code - normalize role code for production and stage
   *
   * @param code {string}
   * @returns {*|string}
   */
  getCorrectRoleCodeForFoolball(code) {
    return this.footballRoleCode[code.toLowerCase()] || code.toLowerCase();
  }

  /**
   * Parse sport scores(and sets for some sports) from event name(example: "(0) 1-1 (1)" or "1-4")
   * @param eventName
   * @returns {Object}
   */
  parseScoresFromName(eventName) {
    const score = eventName.en ? eventName.en : eventName,
      parts = score.match(/(\((\d+)\))?\s?(\d+)-(\d+)\s?(\((\d+)\))?/g),
      teams = score.replace(/\s\(?(\d+)?\)?\s?(\d+)-(\d+)\s?\(?(\d+)?\)?\s?/g, ' v '),
      names = teams.split(' v ');

    if (!score || !parts || names.length < 2) {
      return null;
    }

    const sets = parts[0].match(/\(\d+\)/g),
      currentPoints = sets && parts[0].match(/(\d+)-(\d+)/g)[0].split('-'),
      scores = currentPoints ? sets : parts[0].trim().split('-');

    const homeIsServing = names.length && /\*/.test(names[0]);
    const awayIsServing = names.length && /\*/.test(names[1]);

    return {
      home: {
        isServing: homeIsServing,
        name: names.length && names[0].replace(/\*|\s*\([^)]\BG\)\s*/g, ''),
        score: sets ? scores[0].replace(/\(|\)/g, '') : scores[0],
        currentPoints: currentPoints && currentPoints[0]
      },
      away: {
        isServing: awayIsServing,
        name: names.length && names[1].replace(/\*|\s*\([^)]\BG\)\s*/g, ''),
        score: sets ? scores[1].replace(/\(|\)/g, '') : scores[1],
        currentPoints: currentPoints && currentPoints[1]
      }
    };
  }

  /**
   * Parse sport scores(and sets for some sports) from LiveServ MS SCBRD and update comments
   * @param comments - event's comments which need to update
   * @param scoreboardData - object with new comments data
   */
  updateSportScores(comments, scoreboardData) {
    const teams = {};
    if (scoreboardData.CURRENT) {
      _.each(scoreboardData.CURRENT, obj => {
        teams[(obj as any).role_code.toLowerCase()] = {
          currentPoints: (obj as any).value,
          isActive: this.isScoreboardTeamActive(obj)
        };
      });
    }

    _.each(scoreboardData.ALL, obj => {
      const roleCode = (obj as any).role_code.toLowerCase();

      if (_.has(teams, roleCode)) {
        teams[roleCode].score = (obj as any).value;
      } else {
        teams[roleCode] = { score: (obj as any).value };
      }
    });

    this.sportUpdateExtend(comments, teams);
  }

  /**
   * Parse LiveServ update comments data for sports(Handball, Volleyball, Beach Volleyball) and extend original event with them
   * @param {Object} comments - event parsed comments
   * @param {Object} scores - raw comments data
   * @returns {Object} extended event
   */
  sportUpdateExtend(comments, scores): void {
    if (comments.teams.player_1 && scores.type === 'SetsGamesPoints') {
      // Tennis scores from event names
      Object.assign(comments, this.tennisTransformFallback(scores));
      return;
    }

    const propertiesForUpdate: IPropertiesForUpdate[] = [
      { name: 'score', updateHard: true },
      { name: 'currentPoints', updateHard: false },
      { name: 'periodScore', updateHard: false },
      { name: 'isServing', updateHard: true },
      { name: 'isActive', updateHard: true },
      { name: 'inn1', updateHard: false },
      { name: 'inn2', updateHard: false },
    ];

    propertiesForUpdate.forEach((prop: IPropertiesForUpdate) => {
      const { name, updateHard } = prop;
      if (!scores.home || (!updateHard && !scores.home.hasOwnProperty(name))) {
        return;
      }

      try {
        comments.teams.home[name] = scores.home[name];
        comments.teams.away[name] = scores.away[name];
      } catch (e) {
        console.warn('wrong comments data feed format');
      }
    });
  }

  /**
   * Private methods
   */

  /**
   * Get score type by sport category code
   * Useful for sport events which receive live updates by comments
   * @param {string} categoryCode - sport category code
   * @returns {IScoreType | null}
   */
  private getScoreTypeByCategory(categoryCode: string): IScoreType | null {
    return (categoryCode && this.categoryCodeScoreTypeMap[categoryCode]) || null;
  }

  private getTeamsAndMainFacts(subData) {
    let facts;

    const teams = {};

    _.each(subData, commentsElement => {
      if ((commentsElement as any).eventParticipant) {
        if (_.has((commentsElement as any).eventParticipant, 'roleCode')) {
          teams[(commentsElement as any).eventParticipant.roleCode.toLowerCase()] = (commentsElement as any).eventParticipant;
        }
      } else if (_.has(commentsElement, 'eventPeriod')) {
        facts = (commentsElement as any).eventPeriod.children;
      }
    });

    return { facts, teams };
  }

  private getSetScoresAndRunningSetIndex(facts) {
    const setScores = {};

    let runningSetIndex = 0;

    // Loop through sets to get set scores and identify last set
    _.each(facts, periodAllElement => {
      if ((periodAllElement as any).eventPeriod && (periodAllElement as any).eventPeriod.periodCode === 'SET') {
        const setIndex = parseInt((periodAllElement as any).eventPeriod.periodIndex, 10);

        setScores[setIndex] = {};

        _.each((periodAllElement as any).eventPeriod.children, obj => {
          // Get score for set
          if ((obj as any).eventFact && (obj as any).eventFact.factCode === 'SCORE') {
            setScores[setIndex][(obj as any).eventFact.eventParticipantId] = (obj as any).eventFact.fact;
          }

          if (setIndex > runningSetIndex) {
            runningSetIndex = setIndex;
          }
        });
      }
    });

    return { setScores, runningSetIndex };
  }

  private getRunningGameScores(facts, runningSetIndex) {
    const runningGameScores = {};

    // Loop through sets to get last game scores from last set
    _.each(facts, periodAllElement => {
      if ((periodAllElement as any).eventPeriod && (periodAllElement as any).eventPeriod.periodCode === 'SET') {
        const setIndex = parseInt((periodAllElement as any).eventPeriod.periodIndex, 10);

        // If set is currently running get last game scores
        if (runningSetIndex === setIndex) {
          _.each(this.getLastGame((periodAllElement as any).eventPeriod.children), obj => {
            // Get score for game
            if ((obj as any).eventFact && (obj as any).eventFact.factCode === 'SCORE') {
              runningGameScores[(obj as any).eventFact.eventParticipantId] = (obj as any).eventFact.fact;
            }
          });
        }
      }
    });

    return runningGameScores;
  }

  /**
   * Get last game object
   * @param {Object} facts
   * @returns {Object} last game
   */
  private getLastGame(facts) {
    const games = {};

    let lastGameIndex = 0;

    _.each(facts, obj => {
      if ((obj as any).eventPeriod && (obj as any).eventPeriod.periodCode === 'GAME') {
        const index = parseInt((obj as any).eventPeriod.periodIndex, 10);

        if (index > lastGameIndex) {
          lastGameIndex = index;
        }
        games[(obj as any).eventPeriod.periodIndex] = (obj as any).eventPeriod.children;
      }
    });

    return games[lastGameIndex.toString()];
  }

  /**
   * Checks if commentary period is of "eventPeriod" type
   * @param {ICommentaryEventPeriod} period
   * @return {boolean}
   */
  private isEventPeriod(period: ICommentaryEventPeriod): boolean {
    return period.hasOwnProperty('eventPeriod');
  }

  /**
   * Parses commentary perid facts to gather score changing periods.
   * @param {ICommentaryEventPeriod} period
   * @return {Array<ICommentaryEventFact>}
   */
  private parsePeriodFacts(period: ICommentaryEventPeriod): Array<ICommentaryEventFact> {
    const facts: Array<ICommentaryEventFact> = [];

    _.each(period.eventPeriod.children, (periodFact: ICommentaryEventFact) => {
      if (periodFact.hasOwnProperty('eventFact') && periodFact.eventFact.factCode === this.SCORE_FACT) {
        facts.push(periodFact);
      }
    });

    return facts;
  }

  /**
   * Increases score by given commentary fact amount.
   * @param {string} score
   * @param {ICommentaryEventFact} fact
   * @return {string}
   */
  private increaseScoreByFact(score: string, fact: ICommentaryEventFact): string {
    const resultScore = Number(score) + Number(fact.eventFact.fact);

    return `${resultScore}`;
  }

  /**
   * Checks if team is active
   * @param {Partial<is_active: string>} item
   * @return {boolean}
   */
  private isScoreboardTeamActive(item: Partial<{is_active: string}>): boolean {
    return item.is_active === 'Y' || item.is_active === 'true';
  }
}
