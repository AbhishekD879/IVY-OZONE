import { ActivatedRoute } from '@angular/router';
import { Component, Output, Input, OnInit, EventEmitter } from '@angular/core';

import { TOTE_CONFIG } from '../../tote.constant';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'tote-request-error',
  templateUrl: './tote-request-error.component.html'
})
export class ToteRequestErrorComponent implements OnInit {
  @Input() activeTab: { id: string };
  @Output() readonly reload: EventEmitter<void> = new EventEmitter();

  responseError: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private routingState: RoutingState
  ) {}

  ngOnInit(): void {
    if (this.route.snapshot.params['sport']) {
      const routeParams = this.routingState.getRouteParam('sport', this.route.snapshot);
      this.activeTab.id = `tab-${(routeParams || TOTE_CONFIG.DEFAULT_TOTE_SPORT)}`;
    } else {
      this.activeTab.id = `tab-results`;
    }
  }
}
