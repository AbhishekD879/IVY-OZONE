import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { DeviceService } from '@core/services/device/device.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'favourites-add-all',
  templateUrl: './favourites-add-all-button.html',
  styleUrls: ['./favourites-add-all-button.component.scss']
})
export class FavouritesAddAllButtonComponent implements OnInit, OnDestroy {

  @Input() eventsArray: ISportEvent[];

  starSelected: boolean = false;
  clickLock: boolean = true;
  isAvailable: boolean = false;

  constructor(
    private favouritesService: FavouritesService,
    private deviceService: DeviceService,
    private pubSubService: PubSubService
  ) { }

  ngOnInit() {
    this.favouritesService.showFavourites().subscribe((res: boolean) => {
      this.isAvailable = res;
      if (this.isAvailable) {
        this.initCounter('bsReceipt', true);
      }
    });
  }

  ngOnDestroy() {
    if (this.isAvailable) {
      this.favouritesService.removeCountListener('bsReceipt');
    }
  }

  /**
   * applyAction()
   * @param {Event} event
   */
  applyAction(event: Event): void {
    if (this.clickLock) {
      event.stopPropagation();
      return;
    }

    this.clickLock = true;
    this.favouritesService.isAllFavourite(this.eventsArray, 'football')
      .then(isAllFavourite => {
        const method = isAllFavourite ? this.favouritesService.removeEventsArray : this.favouritesService.addEventsArray,
          config = { sportName: 'football', fromWhere: 'bsreceipt' };

        method(this.eventsArray, config).then(() => {
          this.pubSubService.publish(this.pubSubService.API.EVENT_ADDED);
          if (this.deviceService.isWrapper) {
            this.favouritesService.syncToNative();
          }
        });
      });
  }

  /**
   * initCounter()
   * @param {string} listenerName
   * @param {boolean} initRefresh
   */
  initCounter(listenerName: string, initRefresh: boolean = false): void {
    this.favouritesService.countListener(listenerName, initRefresh)
      .then(() => {
          this.initIsAllFavourite();
          this.initCounter(listenerName);
        },
        error => {
          console.warn(error);
          this.initCounter(listenerName);
        });
  }

  /**
   * initIsAllFavourite()
   */
  initIsAllFavourite(): void {
    this.favouritesService.isAllFavourite(this.eventsArray, 'football')
      .then(result => {
        this.starSelected = result;
        this.clickLock = false;
      });
  }
}
