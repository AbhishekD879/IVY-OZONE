import { Component, OnInit, Input } from '@angular/core';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { DomSanitizer } from '@angular/platform-browser';
import { IYourCallStaticBlock } from '@core/services/cms/models';

@Component({
  selector: 'your-call-static-block',
  templateUrl: 'your-call-static-block.component.html'
})
export class YourCallStaticBlockComponent implements OnInit {
  @Input() staticType: string;
  @Input() showIcon: boolean;
  @Input() trustAsHtml: boolean;
  @Input() minHeightByb ?:boolean;

  staticBlock: IYourCallStaticBlock;

  constructor(
    private yourCallService: YourcallService,
    private domSanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.yourCallService.getStaticBlocks().then(() => {
      const staticType = this.staticType || this.yourCallService.keys.page;
      this.staticBlock = this.yourCallService.getStaticBlock(staticType);
      if (this.trustAsHtml) {
        if (typeof this.staticBlock.htmlMarkup === 'string') {
          this.staticBlock.htmlMarkup = this.domSanitizer.bypassSecurityTrustHtml(this.staticBlock.htmlMarkup);
        }
      }
    });
  }
}


