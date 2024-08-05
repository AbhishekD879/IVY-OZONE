import { OnInit, Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { NavigationService } from '@core/services/navigation/navigation.service';

@Component({
  selector: 'sport-event',
  template: '<div></div>'
})
export class SportEventComponent implements OnInit {
  sportId: number;

  constructor(
    private siteServerService: SiteServerService,
    private routingHelperService: RoutingHelperService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private navigationService: NavigationService) {}

  ngOnInit(): void {
    this.sportId = Number(this.activatedRoute.snapshot.paramMap.get('sport'));

    if (isNaN(this.sportId)) {
      this.navigationService.handleHomeRedirect('edp');
    } else {
      this.siteServerService.getEventByEventId(this.sportId).then((event: ISportEvent) => {
        if (event) {
          const edpUrl = this.routingHelperService.formResultedEdpUrl(event);
          this.router.navigateByUrl(edpUrl);
        } else {
          this.navigationService.handleHomeRedirect('edp');
        }
      });
    }
  }
}
