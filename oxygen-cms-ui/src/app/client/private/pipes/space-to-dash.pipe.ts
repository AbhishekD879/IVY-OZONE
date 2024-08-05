import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'spaceToDash',
})
export class SpaceToDashPipe implements PipeTransform {
  transform(value: string = ''): string {
    return value.toLowerCase()
      .trim()
      .replace(/\s/g, '-');
  }
}
