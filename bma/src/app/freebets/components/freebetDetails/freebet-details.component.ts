import { finalize } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { FiltersService } from '@core/services/filters/filters.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { UserService } from '@core/services/user/user.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';

@Component({
  selector: 'freebet-details',
  templateUrl: './freebet-details.component.html'
})
export class FreebetDetailsComponent extends AbstractOutletComponent implements OnInit {
  item: IFreebetToken;

  constructor(
    private filtersService: FiltersService,
    private userService: UserService,
    private router: Router,
    private freebetsService: FreeBetsService,
    private route: ActivatedRoute,
    private routingState: RoutingState,
    private coreToolsService: CoreToolsService
  ) {
    super();
  }

  ngOnInit() {
    const betId = this.routingState.getRouteParam('betId', this.route.snapshot);
    this.freebetsService.getFreeBet(betId).pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((data: IFreebetToken) => {
        this.item = this.coreToolsService.deepClone(data);
        this.item.freebetTokenValue = this.filtersService.setCurrency(data.freebetTokenValue, this.userService.currencySymbol);
      }, () => {
        if (!this.userService.status) {
          this.router.navigate(['/']);
        } else {
          this.showError();
        }
      });
  }
}
