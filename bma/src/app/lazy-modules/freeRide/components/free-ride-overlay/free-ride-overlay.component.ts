import { Component, ElementRef, OnInit, ViewChild, Input, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { PlatformLocation } from '@angular/common';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRoutingHelperEvent } from '@core/services/routingHelper/routing-helper.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { UserService } from '@core/services/user/user.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { FreeRideDomService } from '@lazy-modules/freeRide/services/freeRideDom.service';
import { FreeRideService } from '@lazy-modules/freeRide/services/freeRide.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import {
  IDOMData,
  IFreeRideCampaign,
  IOverlayData,
  IQuestionnarie,
  IQuestions,
  IRaceEvent,
  IUserAnswer,
  IUserSelectionDetail
} from '@lazy-modules/freeRide/models/free-ride';
import {
  FREE_RIDE_CONSTS,
  PROPERTY_TYPE,
  FREE_RIDE_HTML,
  HORSE_DATA_CONFIG,
  RESULT_DATA_CONFIG,
  FREE_RIDE_MESSAGES,
  HORSE_DATA_SUMMARY_CONFIG
} from '@lazy-modules/freeRide/constants/free-ride-constants';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'free-ride-overlay',
  templateUrl: './free-ride-overlay.component.html',
  styleUrls: ['./free-ride-overlay.component.scss']
})

export class FreeRideOverlayComponent implements OnInit {
  @Input() campaignData: IOverlayData;
  @Output() readonly freeRideClose = new EventEmitter();
  @ViewChild('ansAudioOption') ansAudioPlayerRef: ElementRef;
  @ViewChild('quesAudioOption') quesAudioPlayerRef: ElementRef;
  @ViewChild('resultAudioOption') resultAudioPlayerRef: ElementRef;
  currentAudio: ElementRef;
  index: number;
  splashImg: string;
  campaignId: string;
  freeRideImg: string;
  freeBetToken: string;
  freeRideImage: HTMLElement;
  freeRideHeadingImage: HTMLElement;
  chatContent: HTMLElement;
  overlayBannerContainer: HTMLElement;
  soundSrc: HTMLElement;
  body: HTMLElement;
  freeRideOverlay: HTMLElement;
  loadingDiv: HTMLElement;
  overlayContentArea: HTMLElement;
  campaignInfo: IFreeRideCampaign;
  questions: IQuestionnarie;
  selectedHorseDetails: IRaceEvent;
  soundSelected: boolean = true;
  freeRideError: boolean = false;
  saveSelectedData: string[] = [];
  userAnswers: IUserAnswer[] = [];
  FREERIDEMSGS = FREE_RIDE_MESSAGES;
  cmsUri: string = environment.CMS_ROOT_URI;
  private timer: number;
  private ctaEvent: () => void;
  private optionsList: () => void;

  constructor(
    loc: PlatformLocation,
    private router: Router,
    private windowRef: WindowRefService,
    private rendererService: RendererService,
    private freeRideService: FreeRideService,
    private routingHelperService: RoutingHelperService,
    private clientUserAgentService: ClientUserAgentService,
    private userService: UserService,
    private timeSyncService: TimeSyncService,
    private deviceService: DeviceService,
    private pubSubService: PubSubService,
    private freeRideDomService: FreeRideDomService,
    private freeRideHelperService: FreeRideHelperService
  ) {
    loc.onPopState(() => this.destroyOverlay());
  }

  ngOnInit(): void {
    this.initOverlay(this.campaignData);
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', true);
  }

  /**
   * initialize the overlay
   * @param {IOverlayData} campaignData
   * @returns {void}
   */
  public initOverlay(campaignData: IOverlayData): void {
    this.index = FREE_RIDE_CONSTS.START_INDEX;
    this.saveSelectedData.length = FREE_RIDE_CONSTS.RESET_VALUE;
    this.questions = campaignData.campaignInfo.questionnarie;
    this.freeRideImg = `${this.cmsUri}${campaignData.splashInfo.freeRideLogoUrl}`;
    this.splashImg = `${this.cmsUri}${campaignData.splashInfo.splashImageUrl}`;
    this.campaignId = campaignData.campaignInfo.id;
    this.freeBetToken = campaignData.freeBetToken;
    this.soundSelected = campaignData.isSoundChecked;
    this.campaignInfo = campaignData.campaignInfo;
    this.getDomAccessors();
    this.rendererService.renderer.setStyle(this.body, PROPERTY_TYPE.SCROLL, FREE_RIDE_HTML.HIDDEN);
    this.chatContent = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.DIV, undefined, FREE_RIDE_CONSTS.CONTENT] }]);
    this.freeRideDomService.appendDomElems([{ parentElem: this.overlayContentArea, childElem: this.chatContent }]);
    this.displayQuestionNumber(this.index);
  }

  /**
   * store DOM elements
   * @returns {void}
   */
  public getDomAccessors(): void {
    this.body = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.BODY);
    this.freeRideOverlay = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.FREE_RIDE_OVERLAY);
    this.overlayContentArea = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.CONTENT_AREA);
    this.loadingDiv = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.LOADING_CHAT);
    this.freeRideImage = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.MAIN_IMAGE);
    this.freeRideHeadingImage = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.HEADING_IMAGE);
    this.overlayBannerContainer = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.BANNER_CONTAINER);
    this.soundSrc = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.SOURCE);
  }

  /**
   * play audio
   * @param {string} audioSource
   * @returns {void}
   */
  public playSound(audioSource: ElementRef): void {
    if (this.currentAudio && !this.currentAudio.nativeElement.paused) {
      this.currentAudio.nativeElement.pause();
      this.currentAudio.nativeElement.currentTime = 0;
    }
    this.currentAudio = audioSource;
    switch (audioSource) {
      case this.quesAudioPlayerRef:
        this.quesAudioPlayerRef.nativeElement.play().catch(() => { });
        break;
      case this.ansAudioPlayerRef:
        this.ansAudioPlayerRef.nativeElement.play().catch(() => { });
        break;
      case this.resultAudioPlayerRef:
        this.resultAudioPlayerRef.nativeElement.play().catch(() => { });
    }
  }

  /**
   * display loading
   * @param {boolean} show
   * @returns {void}
   */
  public showLoading(show: boolean): void {
    show ? this.rendererService.renderer.removeClass(this.loadingDiv, FREE_RIDE_HTML.HIDDEN) : this.rendererService.renderer.addClass(this.loadingDiv, FREE_RIDE_HTML.HIDDEN);
  }

  /**
   * display question
   * @param {number} quesNumber
   * @returns {void}
   */
  public displayQuestionNumber(quesNumber: number): void {
    switch (quesNumber) {
      case 1:
        this.showLoading(true);
        this.displayAdditionalMsg(this.questions.welcomeMessage);
        this.executeCallback(FREE_RIDE_CONSTS.LONG_DELAY, this.displayQuestion, this.questions.questions[quesNumber - FREE_RIDE_CONSTS.START_INDEX].quesDescription, quesNumber);
        break;
      case 2:
        this.displayAdditionalMsg(this.questions.questions[quesNumber - FREE_RIDE_CONSTS.SECOND_INDEX].chatBoxResp);
        this.updateOverlayDisplay(true);
        this.executeCallback(FREE_RIDE_CONSTS.LONG_DELAY, this.displayQuestion, this.questions.questions[quesNumber - FREE_RIDE_CONSTS.START_INDEX].quesDescription, quesNumber);
        break;
      case 3:
        this.displayAdditionalMsg(this.questions.questions[quesNumber - FREE_RIDE_CONSTS.SECOND_INDEX].chatBoxResp);
        this.executeCallback(FREE_RIDE_CONSTS.LONG_DELAY, this.displayQuestion, this.questions.questions[quesNumber - FREE_RIDE_CONSTS.START_INDEX].quesDescription, quesNumber);
        break;
      case 4:
        this.displayAdditionalMsg(this.questions.questions[quesNumber - FREE_RIDE_CONSTS.SECOND_INDEX].chatBoxResp);
        this.displaySavedDetailsMsg();
        this.sendUserSelectedAnswers(this.buildResponse());
        break;
      default:
        break;
    }
  }

  /**
   * executes callback after provided delay
   * @param {number} delay
   * @param {Function} callback
   * @param {any[]} params
   * @returns {void}
   */
  public executeCallback(delay, callback: Function, ...params: any[]): void {
    this.timer = this.windowRef.nativeWindow.setTimeout(() => {
      const bindCallback = callback.bind(this);
      bindCallback(...params);
    }, delay);
  }

  /**
   * update overlay display
   * @param {boolean} update
   * @returns {void}
   */
  public updateOverlayDisplay(update: boolean): void {
    update ? this.rendererService.renderer.addClass(this.freeRideImage, FREE_RIDE_HTML.HIDDEN) : this.rendererService.renderer.removeClass(this.freeRideImage, FREE_RIDE_HTML.HIDDEN);
    update ? this.rendererService.renderer.addClass(this.freeRideHeadingImage, FREE_RIDE_CONSTS.NEW_DISPLAY) : this.rendererService.renderer.removeClass(this.freeRideHeadingImage, FREE_RIDE_CONSTS.NEW_DISPLAY);
  }

  /**
   * display additional msg
   * @param {string} firstMsg
   * @returns {void}
   */
  public displayAdditionalMsg(firstMsg: string): void {
    const firstAdditionalElem: HTMLElement = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.DIV, firstMsg, FREE_RIDE_CONSTS.QUESTION] }]);
    this.executeCallback(FREE_RIDE_CONSTS.DELAY, this.showDetails, firstAdditionalElem);
  }

  /**
   * append additional details
   * @param {HTMLElement} firstAdditionalElem
   * @returns {void}
   */
  public showDetails(firstAdditionalElem: HTMLElement, loading?: boolean): void {
    (loading) ? this.showLoading(true) : this.showLoading(false);
    this.freeRideDomService.appendDomElems([{ parentElem: this.chatContent, childElem: firstAdditionalElem }]);
    firstAdditionalElem.scrollIntoView(false);
    this.soundSelected && this.playSound(this.quesAudioPlayerRef);
    this.overlayContentArea.scrollIntoView(false);
  }

  /**
   * display question
   * @param {string} msg
   * @param {stepNum} number
   * @returns {void}
   */
  public displayQuestion(msg: string, stepNum: number): void {
    const quesElem = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.DIV, msg, FREE_RIDE_CONSTS.QUESTION, stepNum] }]);
    this.showLoading(false);
    this.freeRideDomService.appendDomElems([{ parentElem: this.chatContent, childElem: quesElem }]);
    this.soundSelected && this.playSound(this.quesAudioPlayerRef);
    this.executeCallback(FREE_RIDE_CONSTS.SHORT_DELAY, this.displayOptionsList, stepNum);
  }

  /**
   * display answer options
   * @param {number} stepNum
   * @returns {void}
   */
  public displayOptionsList(stepNum: number): void {
    if (stepNum) {
      const optionDOMData = [{ 'stepElem': [FREE_RIDE_HTML.DIV, `Step ${stepNum} of 3`, FREE_RIDE_CONSTS.STEP_COUNT] }, { 'optionContainer': [FREE_RIDE_HTML.DIV, undefined, FREE_RIDE_CONSTS.OPTION_CONTAINER] }];
      const domElems = this.freeRideDomService.createDOMElements(optionDOMData);
      const appendDOMData = [{ parentElem: this.chatContent, childElem: domElems.get('stepElem') }, { parentElem: this.chatContent, childElem: domElems.get('optionContainer') }];
      this.freeRideDomService.appendDomElems(appendDOMData);
      this.questions.questions[stepNum - FREE_RIDE_CONSTS.START_INDEX].options.forEach((option) => {
        const showOptions = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.DIV, option.optionText, FREE_RIDE_CONSTS.ANSWER_OPTION, option.optionId] }]);
        this.optionsList = this.bindEvent(FREE_RIDE_HTML.CLICK, showOptions, this.questions.questions[stepNum - FREE_RIDE_CONSTS.START_INDEX]);
        this.freeRideDomService.appendDomElems([{ parentElem: domElems.get('optionContainer'), childElem: showOptions }]);
      });
      this.overlayContentArea.scrollIntoView(false);
    }
  }

  /**
   * triggers on user selection
   * @param {string} showMsg
   * @param {number} quesSetNum
   * @param {number} optionId
   * @returns {void}
   */
  public optionSelected(showMsg: string, quesSetNum: number, optionId: number): void {
    this.showLoading(true);
    const optionContainer = this.windowRef.document.querySelector(FREE_RIDE_CONSTS.OPTION_CONTAINER_CLS);
    const answerSelected = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.DIV, showMsg, FREE_RIDE_CONSTS.ANSWER, optionId] }]);
    this.windowRef.document.querySelectorAll(FREE_RIDE_CONSTS.OPTION_CONTAINER_CLS).forEach(option => {
      option.remove();
    });
    this.rendererService.renderer.removeChild(this.chatContent, optionContainer);
    this.freeRideDomService.appendDomElems([{ parentElem: this.chatContent, childElem: answerSelected }]);
    this.soundSelected && this.playSound(this.ansAudioPlayerRef);
    if (quesSetNum < FREE_RIDE_CONSTS.OPTION_NUM) {
      this.displayQuestionNumber(quesSetNum);
    }
  }

  /**
   * create chat bubble with selected data
   * @returns {void}
   */
  public displaySavedDetailsMsg(): void {
    const domElems = this.freeRideDomService.createDOMElements(this.constructSavedDetailsMsg());
    const appendsavedDetailsDOMData = [
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('summaryMsg') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans1') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans1Val') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans2') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans2Val') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans3') },
      { parentElem: domElems.get('savedDetailsElem'), childElem: domElems.get('ans3Val') },
    ];
    this.freeRideDomService.appendDomElems(appendsavedDetailsDOMData);
    this.executeCallback(FREE_RIDE_CONSTS.DELAY, this.showDetails, domElems.get('savedDetailsElem'), true);
  }

  /**
   * prepare config for saved data
   * @returns {Array<any>}
   */
  public constructSavedDetailsMsg(): Array<any> {
    return [
      ...HORSE_DATA_SUMMARY_CONFIG,
      { 'summaryMsg': [FREE_RIDE_HTML.DIV, this.questions.summaryMsg, FREE_RIDE_CONSTS.HORSE_SUMMARY_DATA] },
      { 'ans1Val': [FREE_RIDE_HTML.SPAN, this.saveSelectedData[0], FREE_RIDE_CONSTS.HORSE_SUMMARY_DATA] },
      { 'ans2Val': [FREE_RIDE_HTML.SPAN, this.saveSelectedData[1], FREE_RIDE_CONSTS.HORSE_SUMMARY_DATA] },
      { 'ans3Val': [FREE_RIDE_HTML.SPAN, this.saveSelectedData[2]] }
    ];
  }

  /**
   * calls placebet with userSelected data
   * @param {IUserSelectionDetail} userSelectedResp
   * @returns {void}
   */
  public sendUserSelectedAnswers(userSelectedResp: IUserSelectionDetail): void {
    if (this.freeRideHelperService.getFreeRideActiveCampaign([this.campaignInfo])) {
      this.freeRideService.requestSelectedHorse(userSelectedResp).subscribe((horseDetails: IRaceEvent) => {
        if (!(horseDetails.betError && horseDetails.betError.length > 0)) {
          this.selectedHorseDetails = horseDetails;
          this.displayResultMsg(horseDetails);
          this.freeRideService.clearFreebet();
          this.pubSubService.publish(this.pubSubService.API.FREE_RIDE_BET, false);
        } else {
          this.showResultantEventError();
        }
      }, () => {
        this.showResultantEventError();
      });
    } else {
      this.showResultantEventError();
    }
  }

  /**
   * builds EDP URL
   * @returns {string}
   */
  public buildEdpUrl(): string {
    const eventEntity: IRoutingHelperEvent | ISportEvent = {
      categoryId: environment.HORSE_RACING_CATEGORY_ID,
      categoryName: FREE_RIDE_CONSTS.CATEGORY_NAME,
      typeName: this.selectedHorseDetails.name.substring(FREE_RIDE_CONSTS.HORSE_TYPE_NUM),
      name: this.selectedHorseDetails.name,
      className: this.selectedHorseDetails.className,
      id: this.selectedHorseDetails.eventId,
    };
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  /**
   * build request for placebet call
   * @returns {IUserSelectionDetail}
   */
  public buildResponse(): IUserSelectionDetail {
    return {
      freebettoken: this.freeBetToken,
      clientUserAgent: this.clientUserAgentService.getId(),
      isAccountBet: FREE_RIDE_CONSTS.YES,
      currencyRef: this.userService.currency,
      userDto: { userName: this.userService.username },
      ipAddress: this.timeSyncService.ip,
      channelRef: this.deviceService.channel.channelRef.id,
      campaignId: this.campaignId,
      brand: environment.brand,
      userAnswers: this.userAnswers
    };
  }

  /**
   * display selected horse
   * @param {IRaceEvent} horseData
   * @returns {void}
   */
  public displayResultMsg(horseData: IRaceEvent): void {
    const resultHorseData = this.constructResultData(horseData);
    const resultConfig = this.freeRideDomService.createDOMElements([{ 'heading': ['div', this.questions.horseSelectionMsg] }, ...HORSE_DATA_CONFIG, ...resultHorseData]);
    if (horseData.silkUrl) {
      this.rendererService.renderer.setStyle(resultConfig.get('silkImage'), PROPERTY_TYPE.BACKGROUND_IMAGE, `url(${horseData.silkUrl}), url(${FREE_RIDE_CONSTS.DEFAULT_JERSEY})`);
    }
    else {
      this.rendererService.renderer.setStyle(resultConfig.get('silkImage'), PROPERTY_TYPE.BACKGROUND_IMAGE, `url(${FREE_RIDE_CONSTS.DEFAULT_JERSEY})`);
    }
    this.freeRideDomService.appendDomElems(this.prepareResultData(JSON.parse(JSON.stringify(RESULT_DATA_CONFIG)), resultConfig));
    this.executeCallback(FREE_RIDE_CONSTS.DELAY, this.displayCTAButton, resultConfig.get('resultElem'));
  }

  /**
   * map result data with elem attributes
   * @param {IRaceEvent} horseData
   * @returns {Array<any>}
   */
  public constructResultData(horseData: IRaceEvent): Array<any> {
    return [
      { ans1: [FREE_RIDE_HTML.DIV, horseData.horseName, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS] },
      { ans2: [FREE_RIDE_HTML.DIV, FREE_RIDE_CONSTS.JOCKEY_PREFIX + horseData.jockeyName, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS] },
      { ans3: [FREE_RIDE_HTML.SPAN, horseData.raceTime + ',', FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS] },
      { ans4: [FREE_RIDE_HTML.SPAN, ' ' + horseData.raceName, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS] }
    ];
  }

  /**
   * map parent and child elems to respective elems
   * @param {Array<IDOMDATA>} resultArray
   * @param {any} listOfFields
   * @returns {Array<IDOMData>}
   */
  public prepareResultData(resultArray: Array<IDOMData>, listOfFields: any): Array<IDOMData> {
    for (const elem in resultArray) {
      resultArray[elem].parentElem = listOfFields.get(resultArray[elem].parentElem);
      resultArray[elem].childElem = listOfFields.get(resultArray[elem].childElem);
    }
    return resultArray;
  }

  /**
   * display CTA btn
   * @param {HTMLElement} resultElem
   * @returns {void}
   */
  public displayCTAButton(resultElem: HTMLElement): void {
    const ctaBtnElems = this.freeRideDomService.createDOMElements([{ 'elem': [FREE_RIDE_HTML.BUTTON, FREE_RIDE_CONSTS.CTA_TO_RACECARD, FREE_RIDE_CONSTS.CTA_BTN] }, { 'elemContainer': [FREE_RIDE_HTML.DIV, '', FREE_RIDE_CONSTS.CTA_CONTAINER] }]);
    this.showLoading(false);
    this.freeRideDomService.appendDomElems([{ parentElem: this.chatContent, childElem: resultElem }]);
    resultElem.scrollIntoView(false);
    this.soundSelected && this.playSound(this.resultAudioPlayerRef);
    this.ctaEvent = this.bindEvent(FREE_RIDE_HTML.CLICK, ctaBtnElems.get('elem'));
    this.freeRideDomService.appendDomElems([{ parentElem: ctaBtnElems.get('elemContainer'), childElem: ctaBtnElems.get('elem') }, { parentElem: this.chatContent, childElem: ctaBtnElems.get('elemContainer') }]);
    ctaBtnElems.get('elemContainer').scrollIntoView(false);
  }

  /**
   * bind event to elems
   * @param {string} eventType
   * @param {HTMLElement} elem
   * @param {IQuestions} questionsData
   * @returns {() => void}
   */
  public bindEvent(eventType: string, elem: HTMLElement, questionsData?: IQuestions): () => void {
    return this.rendererService.renderer.listen(elem, eventType, (event) => {
      event.stopPropagation();
      if (elem.className !== FREE_RIDE_CONSTS.CTA_BTN) {
        this.storeSelectedData(event, questionsData);
      } else {
        this.goToEdpPage();
      }
    });
  }

  /**
   * stores user selected data
   * @param {any} event
   * @param {IQuestions} questionsData
   * @returns {void}
   */
  public storeSelectedData(event: any, questionsData: IQuestions): void {
    if (this.userAnswers.length == 0 || !this.userAnswers.find(answer => answer.questionId == questionsData.questionId)) {
      const selectedAnswer = { questionId: questionsData.questionId, optionId: +event.currentTarget.id };
      this.saveSelectedData.push(event.currentTarget.innerText);
      this.rendererService.renderer.addClass(event.currentTarget, FREE_RIDE_CONSTS.SELECTED_ANSWER);
      this.userAnswers.push(selectedAnswer);
      this.executeCallback(FREE_RIDE_CONSTS.SELECTION_DELAY, this.optionSelected, event.currentTarget.innerText, ++this.index, event.currentTarget.id);
      this.freeRideService.sendGTM('chat box', `step ${String(questionsData.questionId)}`, event.currentTarget.innerText);
      this.optionsList();
    }
  }

  /**
   * navigate to edp page
   * @returns {void}
   */
  public goToEdpPage(): void {
    this.freeRideService.sendGTM('chat box', FREE_RIDE_CONSTS.CTA_TO_RACECARD);
    this.pubSubService.publish(this.pubSubService.API.FREE_RIDE_BET, false);
    this.ctaEvent();
    this.destroyOverlay();
    this.router.navigateByUrl(this.buildEdpUrl());
  }

  /**
   * show error msg
   * @returns {void}
   */
  public showResultantEventError(): void {
    this.showLoading(false);
    this.freeRideError = true;
    this.freeRideService.sendGTM('chat box', 'error message');
  }

  /**
   * close error msg
   * @param {Event} event
   * @returns {void}
   */
  public closeErrorMessage(event: Event): void {
    event.preventDefault();
    this.freeRideError = false;
  }

  /**
   * destroy overlay
   * @returns {void}
   */
  public destroyOverlay(): void {
    this.rendererService.renderer.removeStyle(this.body, PROPERTY_TYPE.SCROLL);
    this.freeRideClose.emit();
    clearTimeout(this.timer);
    this.freeRideService.sendGTM('chat box', 'exit');
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM_INDEX', false);
  }
}
