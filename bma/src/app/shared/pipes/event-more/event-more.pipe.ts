import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'eventMore'
})

export class EventMorePipe implements PipeTransform {
  transform(value: number): string {
    return value ? `${value - 1} MORE` : 'MORE';
  }
}
