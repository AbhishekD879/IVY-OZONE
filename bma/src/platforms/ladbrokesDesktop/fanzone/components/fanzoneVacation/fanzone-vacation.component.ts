import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FanzoneAppVacationComponent } from '@app/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { CmsService } from '@app/core/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { WindowRef } from '@frontend/vanilla/core';
@Component({
  selector: 'fanzone-vacation',
  templateUrl: '../../../../../app/fanzone/components/fanzoneVacation/fanzone-vacation.component.html',
  styleUrls: ['../../../../../app/fanzone/components/fanzoneVacation/fanzone-vacation.component.scss'],
})
export class FanzoneVacationDesktopComponent extends FanzoneAppVacationComponent implements OnInit {
  constructor(    
    protected cms: CmsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected device: DeviceService,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected windowRef: WindowRef
    ) {
    super(cms, changeDetectorRef, device, fanzoneModuleService, windowRef);
  }
  
  ngOnInit(): void {
    super.ngOnInit();
  }
}