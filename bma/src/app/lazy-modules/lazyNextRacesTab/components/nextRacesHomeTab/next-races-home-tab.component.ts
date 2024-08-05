import { Component } from '@angular/core';
import { NavigationService } from '@core/services/navigation/navigation.service';

@Component({
  selector: 'next-races-home-tab',
  templateUrl: './next-races-home-tab.component.html'
})
export class NextRacesHomeTabComponent {
  extraPlaceLimit: number = 2;
  moduleType: string;
  showLoader: boolean = true;
  constructor(protected navigationService: NavigationService) { }

  /**
   * Hide loader when child component will be ready
   * @param dataLoaded - identifies whether data was loaded in child component
   */
  toggleLoader(dataLoaded: boolean = false): void {
    this.showLoader = !dataLoaded;
    this.navigationService.emitChangeSource.next(dataLoaded);
  }
}
