import { Component, Input, Output, EventEmitter } from '@angular/core';
import * as _ from 'underscore';
import {
  IForecastMatrixMap, ITricastMatrixMap
} from '@lazy-modules/forecastTricast/components/forecastTricastCheckboxMatrix/forecast-tricast-checkbox-matrix.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'forecast-tricast-checkbox-matrix',
  styleUrls: ['./forecast-tricast-checkbox-matrix.scss'],
  templateUrl: './forecast-tricast-checkbox-matrix.component.html'
})
export class ForecastTricastCheckboxMatrixComponent {
  @Input() map: IForecastMatrixMap | ITricastMatrixMap;
  @Input() outcomesMap: { [key: string]: IOutcome };
  @Input() outcome: IOutcome;
  @Input() isSuspended: boolean;

  @Output() readonly mapUpdate: EventEmitter<IForecastMatrixMap | ITricastMatrixMap> = new EventEmitter();

  selectedOutcomes: IOutcome[];

  constructor() {}

  trackByCheckBox(index: number, element: {key: string; value: string}): string {
    return `${index}${element.key}${element.value}`;
  }

  get checkBoxMatrix(): {key: string, value: any}[]  {
    const currentMap = this.map[this.outcome.id];
    return _.map(_.keys(currentMap), (key: string) => ({
      key,
      value: currentMap[key]
    }));
  }
 set checkBoxMatrix(value:{key: string, value: any}[]){}
  getCssClass(element: {key: string; value: string}): string {
    return `${element.value} ${this.isSuspended ? 'disabled' : ''} ${this.outcome.nonRunner ? 'non-runner' : ''}`;
  }

  checkPlace(id: string, index: string): void {
    if (this.preventDoubleClick(id, index)) {
      return;
    }

    const uncheck = this.map[id][index] === 'checked';
    this.map[id][index] = uncheck ? 'open' : 'checked';

    if (index === 'any') {
      const val = _.some(this.map, el => el['any'] === 'checked') ? 'disabled' : 'enabled';
      _.each(this.map as ITricastMatrixMap, el => {
        el['1st'] = el['2nd'] = val;
        if ('3rd' in el) {
          el['3rd'] = val;
        }
        if (el['any'] === 'disabled') {
          el['any'] = 'enabled';
        }
      });
    } else {
      const val = uncheck ? 'enabled' : 'disabled';
      _.each(this.map, (el, elId) => {
        if (elId === id) {
          _.each(el, (pVal, pKey) => {
            if (pKey !== index && !_.some(this.map, item => item[pKey] === 'checked')) {
              el[pKey] = val;
            }
          });
        }

        if (!_.some(el, pVal => pVal === 'checked')) {
            el[index] = val;
        }
      });
    }

    this.mapUpdate.emit(this.map);
  }

  private preventDoubleClick(id: string, index: string): boolean {
    let preventClick;

    _.mapObject(this.map, (val: { [key: string]: string }, key: string) => {
      if (id === key) {
        // horizontal check
        if (val[index] !== 'checked' && _.values(val).includes('checked')) {
          preventClick = true;
        }
      } else {
        // vertical check
        if (index !== 'any' && (val[index] === 'checked' || val['any'] === 'checked')) {
          preventClick = true;
        }
      }
    });

    return preventClick;
  }
}
