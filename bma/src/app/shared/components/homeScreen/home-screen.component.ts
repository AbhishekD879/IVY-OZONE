import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { Component, OnInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';

/**
 * Removes Splash screen after application is loaded.
 * Should be applied to #home-screen element
 */
@Component({
  selector: 'home-screen',
  templateUrl: 'home-screen.component.html',
  styleUrls: ['home-screen.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeScreenComponent implements OnInit, OnDestroy {

  private RENDER_DELAY: number = 200;
  private resizeListener: Function;
  private orientationChangeListener: Function;
  private readonly title = 'HomeScreenComponent';
  streamBetVideoMode: boolean;

  constructor(
    private rendererService: RendererService,
    private pubsub: PubSubService,
    private windowRef: WindowRefService,
    private device: DeviceService,
    private domTools: DomToolsService,
    private nativeBridgeService: NativeBridgeService,
    private sessionstorageService: SessionStorageService
  ) {}

  ngOnInit(): void {
    if (this.device.isMobile) {
      this.onWindowResize();
    }

    this.pubsub.subscribe(this.title, this.pubsub.API.APP_IS_LOADED, (isHide: boolean) => {
      const spashScreen = this.windowRef.document.getElementById('home-screen');
      if (spashScreen && isHide) {
        spashScreen.style.display = 'none';
        this.nativeBridgeService.pageLoaded();
      }
    });

    if (!this.device.isMobile) { return; }

    this.resizeListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'resize',
      () => this.orientationChangeHandler());
    this.orientationChangeListener = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'orientationchange',
      () => this.orientationChangeHandler());

    if (this.device.isWrapper && this.device.isAndroid) {
      this.pubsub.subscribe(this.title, this.pubsub.API.ORIENTATION_CHANGED, orientation => {
        this.onWindowResize();
      });
    }
  }

  ngOnDestroy() {
    this.pubsub.unsubscribe(this.title);
    this.resizeListener && this.resizeListener();
    this.orientationChangeListener && this.orientationChangeListener();
  }


  private orientationChangeHandler(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.onWindowResize();
    }, this.RENDER_DELAY);
  }

  private onWindowResize(): void {
    const snbContainer = this.windowRef.nativeWindow.document.querySelector('.snb-video-container');
    if (this.isLandscape && !snbContainer) {
      this.rendererService.renderer
        .addClass(this.windowRef.nativeWindow.document.querySelector('.landscape-mobile-overlay'), 'landscape-mode');
      this.rendererService.renderer
        .addClass(this.windowRef.document.body, 'mobile-overlay-active');
      this.windowRef.nativeWindow.document.activeElement.blur();
    } else {
      this.domTools.removeClass(this.windowRef.nativeWindow.document.querySelector('.landscape-mobile-overlay'), 'landscape-mode');
      this.rendererService.renderer.removeClass(this.windowRef.document.body, 'mobile-overlay-active');
    }
  }

  private get isLandscape(): boolean {
    return (this.windowRef.nativeWindow.orientation === 90 || this.windowRef.nativeWindow.orientation === -90);
  }
  private set isLandscape(value:boolean){}
}
