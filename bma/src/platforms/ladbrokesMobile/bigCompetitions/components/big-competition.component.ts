import { Component } from '@angular/core';

import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';

@Component({
  selector: 'big-competition',
  templateUrl: 'big-competition.component.html',
  styleUrls: ['big-competition.component.scss']
})
export class MobileBigCompetitionComponent extends BigCompetitionComponent {
  brand = {brand:'Lads', device: 'Mobile'};
}
