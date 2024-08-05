import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import QuickLinks from '../../constants/quickLinks';

@Component({
  selector: 'quick-links-header',
  templateUrl: './quick-links-header.component.html',
  styleUrls: ['./quick-links-header.component.scss']
})
export class QuickLinksHeaderComponent {
  ycIconDisplay: string = 'general';
  quickLinks = QuickLinks;

  constructor(
    private activatedRoute: ActivatedRoute,
    private routingHelperService: RoutingHelperService
  ) {

  }

  getLinkUrl(className: string, typeName: string): string {
    const sport: string = this.activatedRoute.snapshot.params.sport;

    return this.routingHelperService.formCompetitionUrl({
      sport,
      typeName,
      className: `${sport} ${className}`
    });
  }

  trackQuickLink(index: number, item: {[key: string]: any}): any {
    return item.id;
  }
}
