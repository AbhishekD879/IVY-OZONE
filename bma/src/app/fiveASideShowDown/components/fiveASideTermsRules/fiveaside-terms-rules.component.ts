import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  SecurityContext
} from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { forkJoin } from 'rxjs';
import { IFAQ } from '@core/services/cms/models/frequently-asked-question';
import { ITermsAndConditions } from '@core/services/cms/models/terms-and-conditions';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';
import { RULES_TABS, REMOVE_ELEMENTS, GTM_EVENTS } from '@app/fiveASideShowDown/constants/constants';
import { RULES_TAB } from '@app/fiveASideShowDown/constants/enums';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IEventDetails, IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { FiveasideRulesEntryAreaService
} from '@fiveASideShowDownModule/services/fiveaside-rules-entry-area.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { FiveASideCmsService } from '@app/fiveASideShowDown/services/fiveaside-cms.service';

@Component({
  selector: 'fiveaside-terms-rules',
  template: ``
})
export class FiveasideTermsRulesComponent implements OnInit {
  @Input() eventEntity: IEventDetails;
  @Input() showDown: IShowDown;
  @Input() baseClass: string;
  @Input() hasTeamImage: boolean;
  @Input() teams: ITeamColor[];
  @Output() readonly clearOverlay = new EventEmitter();
  @Input() leaderboardData: IShowDown; 

  public tabs: ITab[] = RULES_TABS;
  public activeTab: ITab;
  public faqs: IFAQ[] = [];
  public termsConditions: ITermsAndConditions;
  public staticBlockTerms: string;
  public homeTeam: string;
  public awayTeam: string;
  public homeIcon: string;
  public awayIcon: string;
  public prizePoolData: IPrize;
  public readonly removeElements = REMOVE_ELEMENTS;
  public readonly RULES = RULES_TAB;
  protected readonly CONTEST_OVERLAY_CLASS_NAME: string = 'fiveasideentry-rules-overlay';
  protected readonly RULES_OVERLAY_ID: string = 'fiveaside-terms-rules';
  protected overlay: HTMLElement;
  protected baseOverlayElement: HTMLElement;

  constructor(protected cmsService: FiveASideCmsService,
    protected rendererService: RendererService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected domSanitizer: DomSanitizer,
    protected gtmService: GtmService,
    protected rulesEntryService: FiveasideRulesEntryAreaService) { }

  ngOnInit(): void {
    [this.activeTab] = this.tabs;
    this.eventEntity = this.showDown.eventDetails;
    const eventName: string = this.eventEntity.name.replace(/[|,]/g, '');
    [this.homeTeam, this.awayTeam] = eventName.split(/ v | vs | - /);
    this.homeIcon = this.rulesEntryService.formFlagName(this.homeTeam);
    this.awayIcon = this.rulesEntryService.formFlagName(this.awayTeam);
    this.overlay = this.windowRef.document.getElementById(this.RULES_OVERLAY_ID);
    this.validateBaseElement();
    this.getCMSData();
    this.initOverlayElements();
    this.prizePoolData = this.leaderboardData.prizeMap;
  }

  /**
   * Triggered when tab is switched
   * @param event
   * @returns {void}
   */
  switchTab(event: { id: string; tab: ITab }): void {
    this.activeTab = event.tab;
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side Showdown',
      eventAction: 'click',
      eventLabel: this.activeTab.title
    });
    this.faqs.forEach((faq: IFAQ) => faq.isExpanded = false);
  }

  /**
   * Triggered when overlay x svg icon is clicked
   * @returns {void}
   */
  onCloseRulesOverlay(): void {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.clearOverlay.emit();
  }

  /**
   * To track every question
   * @param {number} index
   * @returns {void}
   */
  faqHandler(index: number): void {
    this.faqs[index].isExpanded = !this.faqs[index].isExpanded;
    if (this.faqs[index].isExpanded) {
      this.gtmService.push('trackEvent', {
        eventCategory: GTM_EVENTS.FAQ.category,
        eventAction: GTM_EVENTS.FAQ.action,
        eventLabel: this.faqs[index].question
      });
    }
  }

  /**
   * Initialize Overlay Elements
   * @returns {void}
   */
  protected initOverlayElements(): void {
    this.rendererService.renderer.addClass(this.overlay, 'active');
    this.rendererService.renderer.addClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
  }

  /**
   * To fetch Rules/FAQS from CMS
   * @returns {void}
   */
  private getCMSData(): void {
    forkJoin(this.cmsService.getFAQs(),
      this.cmsService.getTermsAndConditions()
    ).subscribe((response: [IFAQ[], ITermsAndConditions]) => {
      [this.faqs, this.termsConditions] = response;
      this.setTermsConditions();
    }, (error) => {
      console.warn(error);
    });
  }
  

  /**
   * To set terms and conditions block
   * @returns {void}
   */
  private setTermsConditions(): void {
    if (this.termsConditions && this.termsConditions.text) {
      this.staticBlockTerms = this.domSanitizer.sanitize(SecurityContext.NONE,
            this.domSanitizer.bypassSecurityTrustHtml(this.termsConditions.text));
    }
  }

  /**
   * To Validate base element based on input
   * @returns {void}
   */
  private validateBaseElement(): void {
    if (this.baseClass) {
      this.baseOverlayElement = this.windowRef.document.querySelector(this.baseClass);
    } else {
      this.baseOverlayElement = this.deviceService.isWrapper ?
        this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');
    }
  }

}
