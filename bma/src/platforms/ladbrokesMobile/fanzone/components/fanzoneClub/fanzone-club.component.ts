import { Component, ChangeDetectionStrategy, ViewEncapsulation } from '@angular/core';
import { FanzoneAppClubComponent } from '@app/fanzone/components/fanzoneClub/fanzone-club.component';

@Component({
  selector: 'fanzone-club',
  templateUrl: './fanzone-club.component.html',
  styleUrls: [
    '../../../../../app/fanzone/components/fanzoneClub/fanzone-club.component.scss',
    './fanzone-club.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  encapsulation: ViewEncapsulation.None
})
export class FanzoneClubComponent extends FanzoneAppClubComponent {
}