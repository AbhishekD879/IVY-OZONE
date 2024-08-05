import { Component, DoCheck, ElementRef, KeyValueDiffers, OnInit, ViewChild } from '@angular/core';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { Router, ActivatedRoute } from '@angular/router';
import { FreeRideAPIService } from '../services/free-ride.api.service';
import { Campaign, PotCreation } from '@root/app/client/private/models/freeRideCampaign.model';
import { NgForm } from '@angular/forms';
import * as _ from 'lodash';
import { SpotlightComponent } from '@root/app/timeline/post/spotlight/spotlight.component';

@Component({
  selector: 'app-campaign-edit',
  templateUrl: './campaign-edit.component.html',
  styleUrls: ['./campaign-edit.component.scss']
})
export class CampaignEditComponent implements OnInit, DoCheck {

  @ViewChild('questionForm') questionForm: NgForm;
  @ViewChild('actionButtons') actionButtons;
  @ViewChild(SpotlightComponent) spotlightComponentData: SpotlightComponent;
  public breadcrumbsData: Breadcrumb[];
  public newCampaign: Campaign;
  // public questionnarie: any = {};
  public existingCampaignDate: string;
  public campaignPotsData: PotCreation;
  private campaignDataDiff: any;
  id: string;
  public campaignPotsDataCopy: PotCreation = {} as PotCreation;
  constructor(
    private dialogService: DialogService,
    private router: Router,
    private route: ActivatedRoute,
    private freeRideAPIService: FreeRideAPIService,
    private keyValDiff: KeyValueDiffers,
    private elementRef: ElementRef
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }
  isloading = false;
  dataChanged = false;
  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
    console.log(this.elementRef.nativeElement.querySelector('div'));
  }

  /**
   *Initial Data Load for Edit
   */
  loadInitialData() {
    this.freeRideAPIService.getSingleCampaignData(this.id).subscribe(data => {
      this.newCampaign = data.body;
      console.log(this.newCampaign);
      this.isloading = true;
      this.existingCampaignDate = data.body?.displayFrom;
      if (data.body?.questionnarie) {
        this.newCampaign.questionnarie = data.body?.questionnarie;
      } else {
        this.setQuestionnarie();
      }
      this.campaignPotsData = {} as PotCreation;
      this.campaignPotsData = JSON.parse(JSON.stringify(data.body?.eventClassInfo));
      this.campaignPotsDataCopy = JSON.parse(JSON.stringify(data.body?.eventClassInfo));
      this.breadcrumbsData = [{
        label: `Free Ride`,
        url: `/free-ride/campaign`
      }, {
        label: this.newCampaign.name,
        url: `/free-ride/campaign/${this.newCampaign.id}`
      }];
    });
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleDisplayDateUpdate(data: DateRange): void {
    console.log(data);
    this.newCampaign.displayFrom = data.startDate;
    this.newCampaign.displayTo = data.endDate;
  }

  /**
   * Button Actions Handler
   */
  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeCampaign();
        break;
      case 'save':
        this.saveCampaignChanges();
        break;
      case 'revert':
        this.revertCampaignChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
  * Campaign Create/Update
  */
  saveCampaignChanges() {
    this.newCampaign.eventClassInfo = this.campaignPotsData;
    const flag: boolean = this.checkDateChanged();
    this.freeRideAPIService.updateCampaign(this.newCampaign, flag).subscribe(data => {
      this.newCampaign = data.body;
      this.campaignPotsData = data.body?.eventClassInfo;
      this.campaignPotsDataCopy = JSON.parse(JSON.stringify(data.body?.eventClassInfo));
      this.isEqualCollection();
      this.actionButtons.extendCollection(this.newCampaign);
      this.finishCampaignCreation();
    });
  }

  /**
  * Date Check for existing campaign
  */
  checkDateChanged() {
    return new Date(this.existingCampaignDate).toISOString().substring(0, 10)
      !== new Date(this.newCampaign.displayFrom).toISOString().substring(0, 10);
  }

  /**
   * Date Check for past dates
   */
  isPastDate() {
    return (new Date(this.newCampaign.displayFrom).toISOString().substring(0, 10)
      < new Date().toISOString().substring(0, 10)) ||
      (new Date(this.newCampaign.displayTo).toISOString().substring(0, 10)
        < new Date().toISOString().substring(0, 10));
  }


  /**
  * button disabled check
  */
  isValidModel(campaign): boolean {
    return this.isEndDateValid() && !this.isPastDate() && this.isQuesFormValid() && !campaign.isPotsCreated;
  }

  /**
  * Question Form valid check
  */
  isQuesFormValid() {
    if (this.questionForm?.form.dirty) {
      return this.questionForm?.form.valid;
    }
    return true;
  }

  /**
   * On campaign create Completion
   */
  finishCampaignCreation() {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Campaign is Created and Stored.',
      closeCallback() {
        self.router.navigate([`free-ride/campaign/${self.newCampaign.id}`]);
      }
    });
  }

  /**
 * Set Questions Initial Model
 */
  setQuestionnarie() {
    let optionId = 1;
    this.newCampaign.questionnarie = {} as any;
    this.newCampaign.questionnarie.questions = [];
    this.newCampaign.questionnarie.summaryMsg = '';
    this.newCampaign.questionnarie.welcomeMessage = '';
    this.newCampaign.questionnarie.horseSelectionMsg = '';
    for (let i = 1; i <= 3; i++) {
      const question = {
        questionId: i,
        quesDescription: '',
        chatBoxResp: '',
        options: [],
      };
      for (let j = 1; j <= 3; j++) {
        const option = {
          optionId: optionId,
          optionText: ''
        };
        question.options.push(option);
        optionId++;
      }
      this.newCampaign.questionnarie.questions.push(question);
    }
  }

  /**
  * Campaign Revert changes
  */
  revertCampaignChanges() {
    this.loadInitialData();
    this.spotlightComponentData.getRelatedEvents();
  }


  /**
  * Campaign Remove
  */
  removeCampaign(): void {
    const self = this;
    if (this.newCampaign.isPotsCreated && this.isCampaignActive(this.newCampaign)) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Campaign',
        message: 'Active campaign cannot be deleted'
      });
    } else {
      this.freeRideAPIService.deleteCampaign(this.newCampaign.id)
        .subscribe((data: any) => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Campaign is Removed.',
            closeCallback() {
              self.router.navigate(['free-ride/campaign']);
            }
          });
        });
    }
  }

  /**
   * End Date Valid Check
   */
  isEndDateValid(): boolean {
    const displayFromDate = new Date(this.newCampaign.displayFrom).toDateString();
    const displayToDate = new Date(this.newCampaign.displayTo).toDateString();
    return displayFromDate === displayToDate;
  }

  /**
   * Checks if campaign is active
   */
  isCampaignActive(campaign: Campaign): boolean {
    return (new Date().toDateString()) === (new Date(campaign.displayTo).toDateString()) &&
      (new Date(campaign.displayTo)).getTime() > (new Date()).getTime();
  }

  /**
    * Selected Race events by user
    */
  getSelectedRaces(event: PotCreation) {
    this.campaignPotsData = event;
    this.isEqualCollection();
    if (event.marketPlace && event.marketPlace.length > 0) {
      this.newCampaign.eventClassInfo.marketPlace = JSON.parse(JSON.stringify(event.marketPlace));
    }
    this.campaignDataDiff = this.keyValDiff.find(this.campaignPotsData.marketPlace).create();
  }

  /**
  * Create Pots
  */
  createPotstoCampaign(event: boolean) {
    if (event) {
      this.freeRideAPIService.createPots(this.newCampaign.id)
        .subscribe(() => {
          this.newCampaign.isPotsCreated = true;
          this.dialogService.showNotificationDialog({
            title: 'Pots Created',
            message: 'Pots to Campaign level are created',
          });
        });
    }
  }

  ngDoCheck() {
    const campDataArrChanges = this.campaignDataDiff?.diff(this.campaignPotsData?.marketPlace);
    if (campDataArrChanges) {
      this.newCampaign.eventClassInfo = this.campaignPotsData;
    }
  }

  validateQuestions(): boolean {
    if (this.newCampaign?.questionnarie) {
      return this.newCampaign?.questionnarie.questions.length === 3 &&
        this.isValidQuetsion(this.newCampaign?.questionnarie.questions).length === 3 &&
        this.newCampaign?.questionnarie.summaryMsg !== '' &&
        this.newCampaign?.questionnarie.welcomeMessage !== '' &&
        this.newCampaign?.questionnarie.horseSelectionMsg !== '';
    } else {
      return false;
    }
  }

  isValidQuetsion(questions) {
    return questions.filter(ques => {
      return ques.quesDescription !== '' && ques.chatBoxResp !== '' && this.isValidOptions(ques.options).length === 3;
    });
  }

  isValidOptions(opts) {
    return opts.filter(opt => {
      return opt.optionText !== '';
    });
  }
  /**
   * create pots button  disabled check
   */
  createPotsValidationOnDateTime(): boolean {
    const sixHoursPrior = new Date().setHours(new Date(this.newCampaign?.displayFrom).getHours() - 6);
    if ((new Date(this.newCampaign?.displayFrom).getTime() < new Date().getTime() ||
      new Date(this.newCampaign?.displayFrom).setHours(0, 0, 0, 0) > new Date().setHours(0, 0, 0, 0) ||
      (new Date().getTime() < new Date(sixHoursPrior).getTime()))) { // Pot creation allowed 6 hrs bfore campaign start dtae
      return true;
    } else {
      return false;
    }
  }

  /**
  * create pots button  disabled check
  */
  isEqualCollection() {
    this.dataChanged = _.isEqual(this.campaignPotsData?.marketPlace, this.campaignPotsDataCopy?.marketPlace)
      && this.campaignPotsData?.marketPlace.length > 0;
  }
}
