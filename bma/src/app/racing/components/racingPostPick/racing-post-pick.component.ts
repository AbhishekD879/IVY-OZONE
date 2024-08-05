import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'racing-post-pick',
  templateUrl: './racing-post-pick.component.html',
  styleUrls: ['./racing-post-pick.component.scss'],
})
export class RacingPostPickComponent implements OnInit {
  @Input() eventEntity: string;
  racingPostPick: number[] = [];

  ngOnInit() {
    this.racingPostPick = this.eventEntity.split('-').map(Number);
  }
}
