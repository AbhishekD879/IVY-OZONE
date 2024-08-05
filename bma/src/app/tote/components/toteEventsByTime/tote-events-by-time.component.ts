import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { TOTE_CONFIG } from '../../tote.constant';

import { IToteEvent } from './../../models/tote-event.model';

@Component({
  selector: 'tote-events-by-time',
  templateUrl: './tote-events-by-time.component.html'
})
export class ToteEventsByTimeComponent implements OnInit {
  @Input() events: IToteEvent[];

  expanded: boolean;
  limit: number;
  eventsOrder: string[];

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
    this.expanded = true;
    this.limit = TOTE_CONFIG.RECORDS_LIMIT_BY_TIME;
    this.eventsOrder = TOTE_CONFIG.order.BY_TIME_ORDER;
    this.events = this.events || [];
  }

  goToUrl(uri: string): void {
    this.router.navigateByUrl(uri);
  }
}
