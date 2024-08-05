import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'addSpaceAfterComma',
})
export class AddSpaceAfterCommaPipe implements PipeTransform {
  transform(value: string = ''): string {
    return value.replace(/,/g, ', ');
  }
}
