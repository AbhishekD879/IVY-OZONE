import { async } from '@angular/core/testing';
import { Router } from '@angular/router';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Observable } from 'rxjs/Observable';
import {Campaign } from '@app/client/private/models/freeRideCampaign.model';
import * as _ from 'lodash';
import { CampaignListComponent } from './campaign-list.component';

describe('CampaignListComponent', () => {
  let component: CampaignListComponent;

  let campaignList: Campaign[];

  let freeRideAPIService;
  let dialogService: Partial<DialogService>;
  let router: Partial<Router>;
  let globalLoaderService: Partial<GlobalLoaderService>;

  beforeEach(async(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
      .callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };
   
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

     freeRideAPIService = {
      getCampaignsByBrandWithOrdering: jasmine.createSpy('getCampaignsByBrandWithOrdering')
      .and.returnValue(Observable.of({ body: campaignList })),
      deleteCampaign: jasmine.createSpy('deleteCampaign').and.returnValue(Observable.of({})),
    };

    campaignList = [{
      id: 1,
      name: 'campaign1'
    }, {
      id: 2,
      name: 'campaign2'
    }
  ] as any;
    component = new CampaignListComponent(
      router as any,
      dialogService as any,
      freeRideAPIService as any,
      globalLoaderService as any
    );
  }));

  it('#should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit: should  call loadCampaigns', () => {
    spyOn<any>(component, 'loadCampaigns');
    component.ngOnInit();
    expect(component['loadCampaigns']).toHaveBeenCalled();
  });

  it('#loadCampaigns should get campaign list', () => {
    component['loadCampaigns']();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(freeRideAPIService.getCampaignsByBrandWithOrdering).toHaveBeenCalledWith('createdAt,desc');
    expect(component.campaignData).toEqual(campaignList);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#loadCampaigns should handle error when get campaign list', () => {
    freeRideAPIService.getCampaignsByBrandWithOrdering.and.returnValue(Observable.throw({}));
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.campaignData).not.toEqual(campaignList);
  });

  it('#removeCampaign should show dialog', () => {
    spyOn<any>(component, 'sendRemoveRequest');
    component.campaignData = _.cloneDeep(campaignList);
    const targetCampaign: Campaign = campaignList[1];

    component.removeCampaign(targetCampaign);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Remove Campaign',
      message: `Are You Sure You Want to Remove Campaign?`,
      yesCallback: jasmine.any(Function)
    });
    expect(component['sendRemoveRequest']).toHaveBeenCalledWith(targetCampaign);
    // expect(apiClientService.footballCoupon().remove).toHaveBeenCalledWith(targetCoupon.id);
    // expect(component.couponSegments).toEqual([couponList[0]]);
  });

  it('#removeCampaign should remove Campaign', () => {
    component.campaignData = _.cloneDeep(campaignList);
    const targetCampaign: Campaign = campaignList[1];
    component['sendRemoveRequest'](targetCampaign);
    expect(freeRideAPIService.deleteCampaign).toHaveBeenCalledWith(targetCampaign.id);
    expect(component.campaignData).toEqual([campaignList[0]]);
  });

  it('#addNewCampaign should navigate to new page', () => {
    component.openCreateCampaign();
    expect(router.navigateByUrl).toHaveBeenCalledWith('free-ride/campaign/create');
  });
});
