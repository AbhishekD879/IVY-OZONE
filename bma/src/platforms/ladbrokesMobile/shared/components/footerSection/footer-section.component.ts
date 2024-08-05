import { Component } from '@angular/core';
import { FooterSectionComponent as CoralFooterSectionComponent } from '@shared/components/footerSection/footer-section.component';

@Component({
  selector: 'footer-section',
  templateUrl: '../../../../../app/shared/components/footerSection/footer-section.component.html',
  styleUrls: ['footer-section.component.scss'],
})

export class FooterSectionComponent extends CoralFooterSectionComponent {}
