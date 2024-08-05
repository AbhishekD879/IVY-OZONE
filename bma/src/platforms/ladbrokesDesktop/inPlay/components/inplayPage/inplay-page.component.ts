import { Component, ChangeDetectionStrategy } from '@angular/core';
import { InplayPageComponent as AppInplayPageComponent } from '@ladbrokesMobile/inPlay/components/inplayPage/inplay-page.component';

@Component({
  selector: 'inplay-page',
  templateUrl: 'inplay-page.component.html',
  styleUrls: ['./inplay-page.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplayPageComponent extends AppInplayPageComponent {
}
