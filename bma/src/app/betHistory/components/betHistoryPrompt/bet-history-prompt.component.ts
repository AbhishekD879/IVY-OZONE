import { Component, Input, OnInit } from '@angular/core';
import { EditMyAccaService } from '../../services/editMyAcca/edit-my-acca.service';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'bet-history-prompt',
  templateUrl: './bet-history-prompt.component.html',
  styleUrls: ['./bet-history-prompt.component.scss']
})
export class BetHistoryPromptComponent implements OnInit {
  @Input() prompt: string;
  @Input() mode: string;
  @Input() promptText?: string;

  constructor(private emaService: EditMyAccaService, private locale: LocaleService) {}

  ngOnInit(): void {

    if (this.mode === 'ema') {
      this.promptText = this.prompt === 'success' ? this.locale.getString('ema.editSuccess.caption') :
        this.emaService.emaConfig.genericErrorText;
    }
  }
}
