import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import { from } from 'rxjs';

import { YourcallBybLeagueService } from '@yourcall/components/bybLeague/yourcall-byb-league.service';
import { IYourcallBYBEventResponse } from '@yourcall/models/byb-events-response.model';
import { IBybExtendedLeagueEvent } from '@yourcall/models/byb-extended-league-event.model';
import { YourCallLeague } from '@yourcall/models/yourcall-league';
import { TimeService } from '@core/services/time/time.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';

@Component({
  selector: 'yourcall-byb-league',
  templateUrl: 'yourcall-byb-league.component.html'
})

export class YourcallBybLeagueComponent implements OnInit, OnChanges {
  @Input() league: YourCallLeague;
  @Input() filter: string;

  loading: boolean = false;
  events: IBybExtendedLeagueEvent[] = [];
  @Output() readonly eventsLoaded: EventEmitter<void> = new EventEmitter();

  constructor(
    private locale: LocaleService,
    private router: Router,
    private yourcallBybLeagueService: YourcallBybLeagueService,
    private timeService: TimeService,
    private seoDataService: SeoDataService
  ) { }

  ngOnChanges(changes: SimpleChanges) {
    if (changes && changes.filter && !changes.filter.firstChange) {
      this.initData();
    }
  }

  ngOnInit(): void {
    this.initData();
  }

  initData(): void {
    const interval = this.yourcallBybLeagueService.getInterval(this.filter);

    this.loading = true;

    from(this.yourcallBybLeagueService.getLeagueEvents(this.league, interval))
      .subscribe((data: IYourcallBYBEventResponse[]) => {
        this.events = this.yourcallBybLeagueService.parse(data);
        _.each(this.events, (event: IBybExtendedLeagueEvent) => {
          event.date = this.timeService.getEventTime(event.date);
        });
      }, error => {
        console.warn(error);
      }, () => {
        this.loading = false;
        this.league.eventsLoaded = true;
        this.eventsLoaded.emit();
      });
  }

  trackById(index, event: IBybExtendedLeagueEvent): string {
    return `${event.id} ${index}`;
  }

  /**
   * Go to Event Detail Page
   * @param event
   */
  goToEvent(event: IBybExtendedLeagueEvent): void {
    this.yourcallBybLeagueService.getEventPath(event, this.league).subscribe((path: string) => {
      this.router.navigateByUrl(`/${path}/${this.locale.getString('yourcall.pathBuildYourBet')}`);
      this.seoDataService.eventPageSeo(event, path);
    });
  }
}
