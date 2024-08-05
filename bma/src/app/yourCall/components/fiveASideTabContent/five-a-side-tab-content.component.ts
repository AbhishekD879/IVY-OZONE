import { Component, OnInit, SecurityContext, HostListener, Input, OnDestroy } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { DomSanitizer } from '@angular/platform-browser';
import { IStaticBlock } from '@app/core/services/cms/models';
import { Router, ActivatedRoute } from '@angular/router';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { FiveASideBetService } from '@yourcall/services/fiveASideBet/five-a-side-bet.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'five-a-side-tab-content',
  templateUrl: './five-a-side-tab-content.component.html',
  styleUrls: ['./five-a-side-tab-content.component.scss'],
})

export class FiveASideTabContentComponent implements OnInit, OnDestroy {
  @Input() eventEntity: ISportEvent;

  staticBlockContent: string;
  showPitch: boolean = false;
  isLoaded: boolean = false;
  cmsDown: boolean = false;

  private focusOutListener: Function;

  constructor(
    private cmsService: CmsService,
    private domSanitizer: DomSanitizer,
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private activatedRoute: ActivatedRoute,
    public fiveASideBet: FiveASideBetService,
    public fiveASideService: FiveASideService,
    private gtmService: GtmService,
    private windowRefService: WindowRefService,
    private domToolsService: DomToolsService,
    private deviceService: DeviceService,
    private pubsub: PubSubService
  ) { }

  ngOnInit(): void {
    this.getStaticBlock();
    this.showPitch = this.activatedRoute.snapshot.children[0] && this.activatedRoute.snapshot.children[0].paramMap.get('pitch') === 'pitch';
    this.onCloseIosKeyboardListener();
    this.pubsub.subscribe('FIVE_A_SIDE_TAB_COMPONENT', 'SHOW_FIVE_A_SIDE', (show: boolean) => {
      this.showPitch = show;
    });
  }

  ngOnDestroy(): void {
    this.focusOutListener && this.focusOutListener();
    this.fiveASideService.hideView();
    this.pubsub.unsubscribe('FIVE_A_SIDE_TAB_COMPONENT');
  }

  /**
   * should open pitch view
   */
  @HostListener('click', ['$event'])
  @HostListener('touchstart', ['$event'])
  onClick(event: MouseEvent): void {
    const target: HTMLElement = event.target as HTMLElement;
    if (target && target.className === 'build') {
      event.preventDefault();
      const url = this.routingHelperService.formEdpUrl(this.eventEntity);
      this.showPitch = true;
      this.router.navigate([`/${url}/5-a-side/pitch`]);
      this.gtmService.push('trackEvent', {
       eventCategory: '5-A-Side',
       eventAction: 'Build',
       eventLabel: '/5-a-side'
      });
    }
  }

  /**
   * Reload data
   */
  reloadState() {
    this.isLoaded = false;
    this.cmsDown = false;
    this.getStaticBlock();
  }

  private getStaticBlock(): void {
    this.cmsService.getStaticBlock('five-a-side-launcher').subscribe((cmsContent: IStaticBlock) => {
      this.isLoaded = true;
      this.staticBlockContent =
        this.domSanitizer.sanitize(SecurityContext.NONE, this.domSanitizer.bypassSecurityTrustHtml(cmsContent.htmlMarkup));
    }, () => {
        this.isLoaded = true;
        this.cmsDown = true;
    });
  }

  /**
   * iOS keyboard close listener to fix iOS tablet keyboard specific issue(only for tablets)
   */
  private onCloseIosKeyboardListener(): void {
    if (this.deviceService.isIos && this.deviceService.isTablet) {
      this.focusOutListener = this.windowRefService.nativeWindow.addEventListener('focusout', () => {
        this.domToolsService.scrollPageTop(0);
      });
    }
  }
}
