import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';
import { ITimeFormEntry } from '@core/models/time-form-entry.model';
import { ITimeFormData } from '@core/models/time-form-data.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { TimeFormApiService } from './time-form-api.service';


@Injectable()
export class TimeFormService {

  private readonly RACE_SUMMARY_KEYS = ['raceDistance', 'raceGradeName', 'verdict'];
  private readonly GREYHOUND_SUMMARY_KEYS = ['greyHoundFullName', 'trainerFullName', 'oneLineComment',
                                     'positionPrediction', 'form', 'starRating', 'statusName', 'entryId'];
  private readonly NON_RUNNER_STATUS = 'Non-Runner';

  constructor(
    private timeFormApiService: TimeFormApiService
  ) { }

  /**
   * getGreyhoundRaceById()
   * @param {string} openBetId
   * @returns {Promise<any>}
   */
  getGreyhoundRaceById(openBetId: string): Observable<ITimeFormData> {
    return this.timeFormApiService.getGreyhoundRaceDetails(openBetId);
  }

  /**
   * mergeGreyhoundRaceData()
   * @param {any[]} eventData
   * @returns {any[]}
   */
  mergeGreyhoundRaceData([obData, timeformData]: [ISportEvent, ITimeFormData]): ISportEvent[] {
    if (_.isObject(obData) && _.isObject(timeformData)) {
      const greyhoundsMap = this.getTimeformGreyhoundsMap(timeformData.entries),
        selections = this.getEventSelections(obData.markets),
        positions = this.getPositionsPrediction(greyhoundsMap);

      _.each(selections, (selection: IOutcome) => {
        const greyhound = greyhoundsMap[selection.id];
        if (greyhound) {
          selection.timeformData = greyhound;
        }
      });

      obData.timeformData = _.extend({
        positions,
        winnerPrediction: positions[0]
      }, _.pick(timeformData, this.RACE_SUMMARY_KEYS));
    }

    return _.isObject(obData) ? [obData] : [];
  }

  /**
   * getEventSelections()
   * @param {IMarket[]} markets
   * @returns {IMarket[]}
   */
  private getEventSelections(markets: IMarket[]): IOutcome[] {
    return _.flatten(_.pluck(markets, 'outcomes'));
  }

  /**
   * getTimeformGreyhoundsMap()
   * @param {ITimeFormEntry[]} entries
   * @returns {Object}
   */
  private getTimeformGreyhoundsMap(entries: ITimeFormEntry[]): Object {
    return _.reduce(entries, (map, entry) => {
      _.each(entry.openBetIds, id => {
        if (id) {
          const timeformData = _.pick(entry, this.GREYHOUND_SUMMARY_KEYS);

          timeformData.stars = new Array(timeformData.starRating);
          timeformData.trainer = this.getTrainerName(timeformData.trainerFullName);

          map[id] = timeformData;
        }
      });

      return map;
    }, {});
  }

  /**
   * getPositionsPrediction()
   * @param {any} greyhoundsMap
   * @returns {any}
   */
  private getPositionsPrediction(greyhoundsMap: any): any {
    return _.chain(greyhoundsMap)
      .reduce((list, greyhound) => {
        const greyhoundIncluded = _.findWhere(list, { entryId: greyhound.entryId } );

        if (greyhound.positionPrediction && greyhound.statusName !== this.NON_RUNNER_STATUS &&
          !greyhoundIncluded) {
          list.push(greyhound);
        }
        return list;
      }, [])
      // @ts-ignore
      .sortBy('positionPrediction')
      .value();
  }

  /**
   * getTrainerName()
   * @param {string} trainerFullName
   * @returns {string}
   */
  private getTrainerName(trainerFullName = ''): string {
    const bracketsPosition = trainerFullName.indexOf('(');

    return trainerFullName
      .substring(0, bracketsPosition > -1 ? bracketsPosition : trainerFullName.length)
      .trim();
  }
}
