import {Pipe, PipeTransform} from '@angular/core';

/**
 *  Convert array to string excluding empty values
 */
@Pipe({ name: 'arrayNoNull' })
export class ArrayNoNullPipe implements PipeTransform {
  transform(array: any[]): string {
    let str = '';
    if (array && array.length > 0) {
      str = array
        .map(day => day.toString())
        .filter(dayStr => dayStr !== '').join(',');
    }
    return str;
  }
}
