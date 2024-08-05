'use strict';

import { WinPoolBetsModel } from './wn.model';

/**
 * Class for represent functionality for SH bet model
 * @class
 */
export class ShowPoolBetsModel extends WinPoolBetsModel {
  constructor(eventEntity, ip: string, poolType = 'SH') {
    // ignoring next test as there's an issue with coverage report which shows covered line as uncovered branch
    /* istanbul ignore next */
    super(eventEntity, ip, poolType);
  }
}
