import {Pipe, PipeTransform} from '@angular/core';

// find Uppercase Letters, exclude few upppercase letters in a row, replace only first.
const regex: RegExp = /([^A-Z])([A-Z])/g;
const replaceWith: string = '$1 $2';

@Pipe({name: 'camelCaseToSpace'})
export class CamelCaseToSpacePipe implements PipeTransform {
  transform(value: string, args: string[]): any {
    if (!value || !value.replace) {
      return value;
    }

    return value.replace(regex, replaceWith);
  }
}
