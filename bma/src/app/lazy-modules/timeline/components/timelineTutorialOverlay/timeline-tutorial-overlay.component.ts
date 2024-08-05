import {
  Component,
  OnDestroy,
  OnInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  ViewChild,
  ElementRef,
  Input,
} from '@angular/core';

import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Subscription } from 'rxjs';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@core/services/storage/storage.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ITimelineDetails } from '@core/services/cms/models/timeline-tutorial.model';
import { ITimelineSettings } from '@core/services/cms/models/timeline-settings.model';
import { TIMELINE_TUTORIAL } from '@lazy-modules/timeline/constants/timeline.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'timeline-tutorial-overlay',
  templateUrl: 'timeline-tutorial-overlay.component.html',
  styleUrls: ['timeline-tutorial-overlay.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TimelineTutorialOverlayComponent implements OnInit, OnDestroy {
  header: Element;
  activeTutorial: boolean = false;

  @Input() timelineSettings: ITimelineSettings;
  @Input() isBrandLadbrokes: boolean;
  @ViewChild('timelineTutorial', {static: false}) public timelineTutorialElement: ElementRef;

  public headerTitle: SafeHtml;
  public tltDetails: ITimelineDetails;
  private tltDetailsSub: Subscription;
  private title: string = 'timelineOverlay';
  isCoral: boolean;

  constructor(
    protected cms: CmsService,
    protected windowRef: WindowRefService,
    protected storageService: StorageService,
    protected rendererService: RendererService,
    protected domSanitizer: DomSanitizer,
    protected changeDetectorRef: ChangeDetectorRef,
    protected pubSubService: PubSubService
  ) {
    this.handleTimelineTutorialDisplay = this.handleTimelineTutorialDisplay.bind(this);
  }
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SHOW_TIMELINE_TUTORIAL, () => {
      this.handleTimelineTutorialDisplay();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
    this.removeTutorial();
  }

  /**
   * Handle displaying of timeline tutorial on current page
   * @param event  - Event
   */
  handleTimelineTutorialDisplay(): void {
    if (this.compareCampaignIds()) {
      this.showTutorial();
    } else {
      this.removeTutorial();
    }
  }

  showTutorial(): void {
    this.tltDetailsSub = this.cms.getTimelineTutorialDetails()
      .subscribe((details: ITimelineDetails) => {
        if (details && details.showSplashPage) { // Render tlt using actual cms settings CMS check
          this.tltDetails = details;
          this.headerTitle = this.tltDetails.text ? this.domSanitizer.bypassSecurityTrustHtml(this.tltDetails.text) : '';

          // save liveCampaignId to localStorage if it's exist, if not - will save null
          this.storageService.set(TIMELINE_TUTORIAL, {liveCampaignId: this.timelineSettings.liveCampaignId});
          this.activeTutorial = true;
          this.changeDetectorRef.detectChanges();
        } else {
          this.removeTutorial();
        }
      });
  }

  removeTutorial(): void {
    this.activeTutorial = false;
    this.tltDetailsSub && this.tltDetailsSub.unsubscribe();
    this.changeDetectorRef.markForCheck();
  }

  private compareCampaignIds(): boolean {
    const tlt: ITimelineSettings = this.storageService.get(TIMELINE_TUTORIAL);

    return this.timelineSettings && this.timelineSettings.enabled &&
      (!tlt || tlt.liveCampaignId !== this.timelineSettings.liveCampaignId);
  }
}
