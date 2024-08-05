import { ISwitcherConfig } from '@core/models/switcher-config.model';

export interface IBetHistorySwitcherConfig extends ISwitcherConfig {
  /**
   * Reference name/key/code or object which relates switcher/tab to response data fields
   */
  refs?: any;
}
