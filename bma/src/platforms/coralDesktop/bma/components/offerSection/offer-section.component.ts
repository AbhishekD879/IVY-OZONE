import { OffersSectionComponent as AppOffersSectionComponent } from '@bma/components/offerSection/offer-section.component';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'offer-section',
  templateUrl: './offer-section.component.html'
})
export class OffersSectionComponent extends AppOffersSectionComponent implements OnInit {

  ngOnInit(): void {
    this.getOffersData('desktop');
  }
}
