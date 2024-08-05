import * as _ from 'underscore';

export class Cached {
  constructor(data, timeService) {
    _.extend(this, {
      data,
      updated: timeService.getCurrentTime()
    });
  }
}
