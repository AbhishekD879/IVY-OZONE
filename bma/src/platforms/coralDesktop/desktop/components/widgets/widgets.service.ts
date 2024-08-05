import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { WIDGET_CONSTANT } from '@desktop/constants/widgets.constants';
import { ISportConfigurationTabs } from '@sb/models/sport-configuration.model';
import { IWidgetConfig, IWigetsConfigsData } from '@desktop/models/wigets.model';

@Injectable()
export class WidgetsService {
  activeWidgets: IWidgetConfig = {};

  private defaultWidgetsConfig = WIDGET_CONSTANT;

  constructor() { }

  /**
   * Get config for tabs
   * @param config
   * @return {Object} widgets
   */
  getConfig(config: ISportConfigurationTabs[]): IWigetsConfigsData {
    const widgets = {};

    _.each(config, (tab: any) => {
      widgets[tab.id] = this.convertArrayToObject(tab.widgets || this.defaultWidgetsConfig[tab.name]);
    });
    return widgets;
  }

  /**
   * Get Widgets Visibility
   * @param {Object} widget
   * @returns {Boolean}
   */
  getWidgetsVisibility(widget: IWidgetConfig): boolean {
    this.activeWidgets = widget ? _.extend(this.activeWidgets, widget) : this.activeWidgets;
    return _.contains(_.values(this.activeWidgets), true);
  }

  /**
   * Convert array to object
   * @param array
   * @return {Object}
   */
  private convertArrayToObject(array: any): any {
    const object: any = {};
    _.each(array, (item: any) => {
      object[item] = true;
    });
    return object;
  }
}
