import { Component } from '@angular/core';
import {
  BetHistoryPromptComponent as CoralBetHistoryPromptComponent
} from '@app/betHistory/components/betHistoryPrompt/bet-history-prompt.component';

@Component({
  selector: 'bet-history-prompt',
  templateUrl: '../../../../../app/betHistory/components/betHistoryPrompt/bet-history-prompt.component.html',
  styleUrls: ['../../../../../app/betHistory/components/betHistoryPrompt/bet-history-prompt.component.scss',
    './bet-history-prompt.component.scss']
})
export class BetHistoryPromptComponent extends CoralBetHistoryPromptComponent {}
