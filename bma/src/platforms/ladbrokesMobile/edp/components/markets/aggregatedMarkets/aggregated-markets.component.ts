import { Component, HostBinding, Input } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { AggregatedMarketsComponent as AppAggregatedMarketsComponent } from '@edp/components/markets/aggregatedMarkets/aggregated-markets.component';
@Component({
  selector: 'aggregated-markets',
  styleUrls: ['./aggregated-markets.component.scss'],
  templateUrl: './aggregated-markets.component.html'
})
export class AggregatedMarketsComponent extends AppAggregatedMarketsComponent {
  @HostBinding('class.is-expanded') isExpanded: boolean;
  @Input() eventEntity: ISportEvent;

  toggled(event: MouseEvent) {
    super.toggled(event);
    this.headerClasses = this.setHeaderClass();
  }

  /**
   * Set Header CSS Class
   * @returns { [key: string]: boolean }
   */
  setHeaderClass(): { [key: string]: boolean } {
    const classes = {
      'inner-header': this.isChevronToLeft || this.inner,
      'byb-header': this.isBybState && !this.isChevronToLeft,
    };
    if (this.headerClass) {
      classes[this.headerClass] = this.headerClass;
    }
    return classes;
  }
}
