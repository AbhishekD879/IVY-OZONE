import { async } from '@angular/core/testing';
import { Router } from '@angular/router';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Observable } from 'rxjs/Observable';
import { Campaign } from '@app/client/private/models/freeRideCampaign.model';
import * as _ from 'lodash';
import { CampaignEditComponent } from './campaign-edit.component';

describe('CampaignEditComponent', () => {
  let component: CampaignEditComponent;
  let campaignObj: Campaign;
  let freeRideAPIService;
  let dialogService: Partial<DialogService>;
  let router: Partial<Router>;
  let route;
  let keyValDiff;
  let elementRef;
  let date;

  beforeEach(async(() => {
    campaignObj = {
      name: 'Test Title',
      id: '45',
      displayFrom: date,
      displayTo: date,
      brand: 'ladbrokes',
      openBetCampaignId: 'lkl',
      optimoveId: 'kl6'
    } as any;

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    route = {
      snapshot: {
        paramMap: {
          get: (id: string) => {
            return 'id';
          }
        }
      }
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
      updateCampaign: jasmine.createSpy('postNewCampaign')
        .and.returnValue(Observable.of({ body: { id: 'testid' } })),
      getSingleCampaignData: jasmine.createSpy('getSingleCampaignData')
        .and.returnValue(Observable.of({ body: { id: 'testid', name: 'Test Title' } })),
      deleteCampaign: jasmine.createSpy('deleteCampaign').and.returnValue(Observable.of({})),
    };

    date = new Date().toISOString(),
      component = new CampaignEditComponent(
        dialogService as any,
        router as any,
        route as any,
        freeRideAPIService as any,
        keyValDiff,
        elementRef
      );

  }));



  it('should create', () => {
    expect(component).toBeTruthy();
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
    component.newCampaign = {} as any;
    component.newCampaign.displayFrom = new Date(date).toDateString();
    component.newCampaign.displayTo = new Date(date).toDateString();
    expect(component.isEndDateValid()).toEqual(true);
  });

  it('#actionHandler should call correct method', () => {
    spyOn(component, 'removeCampaign');
    component.actionsHandler('remove');
    expect(component.removeCampaign).toHaveBeenCalled();

    spyOn(component, 'saveCampaignChanges');
    component.actionsHandler('save');
    expect(component.saveCampaignChanges).toHaveBeenCalled();

    spyOn(component, 'revertCampaignChanges');
    component.actionsHandler('revert');
    expect(component.revertCampaignChanges).toHaveBeenCalled();
  });

  it('#actionHandler should do nothing if wrong event', () => {
    spyOn(component, 'removeCampaign');
    spyOn(component, 'saveCampaignChanges');
    spyOn(component, 'revertCampaignChanges');

    component.actionsHandler('test-event');
    expect(component.removeCampaign).not.toHaveBeenCalled();
    expect(component.saveCampaignChanges).not.toHaveBeenCalled();
    expect(component.revertCampaignChanges).not.toHaveBeenCalled();
  });

  it('#revertChanges should call #loadInitialData', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component.revertCampaignChanges();
    expect(component['loadInitialData']).toHaveBeenCalled();
  });

  it('#removeCampaign should remove Campaign', () => {
    component.newCampaign = campaignObj;
    component.removeCampaign();
    expect(freeRideAPIService.deleteCampaign).toHaveBeenCalledWith(campaignObj.id);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Remove Completed',
      message: `Campaign is Removed.`,
      closeCallback: jasmine.any(Function)
    });
    expect(router.navigate).toHaveBeenCalledWith(['free-ride/campaign']);
  });

  it('#saveCampaign should save Campaign', () => {
    spyOn<any>(component, 'finishCampaignCreation');
    component.actionButtons = jasmine.createSpyObj([
      'extendCollection'
    ]);
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
      questionnarie: {}
    };
    component.newCampaign = _.cloneDeep(expectResult) as any;
    component['saveCampaignChanges']();
    expect(freeRideAPIService.updateCampaign).toHaveBeenCalledWith(expectResult, true);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.newCampaign);
    expect(component['finishCampaignCreation']).toHaveBeenCalledWith();
  });

  it('finishCampaignCreation should show dialog', () => {
    component.newCampaign = campaignObj;
    component.finishCampaignCreation();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Save Completed',
      message: `Campaign is Created and Stored.`,
      closeCallback: jasmine.any(Function)
    });
    expect(router.navigate).toHaveBeenCalled();
  });

  it('checkDateChanged', () => {
    component.newCampaign = {} as any;
    component.existingCampaignDate = date;
    component.newCampaign.displayFrom = date;
    expect(component.checkDateChanged()).toEqual(false);
  });

  it('oninit', () => {
    spyOn<any>(component, 'loadInitialData');
    component.ngOnInit();
    expect(component['loadInitialData']).toHaveBeenCalled();
    expect(component.id).toBeDefined();
  });

  it('loadInitData', () => {
    spyOn<any>(component, 'setQuestionnarie');
    component.ngOnInit();
    component['loadInitialData']();
    component.newCampaign = {} as any;
    expect(freeRideAPIService.getSingleCampaignData).toHaveBeenCalledWith(component.id);
    component.newCampaign = campaignObj;
    const breadcrumbs = [{
      label: `Free Ride`,
      url: `/free-ride/campaign`
    }, {
      label: 'Test Title',
      url: `/free-ride/campaign/testid`
    }];
    expect(component.breadcrumbsData).toEqual(breadcrumbs);
    expect(component.newCampaign.questionnarie).toBeUndefined();
    expect(component['setQuestionnarie']).toHaveBeenCalled();

  });

  it('setQuestionnnaire', () => {
    component.newCampaign = {} as any;
    component.setQuestionnarie();
    component.newCampaign.questionnarie = {} as any;
    component.newCampaign.questionnarie.questions = [];
    component.newCampaign.questionnarie = {
      'questions': [
        {
          'questionId': 1,
          'quesDescription': '',
          'options': [
            {
              'optionId': 1,
              'optionText': ''
            },
            {
              'optionId': 2,
              'optionText': ''
            },
            {
              'optionId': 3,
              'optionText': ''
            }
          ],
          'chatBoxResp': ''
        },
        {
          'questionId': 2,
          'quesDescription': '',
          'options': [
            {
              'optionId': 4,
              'optionText': ''
            },
            {
              'optionId': 5,
              'optionText': ''
            },
            {
              'optionId': 6,
              'optionText': ''
            }
          ],
          'chatBoxResp': ''
        },
        {
          'questionId': 3,
          'quesDescription': '',
          'options': [
            {
              'optionId': 7,
              'optionText': ''
            },
            {
              'optionId': 8,
              'optionText': ''
            },
            {
              'optionId': 9,
              'optionText': ''
            }
          ],
          'chatBoxResp': ''
        }
      ],
      'summaryMsg': '',
      'welcomeMessage': '',
      'horseSelectionMsg': ''
    };

    expect(component.newCampaign.questionnarie).toBeDefined();
    expect(component.newCampaign.questionnarie.questions.length).toEqual(3);
  });

  it('isvalidModel should be true', () => {
    component.newCampaign = campaignObj;
    component.newCampaign.questionnarie = {
      'questions': [
        {
          'questionId': 1,
          'quesDescription': 'question1',
          'options': [
            {
              'optionId': 1,
              'proxyChoice': 1,
              'optionText': 'opt1'
            },
            {
              'optionId': 2,
              'proxyChoice': 2,
              'optionText': 'jjn'
            },
            {
              'optionId': 3,
              'proxyChoice': 2,
              'optionText': 'jbjkb'
            }
          ],
          'chatBoxResp': 'bjkbkj'
        },
        {
          'questionId': 2,
          'quesDescription': 'jj',
          'options': [
            {
              'optionId': 4,
              'proxyChoice': 4,
              'optionText': 'bjb'
            },
            {
              'optionId': 5,
              'proxyChoice': 5,
              'optionText': 'b'
            },
            {
              'optionId': 6,
              'proxyChoice': 5,
              'optionText': 'jb'
            }
          ],
          'chatBoxResp': 'j'
        },
        {
          'questionId': 3,
          'quesDescription': 'jbj',
          'options': [
            {
              'optionId': 7,
              'proxyChoice': 7,
              'optionText': 'jb'
            },
            {
              'optionId': 8,
              'proxyChoice': 8,
              'optionText': 'bjk'
            },
            {
              'optionId': 9,
              'proxyChoice': 8,
              'optionText': 'jb'
            }
          ],
          'chatBoxResp': 'nlkn'
        }
      ],
      'summaryMsg': 'jb',
      'welcomeMessage': 'welcome',
      'horseSelectionMsg': 'jbjnjy'
    },
      component.questionForm = {
        form: {
          value: component.newCampaign.questionnarie,
          valid: true
        }
      } as any;
    expect(component.isValidModel).toEqual(true);
  });

});
