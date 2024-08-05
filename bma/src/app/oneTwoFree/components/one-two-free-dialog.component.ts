import { Component, ViewChild, OnInit, ChangeDetectorRef, ElementRef, OnDestroy } from '@angular/core';
import { ModalComponent } from '@sharedModule/components/customModal/custom-modal.component';
import { DeviceService } from '@coreModule/services/device/device.service';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { CmsService } from '@app/core/services/cms/cms.service';

@Component({
  selector: 'one-two-free-dialog',
  templateUrl: './one-two-free-dialog.component.html',
  styleUrls: ['./one-two-free-dialog.component.scss']
})

export class OneTwoFreeDialogComponent extends ModalComponent implements OnInit, OnDestroy {
  @ViewChild('OneTwoFreeDialog', {static: false}) modal: ModalComponent;

  isMobile: boolean = true;
  errorMsg: string;

  constructor(
    elementRef: ElementRef,
    changeDetectorRef: ChangeDetectorRef,   
    private deviceService: DeviceService,
    private pubSubService: PubSubService ,
    private cmsService: CmsService,
    public serviceClosureService: ServiceClosureService, 
  ) {
    super(elementRef, changeDetectorRef);
    this.cmsService.getSystemConfig().subscribe((config: any) => {
      this.errorMsg = config.F2PERRORS['F2PError'] || '';
    });
  }

  ngOnInit(): void {
    this.isMobile = this.deviceService.isMobile;
    
    if (this.isMobile) {
      this.pubSubService.publish(this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, false);
    } else {
      this.pubSubService.publish(this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, true);
    }
  }

  ngOnDestroy(): void {
    this.isMobile && this.pubSubService.publish(this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, true);
  }

}
