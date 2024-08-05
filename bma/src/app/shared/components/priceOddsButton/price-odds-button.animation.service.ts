import { Injectable } from '@angular/core';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { DeviceService } from '@core/services/device/device.service';
import { StorageService } from '@core/services/storage/storage.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '../../services/renderer/renderer.service';

@Injectable()
export class PriceOddsButtonAnimationService {

  maxBetsAmount: number;
  animatedElement: HTMLElement;
  currentTarget: HTMLElement;
  aniTimers: any[]; // Timers
  private aniTarget;

  constructor(private windowRef: WindowRefService,
              private betSlipSelectionsData: BetslipSelectionsDataService,
              private cmsService: CmsService,
              private deviceService: DeviceService,
              private storageService: StorageService,
              private domToolsService: DomToolsService,
              private rendererService: RendererService) {
    this.cmsService.getSystemConfig()
      .subscribe((result: ISystemConfig) => {
        this.maxBetsAmount = result.Betslip && Number(result.Betslip.maxBetNumber);
      });

    this.aniTarget = null;
    this.finishAnimation = this.finishAnimation.bind(this);
  }

  animate(eventArg): Promise<void> {
    this.animatedElement = document.querySelector('.bet-animation');
    this.currentTarget = eventArg.currentTarget;
    const dropzoneElement: any = document.querySelector('.user-bets');
    const dropzone = this.domToolsService.getOffset(dropzoneElement);
    this.aniTimers = [];

    if (this.deviceService.isMobileOrigin && this.animatedElement && this.currentTarget &&
      !this.currentTarget.classList.contains('active') && this.aniTarget !== this.currentTarget &&
      this.betSlipSelectionsData.count() < this.maxBetsAmount &&
      !this.storageService.get('overaskIsInProcess') && // can not add to betslip if overask in progress
      dropzone) {
      const scrollY = this.windowRef.nativeWindow.pageYOffset,
        currentTargetOffset = this.domToolsService.getOffset(this.currentTarget),
        space = 10,
        startPositionValue = `translate(${currentTargetOffset.left}px, ${currentTargetOffset.top - scrollY}px)`,
        endPositionValue = `translate(${(dropzone.left - space)}px,
          ${(dropzone.top - this.windowRef.nativeWindow.scrollY - space)}px) scale(.2, .2)`;

      this.aniTarget = this.currentTarget;
      document.addEventListener('scroll', this.finishAnimation);

      this.resetAnimation();

      this.aniTimers.push(setTimeout(() => {
        this.domToolsService.css(this.animatedElement, '-webkit-transform', startPositionValue);
        this.rendererService.renderer.addClass(this.animatedElement, 'bet-visible');

        this.aniTimers.push(setTimeout(() => {
          this.domToolsService.css(this.animatedElement, '-webkit-transform', endPositionValue);

          this.aniTimers.push(setTimeout(() => {
            this.finishAnimation();
          }, 460));
        }, 20));
      }, 20));
    }

    return Promise.resolve();
  }

  resetAnimation(): void {
    this.rendererService.renderer.removeClass(this.animatedElement, 'bet-visible');
    this.rendererService.renderer.removeAttribute(this.animatedElement, 'css');
  }

  finishAnimation(): void {
    document.removeEventListener('scroll', this.finishAnimation);
    while (this.aniTimers.length) {
      clearTimeout(this.aniTimers.pop());
    }
    if (this.aniTarget === this.currentTarget) {
      this.aniTarget = null;
      this.resetAnimation();
    }
  }
}
