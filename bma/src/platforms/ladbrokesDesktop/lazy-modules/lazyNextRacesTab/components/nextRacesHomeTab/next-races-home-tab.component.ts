import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { NextRacesHomeTabComponent } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';

@Component({
  selector: 'next-races-home-tab',
  templateUrl: 'next-races-home-tab.component.html'
})
export class LadbrokesNextRacesHomeTabComponent extends NextRacesHomeTabComponent implements OnInit {
  extraPlaceLimit: number = 1;
  moduleType: string;
  compName: string;
  @Input() racingName: string;

  constructor(protected route: ActivatedRoute,
    protected navigationService: NavigationService) {
    super(navigationService);
  }

  ngOnInit(): void {
    this.setModuleType();
  }

  private setModuleType(): void {
    this.moduleType = ((this.route.snapshot.data['segment'] && this.route.snapshot.data['segment'] === 'greyhound.nextRaces') || this.racingName==='greyhound')
      ? 'greyhound'
      : 'horseracing';
      if(this.moduleType == 'greyhound') {
        this.compName = 'greyhounds'
      } else if(this.moduleType == 'horseracing') {
        this.compName = 'horseracing'
      }
  }
}
