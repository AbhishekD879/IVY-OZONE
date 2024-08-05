import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import {
  IKnockoutData,
  IEventsByRoundMap,
  IKnockoutEvents,
  IKnockoutRounds
} from './competition-knockouts.model';

@Injectable()
export class CompetitionKnockoutsService {
  /**
   * Get events data and sort them by rounds
   * @return {Object} eventsByRoundMap
   */
  parseData(data: IKnockoutData): IEventsByRoundMap {
    const eventsByRoundMap: IEventsByRoundMap = {
      roundNames: []
    };
    const rounds: IKnockoutRounds[] = data.knockoutRounds;
    const events: IKnockoutEvents[] = data.knockoutEvents;

    rounds.sort((prev: IKnockoutRounds, next: IKnockoutRounds) => {
      return next.number - prev.number;
    });

    _.forEach(rounds, (value: IKnockoutRounds, key: number) => {
      eventsByRoundMap[value.name] = [];
      eventsByRoundMap.roundNames[key] = rounds[key];
    });

    _.forEach(events, (value: IKnockoutEvents) => {
      for (const key in eventsByRoundMap) {
        if (key === value.round) {
          eventsByRoundMap[key].push(value);
        }
      }
    });

    this.sortEvents(eventsByRoundMap);

    return eventsByRoundMap;
  }

  /**
   * Sort events by abbreviation
   * @param {object} eventsByRoundMap
   */
  private sortEvents(eventsByRoundMap: IEventsByRoundMap): void {
    for (const key in eventsByRoundMap) {
      if (key !== 'roundNames') {
        const sortedEvents = _.sortBy(eventsByRoundMap[key], 'abbreviation');
        eventsByRoundMap[key] = this.splitEvents(sortedEvents);
      }
    }
  }

  /**
   * Split events on arrays
   * @param {Array} arr
   * @return {Array} result
   */
  private splitEvents(arr): IKnockoutEvents[] {
    const result = [];
    for (let i = 1; i <= arr.length; i += 2) {
      if (!arr[i]) {
        result.push([arr[i - 1]]);
      } else {
        result.push([arr[i - 1], arr[i]]);
      }
    }
    return result;
  }
}
