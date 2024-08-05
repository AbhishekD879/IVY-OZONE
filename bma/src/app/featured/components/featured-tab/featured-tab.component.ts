import { ChangeDetectorRef, Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Location } from '@angular/common';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import * as _ from 'underscore';
import { switchMap } from 'rxjs/operators';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

import { IFeaturedModule } from './featured-module.model';
import { IInitialData } from './initial-data.model';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'featured-tab',
  templateUrl: './featured-tab.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedTabComponent extends AbstractOutletComponent implements OnInit {
  isFeaturedTabShown: boolean;
  initialData: IInitialData;
  hubIndex: string | number;

  constructor(
    private nativeBridgeService: NativeBridgeService,
    private cms: CmsService,
    private location: Location,
    private router: Router,
    private windowRef: WindowRefService,
    public user: UserService,
    private activatedRoute: ActivatedRoute,
    private changeDetectorRef: ChangeDetectorRef

  ) { super(); 
  }

  ngOnInit() {
    this.activatedRoute.params.pipe(
      switchMap((params: Params) => {
        this.hubIndex = params['hubIndex'];
        this.initialData = null;
        this.isFeaturedTabShown = false;
        this.showSpinner();
        this.changeDetectorRef.detectChanges();
        return this.cms.getRibbonModule();
      })
    ).subscribe((data: IInitialData) => {
      const firstModule = data.getRibbonModule[0],
      firstModuleUrl = firstModule.url.substring(1);
      const queryParams = this.user.getJourneyParams(this.windowRef.nativeWindow.location.href);

      // TODO refactor this checks ASAP , redirects to first tabs are very strange
      if (this.location.path().indexOf('/home/eventhub') === -1 &&
        this.location.path() !== '/home/featured' &&
        firstModule.directiveName.toLowerCase() !== 'eventhub' &&
        firstModule.id !== 'tab-featured' && !this.user.canActivateJourney(queryParams)) {
        this.router.navigate([firstModuleUrl]);
      }

      this.initialData = data;

      const featuredModule: IFeaturedModule = _.find(this.initialData.getRibbonModule, { id: 'tab-featured' }),
        devices = featuredModule && featuredModule.devices ? featuredModule.devices : 'unknown',
        mobileOS = this.nativeBridgeService.getMobileOperatingSystem(),
        deviceMatch = !_.any(devices, device => device === mobileOS);

      if (deviceMatch && this.nativeBridgeService.hasOnFeaturedTabClicked()) {
        this.isFeaturedTabShown = false;
        this.nativeBridgeService.onFeaturedTabClicked();
      } else {
        this.isFeaturedTabShown = true;
      }

      this.hideSpinner();
      this.changeDetectorRef.detectChanges();
    }, () => {
      this.showError();
      this.hideSpinner();
      this.changeDetectorRef.detectChanges();
    });
  }
}
