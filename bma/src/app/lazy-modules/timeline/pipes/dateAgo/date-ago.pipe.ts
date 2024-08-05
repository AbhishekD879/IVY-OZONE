import { Pipe, PipeTransform, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { Observable, interval } from 'rxjs';
import { startWith, map } from 'rxjs/operators';

import { TimeService } from '@core/services/time/time.service';
@Pipe({
  name: 'dateAgo',
  pure: false
})
export class DateAgoPipe extends AsyncPipe implements PipeTransform, OnDestroy {
  private value: string;
  private timer: Observable<string>;

  constructor(
    public ref: ChangeDetectorRef,
    protected timeService: TimeService
  ) {
    super(ref);
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();
  }

  transform(value: any): any {
    if (value) {
      this.value = value;

      if (!this.timer) {
        this.timer = this.getObservable();
      }

      return super.transform(this.timer);

    }

    return value;
  }

  private getObservable(): Observable<string> {
    return interval(30000).pipe(
      startWith(0),
      map(() => {
        const seconds = Math.floor((Date.now() - new Date(this.value).getTime()) / 1000);
        const minutes = Math.floor(seconds / 60);

        if (minutes < 1) {
          return 'Just now';
        } else if (minutes < 60) {
          return `${minutes} minute${minutes > 1 ? 's' : ''}`;
        } else {
          return this.timeService.getEventTime(this.value);
        }
      }));
  }
}
