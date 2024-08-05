import { Component } from '@angular/core';
import { OddsBoostPageComponent } from '@oddsBoost/components/oddsBoostPage/odds-boost-page.component';

@Component({
  selector: 'odds-boost-page',
  templateUrl: './odds-boost-page.component.html',
  styleUrls: ['./odds-boost-page.component.scss']
})
export class MobileOddsBoostPageComponent extends OddsBoostPageComponent {
  public availableBoost: string = 'availableBoost';
  public upcomingBoost: string = 'upcomingBoost';
  public available() {
    if(!this.isActive){
      this.timerMessage = false;
      this.validDateToShow = false;
      this.sportPills = [];
    }    
    this.isActive = true;
    this.isDefaultPillOnLoad = false;
    this.sendGTMData('available');
  }
  public upcoming() {
    if(this.isActive){
      this.timerMessage = false;
      this.validDateToShow = false;
      this.sportPills = [];
    }
    this.isActive = false;
    this.isDefaultPillOnLoad = false;
    this.sendGTMData('upcoming');
  }
}