import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'eventName'
})
export class EventNamePipe implements PipeTransform {

  /**
   * Remove unnecessary flags from event name
   */
  transform(value: string): string {
    return value ?
      value.replace(/\(SS\)|\(BG\)|\(GBR\)|\(Bo\d+\)/gi, '')
        .replace(/\|SS\||\|BG\||\|GBR\||\|Bo\d+\|/gi, '')
        .trim() : '';
  }
}
