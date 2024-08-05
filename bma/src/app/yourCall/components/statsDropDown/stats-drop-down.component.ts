import {
  Component,
  EventEmitter,
  Input,
  Output,
  ChangeDetectionStrategy,
  OnInit
} from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { IYourcallStatisticItem } from '@yourcall/models/yourcall-api-response.model';
import { IFiveASidePlayer } from '@yourcall/services/fiveASide/five-a-side.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { PITCH_NAVIGATION } from '@yourcall/constants/five-a-side.constant';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'stats-drop-down',
  templateUrl: './stats-drop-down.component.html',
  styleUrls: ['./stats-drop-down.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class StatsDropDownComponent implements OnInit {
  @Input() eventEntity: ISportEvent;
  @Input() formation: IMatrixFormation;
  @Input() player: IFiveASidePlayer;

  @Output() readonly statChange: EventEmitter<IYourcallStatisticItem> = new EventEmitter();

  showMenu: boolean = false;
  stats: IYourcallStatisticItem[] = [];
  pitchNavigation: {[key: string]: string} = PITCH_NAVIGATION;

  constructor(public fiveASideService: FiveASideService,
    private gtmService: GtmService) {
  }

  ngOnInit(): void {
    if (this.fiveASideService.activeView === this.pitchNavigation.playerList) {
      this.fiveASideService.loadPlayerStats(this.eventEntity.id, this.player.id)
      .subscribe((response: IYourcallStatisticItem[]) => {
        this.stats = response;
      });
    } else {
      this.stats = this.fiveASideService.getPlayerStats(this.eventEntity.id, this.player.id);
    }
  }

  trackByFn(index: number, item: IYourcallStatisticItem): number {
    return item.id;
  }

  clickItem(item: IYourcallStatisticItem): void {
    if (item.id !== this.formation.statId) {
      this.statChange.emit(item);
    }

    this.menuToggle();
  }

  menuToggle(show?: boolean): void {
    this.showMenu = show !== undefined ? show : !this.showMenu;
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: this.showMenu ? 'Show Markets': 'Hide Markets',
      eventLabel: 'Market Dropdown'
    });
  }

  clickHandler(event: Event): void {
    if (!event.cancelable) { return; }

    event.preventDefault();
    this.menuToggle(false);
  }
}
