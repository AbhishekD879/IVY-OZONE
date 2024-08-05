import { Component, OnDestroy, OnInit } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { StorageService } from '@core/services/storage/storage.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'stream-bet-tutorial-pop-up',
  templateUrl: './stream-bet-tutorial-pop-up.component.html',
  styleUrls: ['./stream-bet-tutorial-pop-up.component.scss']
})
export class StreamBetTutorialPopUpComponent implements OnInit, OnDestroy {
  popUpLoaded: boolean = true;
  homeBody: Element;
  streamBetTutorialConfig: ISystemConfig;
  streamBetTutorialConfigNative: ISystemConfig;
  isWrapper: boolean;
  isStreambetTutorialDisplayed: boolean;
  isCoral: boolean;
  constructor(private windowRefService: WindowRefService,
    private rendererService: RendererService,
    private deviceService: DeviceService,
    private cmsService: CmsService,
    private storageService: StorageService
    ) {
  }
  ngOnInit(): void {
    this.isCoral = environment.brand === 'bma';
    this.isStreambetTutorialDisplayed = this.storageService.get('StreambetTutorialDisplayed');
    if(!this.isStreambetTutorialDisplayed){
    this.storageService.set('StreambetTutorialDisplayed',true);
    this.isWrapper = this.deviceService.isWrapper;
    if(this.isWrapper){
      this.homeBody = this.windowRefService.document.querySelector('body')
      this.cmsService.getFeatureConfig('streamBetTutorialConfigNative').subscribe(streamBetTutorialConfigNative => {
        if (streamBetTutorialConfigNative) {
          this.streamBetTutorialConfigNative = streamBetTutorialConfigNative;
        }
      });
    }
    else{
      this.homeBody =  this.windowRefService.document.querySelector('html, body');
      this.cmsService.getFeatureConfig('streamBetTutorialConfig').subscribe(streamBetTutorialConfig => {
        if (streamBetTutorialConfig) {
          this.streamBetTutorialConfig = streamBetTutorialConfig;
        }
      }); 
    }
    if (this.homeBody) {
      this.rendererService.renderer.addClass(this.homeBody, 'tint-overlay-whole');
      this.rendererService.renderer.addClass(this.homeBody, 'stream-bet-tutorial-overlay');
    }
   }
  }
  closeTutorial(): void {
    this.popUpLoaded = false;
    if (this.homeBody) {
      this.rendererService.renderer.removeClass(this.homeBody, 'tint-overlay-whole');
      this.rendererService.renderer.removeClass(this.homeBody, 'stream-bet-tutorial-overlay');
    }
  }
  ngOnDestroy(): void {
    this.closeTutorial();
  }
}
