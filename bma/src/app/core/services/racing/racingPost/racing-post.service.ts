import { Injectable } from '@angular/core';
import { RacingPostApiService } from '@coreModule/services/racing/racingPost/racing-post-api.service';
import { ISportEvent, ISportEventNewspaper } from '@core/models/sport-event.model';
import { IOutcome, IRacingPostForm } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import {
  IRacingPostResponse, IRacingPostGHResponse, IRacingPostHRResponse,
  IRacingPostMappingConfig, IRacingPostMapping, IRacingDataHubConfig, IRacingPostHorse
} from '@coreModule/services/racing/racingPost/racing-post.model';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import { Observable, of } from 'rxjs';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { map as observableMap, switchMap } from 'rxjs/operators';
import {
  HORSERACING_MAPPING_CONFIG, GREYHOUND_MAPPING_CONFIG
} from '@core/services/racing/racingPost/racing-post-mapping-config.constant';
import { TimeService } from '@core/services/time/time.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { LocaleService } from '@core/services/locale/locale.service';

@Injectable({
  providedIn: 'root'
})
export class RacingPostService {
  constructor(
    private racingPostApiService: RacingPostApiService,
    private cmsService: CmsService,
    protected timeService: TimeService,
    private toolsService: CoreToolsService,
    private localeService: LocaleService,
  ) {}

  /**
   * getGreyhoundRacingPostById()
   * @param {string} openBetId
   * @returns {Promise<any>}
   */
  getGreyhoundRacingPostById(openBetId: string): Observable<IRacingPostGHResponse> {
    return this.getRacingDataHubConfig().pipe(
      switchMap((config: IRacingDataHubConfig) => config.isEnabledForGreyhound ?
        this.racingPostApiService.getGreyhoundRaceDetails(openBetId) : of({} as IRacingPostGHResponse))
    );
  }

  getHorseRacingPostById(openBetIds: string): Observable<IRacingPostHRResponse> {
    return this.getRacingDataHubConfig().pipe(
      switchMap((config: IRacingDataHubConfig) => config.isEnabledForHorseRacing ?
        this.racingPostApiService.getHorseRaceDetails(openBetIds) : of({} as IRacingPostHRResponse))
    );
  }

  mergeGreyhoundRaceData(eventsData: ISportEvent[], raceData: IRacingPostGHResponse): ISportEvent[] {
    return this.mergeRaceData(eventsData, raceData, GREYHOUND_MAPPING_CONFIG);
  }

  mergeHorseRaceData(eventsData: ISportEvent[], raceData: IRacingPostHRResponse): ISportEvent[] {
    return this.mergeRaceData(eventsData, raceData, HORSERACING_MAPPING_CONFIG);
  }

  getRacingDataHubConfig(): Observable<IRacingDataHubConfig> {
    return this.cmsService.getSystemConfig().pipe(
      observableMap((data: ISystemConfig) => Object.assign({}, data.raceInfo, data.RacingDataHub))
    );
  }

  updateRacingEventsList(eventsData: ISportEvent[], isHorseRasing: boolean = true): Observable<ISportEvent[]> {
    if (!eventsData.length) {
      return of([]);
    }
    const eventIds: string = eventsData.map(item => item.id).join(',');
    return isHorseRasing ?
      this.getHorseRacingPostById(eventIds).pipe(
        observableMap((raceData: IRacingPostHRResponse) => this.mergeHorseRaceData(eventsData, raceData)),
      ) :
      this.getGreyhoundRacingPostById(eventIds).pipe(
        observableMap((raceData: IRacingPostGHResponse) => this.mergeGreyhoundRaceData(eventsData, raceData))
      );
  }

  addRacingFormOutcome<T>(outcome: IOutcome, runnersMap: { [key: string]: T }, keysMap: IRacingPostMapping<T>): void {
    if (outcome.runnerNumber && runnersMap[outcome.runnerNumber]) {
      outcome.racingFormOutcome = this.getValuesByKeysMap(runnersMap[outcome.runnerNumber], keysMap);
    }
  }

  /**
   * To form last run text
   * @param {IRacingPostForm[]} lastRunData
   */
  getLastRunText(lastRunData: IRacingPostForm[]): string {
    let lastRun: IRacingPostForm;
    if (lastRunData && lastRunData.length) {
      lastRun = lastRunData[0] as any;
      const odds = lastRun.odds ? lastRun.odds.replace('/', '-') : '',
        weight = lastRun.weight,
        position = lastRun.position ?
          `${lastRun.position}${this.toolsService.getDaySuffix(lastRun.position)}` : '',
        noOfRunners = lastRun.noOfRunners ? lastRun.noOfRunners : '',
        distanceToWinner = lastRun.distanceToWinner ? lastRun.distanceToWinner : '',
        otherHorseName = lastRun.other ? lastRun.other.horseName : '',
        otherHorseWeight = lastRun.other ? lastRun.other.weight : '',
        raceClass = lastRun.raceClass ? lastRun.raceClass : '',
        month = this.localeService.getString(this.timeService.getMonthI18nValue(new Date(lastRun.date), true)),
        comment = lastRun.comment ? lastRun.comment : '',
        courseName = lastRun.courseName ? lastRun.courseName : '',
        raceTitle = lastRun.raceTitle ? lastRun.raceTitle : '';

      const lastRunText = this.localeService.getString('racing.lastRunText', {
        odds, weight, comment, position, noOfRunners, distanceToWinner,
        otherHorseName, otherHorseWeight, courseName, raceTitle, raceClass, month
      });
      return lastRunText;
    } else {
      return null;
    }
  }

  private mergeRaceData<T, U>(eventsData: ISportEvent[], raceData: IRacingPostResponse<T>,
                        racingFormConfig: IRacingPostMappingConfig<T, U>): ISportEvent[] {
    const eventsDataArray = [].concat(eventsData),
      obEventsMap: { [key: string]: ISportEvent } = eventsDataArray.reduce(this.indexBy('id'), {}),
      rpEventsMap: { [key: string]: T } = raceData && raceData.document || {},
      rpEventIds: string[] = Object.keys(rpEventsMap);

    rpEventIds.forEach((rpEventId: string) => {
      const rpEvent = rpEventsMap[rpEventId],
        obEvent = obEventsMap[rpEventId];

      if (rpEvent && obEvent) {
        const runnersKeys = racingFormConfig.runnersKeys,
          runnersMap: { [key: string]: U } =
            (rpEvent[runnersKeys.runnersPropName] || []).reduce(this.indexBy(runnersKeys.runnerNumberPropName), {});

        if (obEvent.markets) {
          obEvent.markets.forEach((market: IMarket) => {
            if (!market.outcomes) {
              return;
            }
            market.outcomes.forEach((outcome: IOutcome) => {
              this.addRacingFormOutcome(outcome, runnersMap, racingFormConfig.outcomeKeysMap);
            });
          });
        }

        obEvent.racingFormEvent = this.getValuesByKeysMap(rpEvent, racingFormConfig.eventKeysMap);

        if (runnersKeys.runnersPropName === 'horses') {
          obEvent.racingPostVerdict = this.prepareVerdictData(obEvent);
        }
      }
    });
    return eventsDataArray;
  }

  private indexBy<T>(property: keyof T): (map: { [key: string]: T }, item: T) => { [key: string]: T } {
    return (map, item) => { map[String(item[property])] = item; return map; };
  }

  private getValuesByKeysMap<T>(racingPostData, keys: IRacingPostMapping<T>): any {
    return Object.keys(keys).reduce((obj, key) => {
      const data = racingPostData[key];
      if (data !== undefined) {
        obj[keys[key]] = typeof data === 'number' ? data.toString() : data;
      }
      return obj;
    }, {});
  }

  private getSaddleNoBySelectionId(racingFormEvent, rpSelectionUid: number): string {
    if (racingFormEvent && racingFormEvent.horses) {
      const horse = racingFormEvent.horses.find((item: IRacingPostHorse) => item.rpHorseId == rpSelectionUid);
      return horse ? horse.saddle : null;
    }
    return null;
  }

  private prepareVerdictData(eventEntity: ISportEvent): IRacingPostVerdict {
    const data: IRacingPostVerdict = {
      starRatings: [],
      tips: [],
      verdict: '',
      imgUrl: '',
      isFilled: false,
      mostTipped: []
    };
    data.starRatings = eventEntity.markets && eventEntity.markets[0] && eventEntity.markets[0].outcomes ?
      eventEntity.markets[0].outcomes.map(horse => ({
        name: horse.name,
        rating: horse.racingFormOutcome && horse.racingFormOutcome.starRating ? Number(horse.racingFormOutcome.starRating) : 0
      })).filter(item => item.rating > 0) : [];
    data.tips = eventEntity.racingFormEvent.newspapers ? eventEntity.racingFormEvent.newspapers.map(tip => ({
      name: tip.name,
      value: tip.selection,
      rpSelectionUid: tip.rpSelectionUid,
      saddleNo: this.getSaddleNoBySelectionId(eventEntity.racingFormEvent, tip.rpSelectionUid)
    })).filter(item => item.name !== '' && item.value !== '') : [];
    data.verdict = eventEntity.racingFormEvent.overview;
    data.imgUrl = eventEntity.racingFormEvent.courseGraphics;
    data.isFilled = !!((data.verdict && data.verdict.length) || data.starRatings.length || data.tips.length);

    const tippedHorses = [];
    if (eventEntity.racingFormEvent &&
      eventEntity.racingFormEvent.newspapers && eventEntity.racingFormEvent.newspapers.length) {
      const totalNewspapers: ISportEventNewspaper[] = eventEntity.racingFormEvent.newspapers;
      const newspapers: ISportEventNewspaper[] = eventEntity.racingFormEvent.newspapers.slice(0, 3);
      const selections = newspapers.map(newspaper => newspaper.selection);
      selections.forEach((selection: string, index: number) => {
        const selectionNewspapers: ISportEventNewspaper[] = totalNewspapers.filter((newspaper: ISportEventNewspaper) => {
          return (newspaper.selection === selection);
        });
        const tipster = selectionNewspapers.map(tip => tip.name);
        tippedHorses.push({
          name: selection,
          value: tipster.slice(0, 3).join(', '),
          tips: newspapers[index].tips
        });
      });
    }
    const filterdtippedHorses = tippedHorses.filter((newspaper) => {
      return ( newspaper.tips !== undefined );
    });
    data.mostTipped = filterdtippedHorses;
    return data;
  }
}
