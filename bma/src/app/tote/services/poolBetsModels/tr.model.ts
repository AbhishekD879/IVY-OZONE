import { ExPoolBetsModel } from './ex.model';

/**
 * Class for represent functionality for SH bet model
 * @class
 */
export class TrPoolBetsModel extends ExPoolBetsModel {
  constructor(eventEntity, ip: string, poolType = 'TR') {
    // ignoring next test as there's an issue with coverage report which shows covered line as uncovered branch
    /* istanbul ignore next */
    super(eventEntity, ip, poolType);
  }
}
