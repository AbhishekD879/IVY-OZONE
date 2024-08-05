import { Component, Input, OnInit, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'btn-odds',
  templateUrl: './btn-odds.component.html',
  styleUrls: ['./btn-odds.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BtnOddsComponent implements OnInit {
  @Input() isActive: boolean = true;
  @Input() isLoading: boolean = false;
  @Input() template: string = 'placeBet';
  @Input() price: string;
  @Input() oddsFormat?: string;

  public emptyPriceLabel: string;

  ngOnInit(): void {
    if (this.oddsFormat === 'dec') {
      this.emptyPriceLabel = '-.-';
    } else {
      this.emptyPriceLabel = '-/-';
    }
  }
}
