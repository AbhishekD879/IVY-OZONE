import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FavouritesService } from '@app/favourites/services/favourites.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'favourites-counter',
  templateUrl: './favourites-counter.html'
})
export class FavouritesCounterComponent implements OnInit, OnDestroy {

  @Input() listenerName: string;
  @Input() sportName: string;

  count: number;
  isAvailable: boolean = false;

  constructor(
    private favouritesService: FavouritesService,
    public windowRef: WindowRefService
  ) {
    this.initCounter = this.initCounter.bind(this);
  }

  ngOnInit() {
    this.favouritesService.showFavourites().subscribe((show: boolean) => {
      this.isAvailable = show;
      if (this.isAvailable) {
        this.initCounter(this.listenerName, true);
      }
    });
  }

  ngOnDestroy() {
    if (this.isAvailable) {
      this.favouritesService.removeCountListener(this.listenerName);
    }
  }

  iconClicked() {
    this.windowRef.document.getElementById('icon').classList.add('fav-icon-active');
  }

  iconClickRemove() {
    this.windowRef.document.getElementById('icon').classList.add('fav-icon-inactive');
  }

  /**
   * initCounter()
   * @param {string} listenerName
   * @param {boolean} initRefresh
   */
  initCounter(listenerName: string, initRefresh: boolean = false) {
    this.favouritesService.countListener(listenerName, initRefresh).then(
      count => {
        this.count = count;
        this.initCounter(listenerName);
      },
      error => {
        console.warn(error);
        this.initCounter(listenerName);
      }
    );
  }
}
