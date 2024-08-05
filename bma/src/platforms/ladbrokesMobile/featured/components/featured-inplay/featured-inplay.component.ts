import { Component, ViewEncapsulation, ChangeDetectionStrategy } from '@angular/core';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';

@Component({
  selector: 'featured-inplay',
  styleUrls: ['../../../../../app/featured/components/featured-inplay/featured-inplay.component.scss', './featured-inplay.component.scss'],
  templateUrl: '../../../../../app/featured/components/featured-inplay/featured-inplay.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class LadbrokesFeaturedInplayComponent extends FeaturedInplayComponent {}
