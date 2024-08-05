import { async } from '@angular/core/testing';
import { Router } from '@angular/router';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Observable } from 'rxjs/Observable';
import { Campaign } from '@app/client/private/models/freeRideCampaign.model';
import * as _ from 'lodash';
import { CampaignCreateComponent } from './campaign-create.component';
import { BrandService } from '@app/client/private/services/brand.service';

describe('CampaignCreateComponent', () => {
  let component: CampaignCreateComponent;
  let campaignObj: Campaign;

  let freeRideAPIService;
  let dialogService: Partial<DialogService>;
  let router: Partial<Router>;
  let brandService: Partial<BrandService>;
  let date;

  beforeEach(async(() => {
    campaignObj = {
      name: 'Test Title',
      id: ''
    } as any;

    brandService = {
      brand: 'ladbrokes'
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
        closeCallback();
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ title, message, yesCallback }) => {
        yesCallback();
      })
    };

    freeRideAPIService = {
      postNewCampaign: jasmine.createSpy('postNewCampaign')
        .and.returnValue(Observable.of({ body: { id: 'testid' } })),
    };

    date = new Date().toISOString(),
      component = new CampaignCreateComponent(
        dialogService as any,
        router as any,
        freeRideAPIService as any,
        brandService as any
      );
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should create campaign object', () => {
    const expectResult = {
      name: '',
      displayFrom: '',
      displayTo: date,
      openBetCampaignId: '',
      optimoveId: '',
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: brandService.brand,
    };
    expect(component.newCampaign).toEqual(expectResult);
  });

  it('#ngOnInit: should  set breadcrumbs', () => {
    component.ngOnInit();
    const breadcrumbs = [{
      label: `Free Ride`,
      url: `/free-ride/campaign`
    }, {
      label: 'Create campaign',
      url: `/free-ride/campaign/create`
    }];
    expect(component.breadcrumbsData).toEqual(breadcrumbs);
  });

  it('handleDateUpdate should campaign date', () => {
    const startDate = date,
      endDate = date;
    component.newCampaign = campaignObj;
    component.handleDisplayDateUpdate({
      startDate: startDate,
      endDate: endDate
    });
    expect(component.newCampaign.displayFrom).toEqual(startDate);
    expect(component.newCampaign.displayTo).toEqual(endDate);
  });

  it('isEndDatevalid should be true', () => {
    component.newCampaign.displayFrom = new Date(date).toDateString();
    component.newCampaign.displayTo = new Date(date).toDateString();

    expect(component.isEndDateValid()).toEqual(true);
  });

  it('isvalidModel should be true', () => {
    const expectResult = {
      name: 'test1',
      displayFrom: date,
      displayTo: date,
      openBetCampaignId: '5678',
      optimoveId: '7890',
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: brandService.brand,
    };
    component.newCampaign = expectResult;
    expect(component.isValidModel()).toEqual(true);
  });

  it('#saveCampaign should save Campaign', () => {
    spyOn<any>(component, 'finishCampaignCreation');
    const expectResult = {
      name: 'test1',
      displayFrom: date,
      displayTo: date,
      openBetCampaignId: '5678',
      optimoveId: '7890',
      id: 'testid',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: brandService.brand,
    };
    component.newCampaign = _.cloneDeep(expectResult);
    component['saveCampaignChanges']();
    expect(freeRideAPIService.postNewCampaign).toHaveBeenCalledWith(expectResult);
    expect(component['finishCampaignCreation']).toHaveBeenCalledWith();
    // expect(component.campaignData).toEqual([campaignList[0]]);
  });

  it('finishCampaignCreation should show dialog', () => {
    component.finishCampaignCreation();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Save Completed',
      message: `Campaign is Created and Stored.`,
      closeCallback: jasmine.any(Function)
    });
    expect(router.navigate).toHaveBeenCalled();
  });

});
