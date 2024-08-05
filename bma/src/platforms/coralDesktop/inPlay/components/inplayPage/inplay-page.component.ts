import { Component, ChangeDetectionStrategy } from '@angular/core';
import { InplayPageComponent as AppInplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';

@Component({
  selector: 'inplay-page',
  templateUrl: 'inplay-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class InplayPageComponent extends AppInplayPageComponent {
}
