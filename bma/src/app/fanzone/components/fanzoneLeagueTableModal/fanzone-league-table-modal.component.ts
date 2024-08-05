import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'fanzone-league-table-modal',
  templateUrl: './fanzone-league-table-modal.component.html',
  styleUrls: ['./fanzone-league-table-modal.component.scss']
})

export class FanzoneLeagueTableModalComponent {
  @Input() leagueSrcLink: string;
  @Input() isDesktop: boolean;
  @Output() readonly closeOverlay = new EventEmitter();

  constructor() {}

  close(): void {
    this.closeOverlay.emit();
  }
}
