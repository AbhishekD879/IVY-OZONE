import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  Input,
  OnInit,
  Output,
  QueryList,
  SecurityContext,
  ViewChildren,
  EventEmitter,
  OnChanges,
  SimpleChanges
} from '@angular/core';
import { Router } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@core/services/cms/cms.service';
import { IStaticBlock } from '@core/services/cms/models';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { FiveasideRulesEntryAreaService
} from '@fiveASideShowDownModule/services/fiveaside-rules-entry-area.service';
import { IEventDetails, IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { BUTTON_TYPE, PROPERTY_TYPE, RENDERER_METHOD } from '@app/fiveASideShowDown/constants/enums';
import { RULES_DOM, GTM_EVENTS } from '@app/fiveASideShowDown/constants/constants';
import { DecimalPipe } from '@angular/common';
import { RULES_STATIC_BLOCK, CONTEST_STATUSES
} from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.constant';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { UserService } from '@app/core/services/user/user.service';
import { FiveasideLeaderBoardService } from '@fiveASideShowDownModule/services/fiveaside-leader-board.service';
@Component({
  selector: 'fiveaside-rules-entry-area',
  template: ``
})
export class FiveASideRulesEntryAreaComponent implements OnInit, AfterViewInit, OnChanges {
  @Input() removeElements: string[] = [];
  @Input() contest: IShowDown;
  @Input() contestSize: number;
  @Input() userContestSize: number;
  @Input() contestClass: string;
  @Input() contestStatus?: string;
  @Input() hasMaxWidth: boolean = false;
  @Output() readonly showRulesOverlay = new EventEmitter();
  @ViewChildren('rulesArea') rulesArea: QueryList<ElementRef>;
  public eventEntity: IEventDetails;
  public staticBlockContent: string;
  private isBuildBetEnabled: boolean;
  private readonly STATIC_BLOCK_URL: string = 'five-a-side-rules-area';
  private readonly tagName: string = 'ButtonValidator';

  constructor(private localeService: LocaleService,
    private rendererService: RendererService,
    private domSanitizer: DomSanitizer,
    private cmsService: CmsService,
    private windowRefService: WindowRefService,
    private router: Router,
    private rulesEntryService: FiveasideRulesEntryAreaService,
    private decimalPipe: DecimalPipe,
    private fiveaSideContestSelectionService: FiveASideContestSelectionService,
    private pubSubService: PubSubService,
    private userService: UserService,
    private leaderBoardService: FiveasideLeaderBoardService
    ) { }

  ngOnInit(): void {
    this.eventEntity = this.contest.eventDetails;
    this.fetchInitialData();
    this.validateButtonOnLogin();
  }

  ngAfterViewInit(): void {
    this.rulesArea.changes.subscribe((change) => {
      if (change) {
        this.setRulesInformation();
      }
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.userContestSize && !changes.userContestSize.isFirstChange()) {
      this.setRulesInformation(true);
    }
  }

  /**
   * Hndle all click events
   * @param event
   * @returns {void}
   */
  @HostListener('click', ['$event'])
  handleActionClick(event: MouseEvent): void {
    const target: HTMLElement = event.target as HTMLElement;
    event.preventDefault();
    if (target && target.className) {
      switch(target.className) {
        case BUTTON_TYPE.BUILD:
          if (this.isBuildBetEnabled) {
            const url = this.rulesEntryService.formFiveASideUrl(this.eventEntity); // TODO Dependency on event details
            this.fiveaSideContestSelectionService.defaultSelectedContest = this.contest.id;
            if (this.userService && this.userService.username) {
              this.rulesEntryService.trackGTMEvent(GTM_EVENTS.BUILD.category,
                GTM_EVENTS.BUILD.action, GTM_EVENTS.BUILD.label);
              this.router.navigate([`/${url}/5-a-side/pitch`]);
            } else {
              this.rulesEntryService.trackGTMEvent(GTM_EVENTS.BUILD.category,
                GTM_EVENTS.LOGIN.action, GTM_EVENTS.BUILD.label);
              this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'header' });
            }
          }
          break;
        case BUTTON_TYPE.RULES:
            this.rulesEntryService.trackGTMEvent(GTM_EVENTS.RULES.category,
              GTM_EVENTS.RULES.action, GTM_EVENTS.RULES.label);
            this.showRulesOverlay.emit();
          break;
        case BUTTON_TYPE.BACK:
        case BUTTON_TYPE.RETURN_TO_LOBBY:
          this.router.navigate([`/5-a-side/lobby`]);
          break;
        default:
          break;
      }
    }
  }

  /**
   * Fetch Initial Data from CMS
   * @returns {void}
   */
  private fetchInitialData(): void {
    this.cmsService.getStaticBlock(this.STATIC_BLOCK_URL)
      .subscribe((staticBlock: IStaticBlock) => {
        this.staticBlockContent = this.domSanitizer.sanitize(SecurityContext.NONE,
          this.domSanitizer.bypassSecurityTrustHtml(staticBlock.htmlMarkup));
      });
  }

  /**
   * Set Initial Information based on contest details
   * @returns {void}
   */
  private setRulesInformation(hasChange: boolean = false): void {
    if (this.hasMaxWidth) {
      this.addRulesStyles();
    }
    this.appendBlurbInformation(hasChange);
    this.validateBuildButton();
    this.removeElementsBasedOnContestStatus();
    this.setDOMProperty(RULES_DOM.minAmount, RENDERER_METHOD.PROPERTY, { minAmount: this.contest.entryStake },
      PROPERTY_TYPE.TEXT_CONTENT, null);
    if (!this.contest.maxEntries && !this.contest.maxEntriesPerUser) {
      this.setDOMProperty(RULES_DOM.thirdRule, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.DISPLAY, RULES_DOM.displayNone);
    } else {
      this.validateContestProperties('maxEntriesPerUser', RULES_DOM.userEntries.normal, RULES_DOM.userEntries.bold,
      RULES_DOM.userEntries.parent, { maxUserEntries: this.contest.maxEntriesPerUser, betsPlaced: this.userContestSize }, RULES_STATIC_BLOCK.teams);
      this.validateContestProperties('maxEntries', RULES_DOM.totalEntries.normal, RULES_DOM.totalEntries.bold,
        RULES_DOM.totalEntries.parent, { maxContestEntries: this.contest.maxEntries, currentContestEntries: this.contestSize },
        RULES_STATIC_BLOCK.size);
    }
  }

  /**
   * Remove Dom Elements based on request
   * @returns {void}
   */
  private removeElementsBasedOnContestStatus(): void {
    if (this.contestStatus !== CONTEST_STATUSES.pre) {
      this.setDOMProperty(RULES_DOM.returnToLobby, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.DISPLAY, RULES_DOM.displayNone);
    }
    this.removeElements.forEach((selector: string) => {
        this.setDOMProperty(`${selector}`, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.DISPLAY, RULES_DOM.displayNone);
    });
  }

  /**
   * To Append Blurb from contest information
   * @returns {void}
   */
  private appendBlurbInformation(hasChange: boolean = false): void {
    const firstRuleElement: HTMLElement = this.windowRefService.document.querySelector(`${this.contestClass} ${RULES_DOM.rulesParent}`);
    if (this.contest.blurb && firstRuleElement && !hasChange) {
      const blurbElement: HTMLElement = this.rendererService.renderer.createElement('div');
      this.rendererService.renderer.setProperty(blurbElement, PROPERTY_TYPE.INNER_HTML, this.contest.blurb);
      this.rendererService.renderer.addClass(blurbElement, RULES_DOM.rulesSubHeader);
      this.rendererService.renderer.insertBefore(firstRuleElement.parentNode, blurbElement, firstRuleElement);
      this.setDOMProperty(`.${RULES_DOM.rulesSubHeader} p`, RENDERER_METHOD.CLASS, null, PROPERTY_TYPE.CLASS, RULES_DOM.rulesSubHeader);
    }
  }

  /**
   * To Enable/Disable Build Button and Add corresponding styles
   * @returns {void}
   */
  private validateBuildButton(): void {
    const { buttonType, isBuildBetEnabled } = this.rulesEntryService.getButtonStatus(this.contestSize,
      this.userContestSize, this.contest as any);
    this.isBuildBetEnabled = isBuildBetEnabled;
    const buttonElement: HTMLElement = this.windowRefService.document.querySelector(RULES_DOM.buildButton);
    if (buttonElement) {
      this.rendererService.renderer.setProperty(buttonElement, PROPERTY_TYPE.TEXT_CONTENT, buttonType);
    }
    if (!this.isBuildBetEnabled) {
      this.setDOMProperty(RULES_DOM.buildButton, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.BACKGROUND_COLOR, '#c5de91');
    }
  }

  /**
   * Validate contest properties, if prsent perform action
   * @param {string} property
   * @param {string} element
   * @param {string} boldElement
   * @param {string} removeElement
   * @param {[key:string]: number} args
   * @param {string} defaultText
   * @returns {void}
   */
  private validateContestProperties(property: string, element: string,
     boldElement: string, removeElement: string, args: {[key:string]: number},
     defaultText?: string): void {
      if (this.contest[property]) {
        this.setDOMProperty(element, RENDERER_METHOD.PROPERTY, args, PROPERTY_TYPE.TEXT_CONTENT, null);
        this.setDOMProperty(boldElement, RENDERER_METHOD.PROPERTY, args, PROPERTY_TYPE.TEXT_CONTENT, null, defaultText);
      } else {
        this.setDOMProperty(`${removeElement}`, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.DISPLAY, 'none');
      }
  }

  /**
   * To map DOM property using class
   * @param {string} selector
   * @param {string} rendererProperty
   * @param args
   * @param {string} property
   * @param {string} value
   * @returns {void}
   */
  private setDOMProperty(selector: string, rendererProperty: string, args: {[key: string]: number | string}, property: string,
    value: string, defaultText?: string): void {
    const htmlElement: HTMLElement = this.windowRefService.document.querySelector(`${this.contestClass} ${selector}`);
    if (htmlElement) {
      if (property === PROPERTY_TYPE.TEXT_CONTENT) {
        const transformedArgs: {[key: string]: number | string} = this.transformToDecimal(args);
        const textContent: string = defaultText || htmlElement.textContent;
        const localeText: string = this.localeService.applySubstitutions(textContent, transformedArgs);
        this.rendererService.renderer[rendererProperty](htmlElement, property, localeText);
      } else if (property === PROPERTY_TYPE.CLASS) {
        this.rendererService.renderer[rendererProperty](htmlElement, value);
      } else {
        this.rendererService.renderer[rendererProperty](htmlElement, property, value);
      }
    }
  }

  /**
   * To Transform to decimal
   * @param {[key: string]: number | string} args
   * @returns {[key: string]: number | string}
   */
  private transformToDecimal(args: {[key: string]: number | string}): {[key: string]: number | string} {
    const finalArgs: {[key: string]: number | string} = {...args};
    Object.entries(finalArgs).forEach(([key, value]) => {
      if (key !== 'minAmount') {
        finalArgs[key] = this.decimalPipe.transform(value);
      }
    });
    return finalArgs;
  }

  /**
   * To Add Styles when max width is true
   * @returns {void}
   */
  private addRulesStyles(): void {
    // Here as we have three rules, we are defaulting it to 3
    for (let i = 1; i <= 3; i++) {
      const ruleDiv: string = `${RULES_DOM.rulesInfo}-${i}`;
      const ruleDivElement: HTMLElement = this.windowRefService.document.querySelector(`${this.contestClass} ${ruleDiv}`);
      if (ruleDivElement) {
        this.setDOMProperty(`${ruleDiv} ${RULES_DOM.iconContent}`, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.WIDTH,
          RULES_DOM.iconWidth);
        this.setDOMProperty(`${ruleDiv} ${RULES_DOM.textContent}`, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.WIDTH,
          RULES_DOM.textWidth);
      }
    }
    this.setDOMProperty(`${RULES_DOM.buildButton}`, RENDERER_METHOD.STYLE, null, PROPERTY_TYPE.MARGIN,
      RULES_DOM.btnMargin);
  }

  /**
   * Validate button on login success callback
   * @returns void
   */
  private validateButtonOnLogin(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.validateBuildButton();
      if (this.contest) {
        this.leaderBoardService.optInUserIntoTheContest(this.contest);
      }
    });
  }
 }
