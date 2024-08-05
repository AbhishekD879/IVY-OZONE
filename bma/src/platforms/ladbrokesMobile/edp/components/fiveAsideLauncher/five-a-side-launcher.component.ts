import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ITab } from '@app/core/models/tab.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'five-a-side-launcher',
  templateUrl: './five-a-side-launcher.component.html',
  styleUrls: ['./five-a-side-launcher.component.scss']
})
export class FiveAsideLauncherComponent {

  @Input() eventTabs: ITab[];
  @Input() showBanner: boolean = false;
  @Input() fiveASideTitle: string;
  @Input() fiveASideContent: string;
  private launcher: string = 'tab-5-a-side';
  constructor(private router: Router,
    private gtmService: GtmService) {
  }

  /**
   * To navigate to 5a side
   */
  onNavigate(): void {
    const fiveASideTab: ITab = this.eventTabs.find((tab:ITab) => tab.id === this.launcher);
    this.trackChangeStat();
    this.router.navigateByUrl(`${fiveASideTab.url}/pitch`);
    }

  /**
   * To Track Change stat
   */
  private trackChangeStat(): void {
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Build5ASide',
      eventLabel: 'Build'
    });
  }

}
