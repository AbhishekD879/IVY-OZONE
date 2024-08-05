import { Component, HostBinding, Input, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';

@Component({
  selector: 'favourites-add-button',
  templateUrl: './favourites-add-button.html'
})
export class FavouritesAddButtonComponent implements OnInit, OnDestroy {

  @Input() event: ISportEvent;
  @Input() sportName: string;
  @Input() config?: Object;

  @HostBinding('class.hidden') isDisabled: boolean = true;

  id: string;
  clickLock: boolean = false;
  isFavourite: boolean;
  title: string;

  constructor(
    private favouritesService: FavouritesService,
    private pubSubService: PubSubService,
    private cdRef: ChangeDetectorRef
  ) {
  }

  ngOnInit() {
    this.title = `favourites-button-${this.id}-${this.event.id}`;

    this.favouritesService.showFavourites().subscribe((res: boolean) => {
      this.isDisabled = !res;
      if (!this.isDisabled) {
        this.id = Math.random()
          .toString(36)
          .slice(2);

        this.initListener();
        this.checkIsFavourite();
      }
    });
  }

  ngOnDestroy() {
    if (!this.isDisabled) {
      this.favouritesService.deRegisterListener(this.event, this.id);
      this.pubSubService.unsubscribe(this.title);
    }
  }

  /**
   * Init listeners
   */
  initListener(): void {
    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.checkIsFavourite();
    });

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SESSION_LOGOUT], () => {
      this.isFavourite = false;
    });

    this.favouritesService
      .registerListener(this.event, this.id)
      .then(
        (result: any) => {
          this.setClickLock(result);
          this.initListener();
          this.isFavourite = (result === 'added');
          this.cdRef.detectChanges();
        },
        error => {
          this.setClickLock('error');
          this.initListener();
          console.warn(error);
        }
      );
  }

  /**
   * Set click lock
   * @param {string} status
   */
  setClickLock(status: string): void {
    this.clickLock = (status === 'pending');
  }

  /**
   * Add event to favourites
   * @returns {boolean}
   */
  add(): void {
    if (this.clickLock) {
      return;
    }

    this.favouritesService
      .add(this.event, this.sportName, this.config)
      .catch(error => {
        console.warn(error);
      });
  }

  /**
   * Check if event is set as favourite
   */
  private checkIsFavourite(): void {
    this.favouritesService
      .isFavourite(this.event, this.sportName)
      .then(() => {
        this.isFavourite = true;
        this.cdRef.detectChanges();
      })
      .catch(() => {
      });
  }
}
