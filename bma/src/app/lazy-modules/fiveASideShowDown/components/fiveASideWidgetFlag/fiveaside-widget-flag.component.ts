import { Component, ChangeDetectionStrategy } from '@angular/core';
import { FiveasideCrestImageComponent } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveaside-crest-image.component';

@Component({
  selector: 'fiveaside-widget-flag',
  templateUrl: './fiveaside-widget-flag.component.html',
  styleUrls: ['./fiveaside-widget-flag.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveasideWidgetFlagComponent extends FiveasideCrestImageComponent {
}
