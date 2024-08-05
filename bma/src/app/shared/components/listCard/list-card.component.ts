import {
  Component,
  HostListener,
  Output,
  ViewEncapsulation,
  EventEmitter,
  Input
} from '@angular/core';
import { Router } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
@Component({
  selector: 'list-card',
  templateUrl: 'list-card.component.html',
  styleUrls: ['./list-card.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class ListCardComponent {
  @Input() item: { name: string , svgId : string};
  @Input() link: string;
  @Input() date?: string;
  @Input() title?: string;
  @Input() eventId?: string;
  @Input() filter?: string;
  @Input() isEventOverlay?: boolean;
  
  @Output() readonly clickFunction?: EventEmitter<{}> = new EventEmitter();
  @Output() readonly overlayContent?: EventEmitter<{}> = new EventEmitter();
  constructor(private router: Router,
    protected pubSubService: PubSubService,
    protected sessionStorageService: SessionStorageService) {}

  @HostListener('click', ['$event'])
  gotToPage($event: Event): void {
    if (this.clickFunction.observers.length) {
      this.clickFunction.emit(event);
    } else {
      if(this.isEventOverlay) {
        this.overlayContent.emit({filter: this.filter, eventId: this.eventId});
      }
      this.router.navigateByUrl(this.link);
    }
    $event.preventDefault();
  }
}
