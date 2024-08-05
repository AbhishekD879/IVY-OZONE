import { Component } from '@angular/core';

@Component({
  selector: 'blurb-message',
  templateUrl: './blurb-message.component.html',
  styleUrls: ['./blurb-message.component.scss']
})
export class BlurbMessageComponent {
  blurbMessage :string ='Other subscribed lines for these draws will appear in your my bets area within the next 24hrs.';
}
