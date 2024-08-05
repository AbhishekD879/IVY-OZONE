import { Injectable } from '@angular/core';
import * as _ from 'lodash';

@Injectable()
export class CSVGeneratorService {

  /**
   * Generate an csv file and start downloading it.
   * @param {Array<any>} items
   * @param {Array<any>} tableData
   */
  downloadCSV(items: any[], tableData: any[]) {
    // Create map of keys which we need to form the table
    const keyMap = _.map(tableData, item => {
      return item.property;
    });

    items = items.map((item) => {
      if (item.svg) {
        delete item.svg;
      }
      return _.pick(item, keyMap);
    });

    const date = new Date();
    const shortenedDate = date.toLocaleDateString().replace('/', '');
    const timestamp = +date;
    const filename = `CVSDATA-${shortenedDate}-${timestamp}.csv`;

    let csv = '';

    // Loop the array of objects
    for (let row = 0; row < items.length; row++) {
      const keysAmount = Object.keys(items[row]).length;
      let keysCounter = 0;
      /* tslint:disable */
      if (row === 0) {
        // Add first row with titles
        for (let key in tableData) {
            csv += tableData[key].name + (keysCounter + 1 < keysAmount ? ',' : '\r\n');
            keysCounter++;
        }
        keysCounter = 0;
      }
      for (let key in items[row]) {
          let item = _.isObject(items[row][key]) ? JSON.stringify(items[row][key]).replace(/,/g, ';') : items[row][key];
          csv += item + (keysCounter+1 < keysAmount ? ',' : '\r\n');
          keysCounter++;
      }
      /* tslint:enable */
      keysCounter = 0;
    }

    const link = document.createElement('a');
    link.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(csv));
    link.setAttribute('download', filename);
    link.click();
  }
}
