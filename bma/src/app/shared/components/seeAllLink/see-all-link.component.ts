import { Input, Component, ViewEncapsulation, ChangeDetectionStrategy } from '@angular/core';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { GOLF_CONSTANTS } from '@app/shared/constants/channel.constant';

@Component({
  selector: 'see-all-link',
  template: '<a [i18n]="\'sb.seeAll\'" class="see-all-link" [routerLink]="link" (click)="sendGTMData()"></a> ',
  styleUrls: ['./see-all-link.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class SeeAllLinkComponent {
  @Input() link?: string;
  @Input() targetTab;
  @Input() sportId;
  @Input() eventType;
  constructor(private gtmService:GtmService){}
  sendGTMData():void{
    if(this.sportId=='18'){
    const gtmData={
      event: 'Event.Tracking',
      'component.CategoryEvent': 'navigation',
      'component.LabelEvent': 'golf',
      'component.ActionEvent': 'click',
      'component.PositionEvent': this.eventType,
      'component.LocationEvent': GOLF_CONSTANTS[this.targetTab.name] || this.targetTab.name,
      'component.EventDetails': 'see all',
      'component.URLClicked': 'Clicked URL'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
  }
}
