import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FreeRideAPIService } from '../services/free-ride.api.service';
import { ViewHorses, ViewPotsDataTable } from './model/view-pots.model';

@Component({
  selector: 'app-view-pot-table',
  templateUrl: './view-pot-table.component.html',
  styleUrls: ['./view-pot-table.component.scss']
})
export class ViewPotTableComponent implements OnInit {
    potNumbers: Array<string>;
    displayPotData: Array<ViewPotsDataTable>;
    filteredPotsData: Array<ViewHorses>;
    showTable: boolean = false;
    selectedPot: string;
    columns = [
        { name: 'Horse Name', property: 'horseName' },
        { name: 'Race Name', property: 'raceName' },
        { name: 'Race Time', property: 'raceTime' },
        { name: 'Rating', property: 'rating' },
        { name: 'weights', property: 'weight' },
        { name: 'Odds', property: 'odds' }
    ];

  constructor(private freeRideService: FreeRideAPIService,
    private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.getViewPotsData();
  }

  getViewPotsData(): void {
    this.freeRideService.getViewPotsData(this.route.snapshot.paramMap.get('id')).subscribe((res: any) => {
      this.potNumbers = ['Top Player + Big & Strong + Good Chance',
      'Top Player + Big & Strong + Nice Price/Surprise Me',
      'Top Player + Small & Nimble/Surprise Me + Good Chance',
      'Top Player + Small & Nimble/Surprise Me + Nice Price/Surprise Me',
      'Dark Horse/Surprise Me + Big & Strong + Good Chance',
      'Dark Horse/Surprise Me + Big & Strong + Nice Price/Surprise Me',
      'Dark Horse/Surprise Me + Small & Nimble/Surprise Me + Good Chance',
      'Dark Horse/Surprise Me + Small & Nimble/Surprise Me + Nice Price/Surprise Me'];
      this.displayPotData = res.body;
      this.filteredPotsData = this.displayPotData[0].horses;
      this.selectedPot = this.potNumbers[0];
      });
  }

  filterPot(i) {
   this.filteredPotsData = this.displayPotData[i].horses;
  }

}
