import { Injectable } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';

@Injectable()
export class EventTimeService {
  constructor(
    private filterService: FiltersService
  ) {}

  getDate(event: ISportEvent): string {
    const eventDate = this.filterService.date(event.startTime, 'EEEE d MMMM yyyy - HH:mm');
    const monthDate = (eventDate.match(/(\d+)/) && eventDate.match(/(\d+)/)[0]) || '';
    const monthDateSuffix = this.filterService.numberTranslatedSuffix(monthDate);

    return eventDate.replace(/(\d+)/, `$1${monthDateSuffix}`);
  }
}
