import { Component, OnDestroy, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Location } from '@angular/common';
import { Event, NavigationEnd, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import * as _ from 'underscore';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'football-tutorial-overlay',
  templateUrl: 'football-tutorial-overlay.component.html',
  styleUrls: ['football-tutorial-overlay.component.scss']
})
export class FootballTutorialOverlayComponent implements OnInit, OnDestroy {
  header: Element;
  homeBody: Element;
  footballOverlay: Element;
  mainFavouriteStar: Element;
  showTutorialTimer: number;
  runAnimationTimer: number;
  showBlockOverlayTimer: number;
  hideAnimatedElementTimer: number;
  showArr2Timer: number;
  textPanelAnimationTimer: number;
  isActive: boolean = false;
  arrShow: boolean;

  @ViewChild('topStar', {static: true}) topStar: ElementRef;

  private windowResizeListener: any;
  private windowOrientationChangeListener: any;
  private locationChangeListener: Subscription;
  private contentOverlayClassName: string = 'football-content-overlay';

  private showArr2Timeout: number = 4000;
  private textPanelAnimationTimeout: number = 9000;
  private showBlockOverlayTimeout: number = 10;
  private runAnimationTimeout: number = 400;
  private showTutorialTimeout: number = 2500;
  private hideAnimatedElementTimeout: number = 4000;

  private readonly title = 'footballTutorialOverlay';

  constructor(
    private windowRef: WindowRefService,
    private domTools: DomToolsService,
    private pubSubService: PubSubService,
    private storageService: StorageService,
    private userService: UserService,
    private deviceService: DeviceService,
    private location: Location,
    private rendererService: RendererService,
    private router: Router
  ) {
    this.header = this.domTools.HeaderEl;
  }

  ngOnInit(): void {

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SHOW_FOOTBALL_TUTORIAL, () => {
      if (!this.storageService.get('footballTutorial') && this.userService.status) {
        this.showTutorial();
      }
    });

    this.locationChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd && this.isActive && !this.isHomeUrl(event.url)) {
        this.destroyElement();
      }
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGIN, () => this.showTutorial());
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGOUT, () => this.hideTutorial());
  }

  ngOnDestroy(): void {
    this.destroyElement();
  }

  hideTutorial(): void {
    if (this.isActive) {
      this.destroyElement();
      this.rendererService.renderer.removeClass(this.footballOverlay, 'active');
      this.rendererService.renderer.removeClass(this.homeBody, this.contentOverlayClassName);
    }
  }

  private initElements(): void {
    this.homeBody = this.deviceService.isWrapper ?
                          this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');
    this.footballOverlay = this.windowRef.document.getElementById('football-tutorial-overlay');
    this.mainFavouriteStar = this.footballOverlay.querySelector('.favicons-area .main-panel');
  }

  private isHomeUrl(url: string): boolean {
    return url.indexOf('/football/matches') > -1 || url.indexOf('/football') > -1;
  }

  private showTutorial(): void {
    const isHomeURL = this.isHomeUrl(this.location.path());

    this.clearTimers();

    if (isHomeURL && this.deviceService.isMobile && !this.storageService.get('footballTutorial')) {
      this.initElements();
      this.rendererService.renderer.addClass(this.footballOverlay, 'active');
      this.rendererService.renderer.addClass(this.homeBody, this.contentOverlayClassName);

      this.updatePositions();

      this.showArr2Timer = this.windowRef.nativeWindow.setTimeout(() => {
        this.showAnimation('arr2', true);
      }, this.showArr2Timeout);

      this.textPanelAnimationTimer = this.windowRef.nativeWindow.setTimeout(() => {
        this.showAnimation('textPanel');
      }, this.textPanelAnimationTimeout);

      this.isActive = true;
      this.storageService.set('footballTutorial', true);

      this.windowResizeListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow,
        'resize', () => this.updatePositions());
      this.windowOrientationChangeListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow,
        'orientationchange', () => this.updatePositions());
    }
  }

  private updatePositions(): void {
    const landscapeView = this.windowRef.nativeWindow.innerWidth > this.windowRef.nativeWindow.innerHeight;
    const firstEvent = this.domTools.getOffset(
      this.windowRef.document.querySelector('.page-container .fav-icon-svg')
    );

    const minHeight = 200;
    const animateScrollDown = landscapeView ? 135 : 325; // first event position relative to top of the screen
    const starPosition = landscapeView ? 80 : 213; // star's position relative to top of the screen

    if (landscapeView) {
      this.rendererService.renderer.addClass(this.footballOverlay, 'landscape');
    } else {
      this.rendererService.renderer.removeClass(this.footballOverlay, 'landscape');
    }

    this.arrShow = landscapeView;

    if (firstEvent && firstEvent.top > minHeight) {
      this.domTools.scrollPageTop(firstEvent.top - animateScrollDown);
      this.domTools.css(this.mainFavouriteStar, { top: starPosition, left: firstEvent.left - 7 });
    } else {
      this.domTools.scrollPageTop(0);
    }

    if (!this.deviceService.isMobile) {
      this.hideTutorial();
    }
  }

  private clearTimers(): void {
    this.windowRef.nativeWindow.clearTimeout(this.showTutorialTimer);
    this.windowRef.nativeWindow.clearTimeout(this.runAnimationTimer);
    this.windowRef.nativeWindow.clearTimeout(this.showBlockOverlayTimer);
    this.windowRef.nativeWindow.clearTimeout(this.hideAnimatedElementTimer);
    this.windowRef.nativeWindow.clearTimeout(this.showArr2Timer);
    this.windowRef.nativeWindow.clearTimeout(this.textPanelAnimationTimer);
  }

  /**
   * Set animation for text blocks
   * @param {string} targetElement Add class to target element
   * @param {boolean} isAnimated Checks if animation need to switch on
   */
  private showAnimation(targetElement, isAnimated?: boolean): void {
    const elements = this.windowRef.document.querySelectorAll(`.${targetElement}`);

    _.each(elements, (element: HTMLElement) => {
      this.rendererService.renderer.addClass(element, 'show-block');
    });

    if (isAnimated) {
      this.animation();
    }
  }

  /**
   * Set animation for favourite sign
   */
  private animation(): void {
    const animatedElement: HTMLElement = this.footballOverlay.querySelector('.star-animation');
    const currentTarget = this.windowRef.document.querySelector('.main-panel .odds-fav-icon');
    const dropzone = this.domTools.getOffset(this.windowRef.document.querySelector('.header-panel .odds-fav-icon'));
    const iconArea = this.domTools.getOffset(this.windowRef.document.querySelector('.favicons-area'));
    const currentTargetPosition = {
      left: (this.mainFavouriteStar as HTMLElement).offsetLeft,
      top: (this.mainFavouriteStar as HTMLElement).offsetTop
    };
    const marginLeft = 5;
    const marginTop = 5;

    if (currentTarget) {
      this.showTutorialTimer = this.windowRef.nativeWindow.setTimeout(() => {
        this.rendererService.renderer.addClass(this.mainFavouriteStar.querySelector('.odds-fav-icon'), 'fav-active');

        this.domTools.setTranslate(
          animatedElement,
          currentTargetPosition.left + marginLeft,
          currentTargetPosition.top + marginTop + iconArea.top - this.domTools.getPageScrollTop(),
          1, 1
        );

        this.rendererService.renderer.setStyle(animatedElement, 'display', 'block');

        this.runAnimationTimer = this.windowRef.nativeWindow.setTimeout(() => {
          const topStarPosition = this.topStar.nativeElement.getBoundingClientRect().top - 7;
          this.domTools.setTranslate(animatedElement, dropzone.left, topStarPosition, 0.2, 0.2);
          this.showBlockOverlayTimer = this.windowRef.nativeWindow.setTimeout(() => {
            this.rendererService.renderer.addClass(this.footballOverlay.querySelector('.arr3'), 'show-block');
            this.rendererService.renderer.addClass(this.footballOverlay.querySelector('.header-panel'), 'show-block');
          }, this.showBlockOverlayTimeout);
        }, this.runAnimationTimeout);
      }, this.showTutorialTimeout);

      this.hideAnimatedElementTimer = this.windowRef.nativeWindow.setTimeout(() => {
        this.rendererService.renderer.setStyle(animatedElement, 'display', 'none');
      }, this.hideAnimatedElementTimeout);
    }
  }

  /**
   * Clear timeouts and unsync on destroy directive
   */
  private destroyElement(): void {
    if (this.homeBody) {
      this.rendererService.renderer.removeClass(this.homeBody, this.contentOverlayClassName);
    }

    this.pubSubService.unsubscribe(this.title);

    this.windowResizeListener && this.windowResizeListener();
    this.windowOrientationChangeListener && this.windowOrientationChangeListener();
    this.locationChangeListener && this.locationChangeListener.unsubscribe();
    this.clearTimers();
  }
}
