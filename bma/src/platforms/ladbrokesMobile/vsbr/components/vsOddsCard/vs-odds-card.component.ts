import { Component } from '@angular/core';
import { VsOddsCardComponent as CoralVsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';

@Component({
  selector: 'vs-odds-card-component',
  templateUrl: 'vs-odds-card.component.html',
  styleUrls: ['./vs-odds-card.component.scss']
})

export class VsOddsCardComponent extends CoralVsOddsCardComponent {}
