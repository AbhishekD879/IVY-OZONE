import { WinPoolBetsModel } from './wn.model';

/**
 * Class for represent functionality for PL bet model
 * @class
 */
export class PlacePoolBetsModel extends WinPoolBetsModel {
  constructor(eventEntity,  ip: string, poolType = 'PL') {
    // ignoring next test as there's an issue with coverage report which shows covered line as uncovered branch
    /* istanbul ignore next */
    super(eventEntity, ip, poolType);
  }
}
