import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'filter'
})

export class FilterPipe implements PipeTransform {
 transform(value: any, input: string, searchableList: any) {
  if (input) {
   input = input.toLowerCase();
   return value.filter(function (el: any) {
   let isTrue = false;
   for (const k of Object.keys(searchableList)) {
     if (el[searchableList[k]].toLowerCase().indexOf(input) > -1) {
       isTrue = true;
     }
     if (isTrue) {
       return el;
     }
    }
  });
 }
 return value;
 }
}
