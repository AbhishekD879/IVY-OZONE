import { Component } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
    selector:'free-bet-empty',
    templateUrl: './free-bet-empty.component.html',
    styleUrls: ['./free-bet-empty.component.scss']
})

export class FreeBetEmptyComponent {
    message: string = this.localeService.getString('bma.noFreeBets');
    constructor(private localeService: LocaleService) {}

}