import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  HostListener,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
  SimpleChanges
} from '@angular/core';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
@Component({
  selector: 'drawer',
  templateUrl: './drawer.component.html',
  styleUrls: ['./drawer.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DrawerComponent implements OnInit, OnChanges, OnDestroy {
  @Input() show: boolean;
  @Input() hideHeader: boolean;
  @Input() position: 'top' | 'bottom' | 'left' | 'right' = 'bottom';
  @Input() contentStyle: {[key: string]: any} = {};
  @Input() relativeToParent: boolean = false;
  @Input() contentClass: string;
  @Input() lockBodyScroll: boolean = true;
  @Input() showCloseButton: boolean = true;
  @Input() showOverlay: boolean = true;
  @Input() removeBodyClassOnClose: boolean = true;
  @Input() background?: string;
  @Input() showFallbackMessage: boolean;

  @Output() readonly hide = new EventEmitter<void>();
  @Output() readonly shown = new EventEmitter<void>();
  @Output() readonly hidden = new EventEmitter<void>();

  visible: boolean;
  active: boolean;
  isRPverdict = false;
  isCoralMobile = false;
  private animationDuration = 300;
  private scrollPosition: number;

  constructor(
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    protected deviceService: DeviceService,
    protected changeDetector: ChangeDetectorRef,
    protected pubSubService: PubSubService
  ) {

  }

  ngOnInit(): void {
    this.isCoralMobile = environment.brand === 'bma' && environment.CURRENT_PLATFORM === 'mobile';
    if (this.show) {
      this.showDrawer();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if ('show' in changes) {
      if (this.show) {
        this.showDrawer();
        if (this.contentClass && this.contentClass.includes('verdict-nw')) {
          this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', true);
          this.isRPverdict = true;
        }
      } else {
        this.hideDrawer();
        if (this.contentClass && this.contentClass.includes('verdict-nw')) {
          this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
          this.isRPverdict = true;
        }
      }
    }
  }

  ngOnDestroy(): void {
    this.removeBodyClassOnClose && this.toggleBodyClass(false);
    this.isRPverdict = false;
  }

  showDrawer(): void {
    if (this.visible) {
      return;
    }

    this.saveScrollPosition();
    this.toggleBodyClass(true);

    this.visible = true;

    const domDelay = 100;

    // wait when DOM is rendered
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.active = true;
      this.changeDetector.markForCheck();
    }, domDelay);

    // wait when animation completed
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.shown.next();
    }, domDelay + this.animationDuration);
  }

  hideDrawer(): void {
    if (!this.visible) {
      return;
    }

    this.active = false;

    // wait when animation completed
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.visible = false;
      this.removeBodyClassOnClose && this.toggleBodyClass(false);
      this.restoreScrollPosition();
      this.hidden.next();
      this.changeDetector.markForCheck();
    }, this.animationDuration);
  }

  overlayClick(): void {
    this.hide.next();
  }

  closeClick(): void {
    this.hide.next();
  }

  @HostListener('document:keyup.esc')
  escPress(): void {
    this.hide.next();
  }

  private toggleBodyClass(state: boolean): void {
    // handle this only if drawer is shown on the whole page
    // if is relative to Parent blocking scroll of body is no required
    if (!this.relativeToParent && this.lockBodyScroll) {
      this.domToolsService.toggleClass(
        this.windowRefService.document.body,
        this.deviceService.isTouch ? 'drawer-visible-touch' : 'drawer-visible',
        state
      );
    }
  }

  private saveScrollPosition(): void {
    if (this.deviceService.isTouch) {
      this.scrollPosition = this.domToolsService.getPageScrollTop();
    }
  }

  private restoreScrollPosition(): void {
    if (this.deviceService.isTouch) {
      this.domToolsService.scrollPageTop(this.scrollPosition);
    }
  }
}
