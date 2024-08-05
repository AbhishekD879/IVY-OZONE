import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'sortBy'
})
export class SortByPipe implements PipeTransform {
  transform(value: any[], name: string, descending: boolean = false): any[] {
    if (!value || !name)
      return value;
    
    let p: string = name;

    let sortFn:(a: any, b: any) => any = (a, b) => {
      let value: number = 0;
      if (a[p] === undefined) value = -1;
      else if (b[p] === undefined) value = 1;
      else value = a[p] > b[p] ? 1 : (b[p] > a[p] ? -1 : 0);
      return descending ? (value * -1) : value;
    };

    value.sort(sortFn);
    return value;
  }
}