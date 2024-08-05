import { Component, Input, OnInit } from '@angular/core';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
  selector: 'free-bet-icon',
  template: `<a [routerLink]="['/freebets']" *ngIf='freeBetVisible' data-crlat="showFreeBetsIcon">FB</a>`,
  styleUrls: ['./free-bet-icon.component.scss']
})
export class FreeBetIconComponent implements OnInit {
  @Input() event: ISportEvent;
  freeBetVisible: boolean;

  constructor(
    private freeBetsService: FreeBetsService
  ) {}

  ngOnInit(): void {
    this.freeBetVisible = this.freeBetsService.isFreeBetVisible(this.event);
  }
}
