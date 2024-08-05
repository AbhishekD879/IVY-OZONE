import { Component, Input, OnInit } from '@angular/core';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ENTRY_CONFIRMATION, SHOWDOWN_CARDS } from '@app/fiveASideShowDown/constants/constants';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { Router } from '@angular/router';

@Component({
  selector: 'fiveaside-entry-confirmation',
  template: ``
})
export class FiveASideEntryConfirmationComponent implements OnInit {
  @Input() ecText: string;
  @Input() contestId: string;
  @Input() termsConditionTag? : string;
  readonly viewShowDown: string = ENTRY_CONFIRMATION.viewShowDown;
  entryConfirmTerms = ENTRY_CONFIRMATION.entryConfirmationTerms;
  slideUpClass: string = '';
  showEntryConfirmation: boolean = false;
  constructor(
    private window: WindowRefService,
    private gtmService: GtmService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if(this.termsConditionTag){
      this.entryConfirmTerms = this.termsConditionTag;
    }
    this.triggerSlideUp();
    this.gtmService.push('trackEvent', ENTRY_CONFIRMATION.loadViewEntry);
  }

  /**
   * TO navigate for fiveAside Url
   * @returns {void}
   */
  onNavigate(): void {
    this.trackChangeStat();
    this.router.navigate([SHOWDOWN_CARDS.LEADERBOARD_BASE_URL, this.contestId]);
  }

  /**
   * Trigger the slide up animation after 500ms
   * @returns { void }
   */
  private triggerSlideUp(): void {
    this.window.nativeWindow.setTimeout(() => {
      this.slideUpClass = ENTRY_CONFIRMATION.slideUpClassName;
    });
  }

  /**
   * Gtm Tracking For CTA Button
   * @returns {void}
   */
  private trackChangeStat(): void {
    this.gtmService.push('trackEvent', ENTRY_CONFIRMATION.ctaGtmTracking);
  }
}
