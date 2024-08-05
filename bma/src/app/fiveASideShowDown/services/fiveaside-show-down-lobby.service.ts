import { Injectable } from '@angular/core';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import {
  BuildEventsWithScoresAndClockBsService
} from '@app/betHistory/services/cashoutDataProvider/builders/build-events-with-scores-and-clock-bs.service';
import { IPayload } from '@app/core/models/live-serve-update.model';
import { ISportEventEntity } from '@app/core/models/sport-event-entity.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { BuildUtilityService } from '@app/core/services/buildUtility/build-utility.service';
import { CommentsService } from '@app/core/services/comments/comments.service';
import { SiteServerRequestHelperService } from '@app/core/services/siteServerRequestHelper/site-server-request-helper.service';
import { TimeService } from '@app/core/services/time/time.service';
import { IShowdownCard, IShowdownCardDetails, IShowdownCardSignPostings } from '@app/fiveASideShowDown/models/showdown-card.model';
import { LoadByPortionsService } from '@app/ss/services/load-by-portions.service';
import {
  from as observableFrom,
  Observable
} from 'rxjs';
import { map } from 'rxjs/operators';
import { PRIORITY_SIGNPOSTINGS, SHOWDOWN_CARDS } from '@app/fiveASideShowDown/constants/constants';
import { LocaleService } from '@app/core/services/locale/locale.service';
import environment from '@environment/oxygenEnvConfig';
import { IShowdownLobbyContest, LobbyData, IShowdownLobbyResponse } from '@app/fiveASideShowDown/models/showdown-lobby-contest.model';
import { HttpClient } from '@angular/common/http';
import { IPrizePool } from '@app/core/services/cms/models/contest';
import { IEventDetails } from '../models/show-down';

/**
 * Service to handle Showdown lobby and cards
 */
@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveASideShowDownLobbyService {
  private showAnimation: boolean = false;
  private readonly SHOWDOWN_URL = environment.SHOWDOWN_MS;

  constructor(
    private loadByPortionsService: LoadByPortionsService,
    private ssRequestHelperService: SiteServerRequestHelperService,
    private commentsService: CommentsService,
    private buildUtility: BuildUtilityService,
    private timeService: TimeService,
    private buildEventsWithScoresAndClockBsService: BuildEventsWithScoresAndClockBsService,
    private localeService: LocaleService,
    private http: HttpClient
  ) { }

  get loadAnimation() {
    return this.showAnimation;
  }
  set loadAnimation(value: boolean) {
    this.showAnimation = value;
  }
  /**
   * Add and build scores and clock object to events.
   * @param  {ISportEvent[]} events
   * @returns void
   */
  addScoresAndClockForEvents(events: ISportEvent[]): void {
    events.forEach((event: ISportEvent, index: number) => {
      const eventEntity: ISportEventEntity = { 'event': event };
      events[index] = this.buildUtility.eventBuilder(eventEntity);
    });
    this.buildEventsWithScoresAndClockBsService.build({ events, comments: this.getCommentaryFromEvent(events) });
  }

  /**
   * Return event commentary objects for eventIds and build scores and clock
   * @param  {number[]} events
   * @returns {Observable<ISportEvent[]>}
   */
  addScoresAndClock(events: number[]): Observable<ISportEvent[]> {
    return this.getCommentsByEventIds(events).pipe(
      map(result => {
        const data = { events: result.events, comments: result.comments };
        return this.buildEventsWithScoresAndClockBsService.build(data);
      }));
  }

  /**
   * Update current event score comments with liveserve payload
   * @param  {IPayload} payload
   * @param  {ISportEvent} event
   * @returns void
   */
  eventCommentsUpdate(payload: IPayload, event: ISportEvent): void {
    const methodName = `${event.categoryCode.toLowerCase()}UpdateExtend`;
    const extender = this.commentsService[methodName];

    if (event.comments && extender) {
      extender(event.comments, payload);
      this.commentsService.extendWithScoreType(event, event.categoryCode);
    }
  }

  /**
   * Returns ShowdownCard signostings priority object based on contest rules and object
   * @param  {IShowdownCard} contest
   * @returns {IShowdownCardSignPostings}
   */
  signPostingsPriority(contest: IShowdownCard): IShowdownCardSignPostings {
    const prioritySignPostings: IShowdownCardSignPostings = { ...PRIORITY_SIGNPOSTINGS };
    let signPostingsCount = 0;
    const signPostingkeys = Object.keys(prioritySignPostings);
    signPostingkeys.forEach((signPost: string) => {
      if (contest && signPostingsCount < 3) {
        if (this.checkSignPostingExistsInContest(contest, signPost)) {
          prioritySignPostings[signPost] = true;
          signPostingsCount++;
        }
      }
    });

    return prioritySignPostings;
  }

  /**
   * Set Event dateTime and countdown timer based on event status and start date
   * @param  {ISportEvent} event
   * @returns void
   */
  setEventStateByStartDate(event: IEventDetails, categoryName?: string, isMatchFullTime?: boolean): void {
    if (event && event.startTime) {
      const eventStartDate = new Date(event.startTime).getTime();
      const currentDate = new Date().getTime();
      const diffSeconds = Math.floor((eventStartDate - currentDate) / 1000);
      if (!event.started && diffSeconds > 0) {
        event.dateTime = this.timeService.formatByPattern(new Date(event.startTime), 'HH:mm');
      } else if (event.regularTimeFinished
        || (categoryName === SHOWDOWN_CARDS.LAST_7_DAYS && isMatchFullTime)) {
        event.dateTime = this.timeService.getOnlyFullDateFormatSuffix(new Date(event.startTime));
      } else {
        event.dateTime = this.timeService.formatByPattern(new Date(event.startTime), 'HH:mm');
      }
    }
  }

  /**
   * Set Showdown card contest display data based on input contest details
   * @param  {IShowdownCard} contestData
   * @returns {IShowdownCardDetails}
   */
  setContestSignPosting(contestData: IShowdownCard): IShowdownCardDetails {
    const contestDetails: IShowdownCardDetails = {
      entryStake: this.getContestProperty(contestData, 'entryStake', SHOWDOWN_CARDS.POUND_ENTRY),
      totalPrizes: this.getPrizePoolProperty(contestData.prizePool, 'cash', SHOWDOWN_CARDS.POUND),
      prizePoolSummary: this.getPrizePoolProperty(contestData.prizePool, 'summary', SHOWDOWN_CARDS.SUMMARY),
      contestSize: this.getContestProperty(contestData, 'size', SHOWDOWN_CARDS.SIZE),
      prizePoolTotalPrizes: this.getPrizePoolProperty(contestData.prizePool, 'totalPrizes', SHOWDOWN_CARDS.TOTAL_PRIZES),
      teamsEntries: this.getContestProperty(contestData, 'teams', SHOWDOWN_CARDS.ENTRIES),
      firstPlace: this.getPrizePoolProperty(contestData.prizePool, 'firstPlace', SHOWDOWN_CARDS.TOFIRST),
      vouchers: this.getPrizePoolProperty(contestData.prizePool, 'vouchers', SHOWDOWN_CARDS.VOUCHERS),
      tickets: this.getPrizePoolProperty(contestData.prizePool, 'tickets', SHOWDOWN_CARDS.TICKETS),
      freeBets: this.getPrizePoolProperty(contestData.prizePool, 'freeBets', SHOWDOWN_CARDS.FREEBETS)
    };
    return contestDetails;
  }

  /**
   * Fetch Home team and Away team names from event
   * @param  {ISportEvent} event
   * @returns  [key: string]: string
   */
  getTeamNameFromEventComments(event: IEventDetails): { [key: string]: string } {
    let homeTeam: string, awayTeam: string;
    if(event && event.name) { 
      const eventName: string = event.name.replace(/[|,]/g, '');
      [homeTeam, awayTeam] = eventName.split(/ v | vs | - /);
    }
    return { homeTeam, awayTeam };
  }

  /**
   * Get All Showdown contest to display in lobby
   * @param  {string} brand
   * @param  {string} userName
   * @returns Observable
   */
  getAllShowdownContests(brand: string, userName: string, bppToken: string): Observable<IShowdownLobbyResponse> {
    const timeZoneOffset = new Date().getTimezoneOffset();
    const lobbyObj: LobbyData = {
      brand: brand,
      userId: userName,
      offSet: timeZoneOffset,
      token: bppToken
    };
    const LOBYY_CONTESTS_URL = `${environment.SHOWDOWN_MS}/${brand}/lobby`;
    return this.http.post<IShowdownLobbyResponse>(LOBYY_CONTESTS_URL, lobbyObj);
  }

  /**
   * Remove resulted contests from Category
   * @param  {IShowdownLobbyContest[]} displayContests
   * @param  {number} eventId
   * @returns void
   */
  removeResultedContestsFromCategory(displayContests: IShowdownLobbyContest[], eventId: number): void {
    if (displayContests) {
      displayContests.forEach((contest: IShowdownLobbyContest) => {
        const contestEvents = contest.contests;
        if (contestEvents && (contest.category === SHOWDOWN_CARDS.MYSHOWDOWNS || contest.categoryName === SHOWDOWN_CARDS.TODAY)) {
          const filteredEvents = contestEvents.filter((contestData: IShowdownCard) => Number(contestData.eventDetails.id) !== eventId);
          this.pushContestToLast7days(contestEvents, displayContests, eventId);
          contest.contests = [...filteredEvents];
          if (contest.category === SHOWDOWN_CARDS.MYSHOWDOWNS) {
            contest.categoryName = `${SHOWDOWN_CARDS.MY_LEADERBOARDS}${contest.contests.length}${')'}`;
          }
        }
      });
    }
  }

  /**
   * To check if the value is valid and not empty
   * @param  {number|string} value
   * @returns boolean
   */
  isValidValue(value: number | string): boolean {
    return !(value === undefined || value === null || value === '');
  }

  /**
   * Push Completed contest to Last 7 Days section
   * @param  {IShowdownCard[]} contestEvents
   * @param  {IShowdownLobbyContest[]} displayContests
   * @param  {number} eventId
   * @returns void
   */
  private pushContestToLast7days(contestEvents: IShowdownCard[], displayContests: IShowdownLobbyContest[], eventId: number): void {
    const toBePushedEvents = contestEvents.filter((contestData: IShowdownCard) => Number(contestData.eventDetails.id) === eventId);
    const last7daysIndex = displayContests
      .findIndex((section: IShowdownLobbyContest) => section.category === SHOWDOWN_CARDS.LAST7DAYS);
    if (last7daysIndex > -1 && toBePushedEvents) {
      const last7daysList = displayContests[last7daysIndex].contests;
      const contestNotExists = last7daysList.findIndex((contestData: IShowdownCard) => Number(contestData.eventDetails.id) === eventId) === -1;
      if (contestNotExists) {
        displayContests[last7daysIndex].contests.unshift(...toBePushedEvents);
      }
    }
  }

  /**
   * Returns signposting string with prizePool
   * @param  {IPrizePool} prizePool
   * @param  {string} property
   * @param  {string} lang
   * @returns string
   */
  private getPrizePoolProperty(prizePool: IPrizePool, property: string, lang: string): string {
    if (prizePool && prizePool[property]) {
      return this.localeService.getString(`fs.card.${lang}`, [prizePool[property]]);
    }
    return '';
  }

  /**
   * Build comments from events array and returns {eventId, comments} map.
   * @param  {ISportEvent[]} events
   * @returns { [key: string]: any[] }
   */
  private getCommentaryFromEvent(events: ISportEvent[]): { [key: string]: any[] } {
    const filteredEvents: Array<Array<number | any>> = events.filter(
      (event => event.children && event.children.length)
    ).map((item: ISportEvent) => {
      this.removeNullKeysFromEvent(item.children);
      return [item.id, item.children];
    }
    );
    return this.buildEventMapFromArray(filteredEvents);
  }

  /**
   * Remove null keys from the Events commentary
   * @param  {any[]} commentary
   * @returns void
   */
  private removeNullKeysFromEvent(commentary: any[]): void {
    commentary.forEach((item: any) => {
      Object.keys(item).forEach((k) => item[k] == null && delete item[k]);
    });
  }

  /**
   * Convert eventId and comments array to map. i.e {1 : [], 2 : []}
   * @param  {Array<Array<number|any>>|number} events
   * @returns { [key: string]: any[] }
   */
  private buildEventMapFromArray(events: Array<Array<number | any>> | number): { [key: string]: any[] } {
    const eventMap: { [key: string]: any[] } = {};
    if (Array.isArray(events)) {
      events.forEach((item: Array<number | any>) => {
        if (item) {
          const [eventId, comments] = item;
          if (eventId && comments) {
            eventMap[eventId] = comments;
          }
        }
      });
    }
    return eventMap;
  }

  /**
   * Returns comments for given eventIds
   * @param  {number[]} eventsIds
   * @returns {Observable<{ events: Array<ISportEvent>, comments: { [key: string]: any[] } }>}
   */
  private getCommentsByEventIds(eventsIds: number[]): Observable<{ events: Array<ISportEvent>, comments: { [key: string]: any[] } }> {
    const request = this.ssRequestHelperService.getCommentsByEventsIds.bind(this.ssRequestHelperService);
    return observableFrom(
      this.loadByPortionsService.get(request, {}, 'eventsIds', eventsIds)
    ).pipe(
      map((result: Array<ISportEventEntity>) => {
        return {
          events: result && result.map((data: { event: ISportEvent }) => {
            const eventEntity: ISportEventEntity = { event: data.event };
            return this.buildUtility.eventBuilder(eventEntity);
          }),
          comments: result && this.buildEventMapFromArray(result.filter(
            ((eventEntity: ISportEventEntity) => eventEntity.event.children)
          ).map((eventEntity: ISportEventEntity) => [eventEntity.event.id, eventEntity.event]))
        };
      }));
  }

  /**
   * Check whether signPost exists in contest based on priority
   * @param  {IShowdownCard} contest
   * @param  {string} signPost
   * @returns boolean
   */
  private checkSignPostingExistsInContest(contest: IShowdownCard, signPost: string): boolean {
    return !!signPost && (!['size', 'teams'].includes(signPost) && (contest.prizePool?.[signPost]) ||
      (contest[signPost]));
  }

  /**
   * Returns signposting string with contestData
   * @param  {IShowdownCard} contestData
   * @param  {string} property
   * @param  {string} lang
   * @returns string
   */
  private getContestProperty(contestData: IShowdownCard, property: string, lang: string): string {
    if (contestData[property]) {
      if (property === 'size' && this.isValidValue(contestData.contestSize)) {
        return this.localeService
          .getString(`fs.card.${SHOWDOWN_CARDS.CONTEST_SIZE}`, [contestData['contestSize'], contestData[property]]);
      }
      return this.localeService.getString(`fs.card.${lang}`, [contestData[property]]);
    }
    return '';
  }

}
