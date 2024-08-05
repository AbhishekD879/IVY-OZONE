import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'favourite-icon',
  templateUrl: './favourite-icon.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FavouriteIconComponent {
  @Input() isActive: boolean;
  @Input() isOnMatch: boolean;
}
