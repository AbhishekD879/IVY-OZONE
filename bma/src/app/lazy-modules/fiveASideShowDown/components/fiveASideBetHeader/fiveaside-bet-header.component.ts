import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { GTM_EVENTS, LEADERBOARD_WIDGET } from '@app/fiveASideShowDown/constants/constants';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';

@Component({
  selector: 'fiveaside-bet-header',
  templateUrl: './fiveaside-bet-header.component.html',
  styleUrls: ['./fiveaside-bet-header.component.scss']
})
export class FiveasideBetHeaderComponent {
  @Input() bet: any;

  constructor(private router: Router,
    private rulesEntryService: FiveasideRulesEntryAreaService) { }

  onWidgetClick(): void {
    const LEADERBOARDBETURL = `${LEADERBOARD_WIDGET.LEADERBOARD_URL}/${this.bet.contestId}`;
    this.router.navigateByUrl('/', {skipLocationChange: true}).then(()=> {
      this.router.navigate([LEADERBOARDBETURL]);
    });
    this.rulesEntryService.trackGTMEvent(GTM_EVENTS.OPENBET.category,
      GTM_EVENTS.OPENBET.action, GTM_EVENTS.OPENBET.label);
  }
}
