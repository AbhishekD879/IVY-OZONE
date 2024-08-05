import { Component, OnInit, OnDestroy } from '@angular/core';

import { FiltersService } from '@core/services/filters/filters.service';
import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ICategory } from '@core/models/category.model';

import {
  EnhancedMultiplesTabComponent as BaseEnhancedMultiplesTabComponent
} from '@lazy-modules/enhancedMultiplesTab/components/enhanced-multiples-tab.component';

@Component({
  selector: 'enhanced-multiples-tab',
  templateUrl: '../../../../../app/lazy-modules/enhancedMultiplesTab/components/enhanced-multiples-tab.component.html'
})
export class EnhancedMultiplesTabComponent extends BaseEnhancedMultiplesTabComponent
  implements OnInit, OnDestroy {

  private readonly subscriberName = 'EnhancedMultiplesTabComponent';

  constructor(
    enhancedMultiplesService: EnhancedMultiplesService,
    filterSerice: FiltersService,
    private germanSupportService: GermanSupportService,
    private pubSubService: PubSubService
  ) {
    super(enhancedMultiplesService, filterSerice);
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.pubSubService.subscribe(this.subscriberName, this.pubSubService.API.SESSION_LOGIN, this.removeRestrictedCategories);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.subscriberName);
  }

  protected eventsLoaded(eventsCategories: ICategory[]): void {
    super.eventsLoaded(eventsCategories);
    this.removeRestrictedCategories();
  }

  private removeRestrictedCategories = () => {
    if (this.germanSupportService.isGermanUser()) {
      this.eventsCategories = this.germanSupportService.filterEnhancedCategories(this.eventsCategories);
    }
  }
}
