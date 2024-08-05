import { Component, Input } from "@angular/core";

import { AbstractOutletComponent } from "@app/shared/components/abstractOutlet/abstract-outlet.component";
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { LocaleService } from "@core/services/locale/locale.service";

@Component({
    selector: 'racing-antepost-content',
    templateUrl: './racing-antepost-content.component.html',
    styleUrls: ['./racing-antepost-content.component.scss']
})

export class RacingAntepostContentComponent extends AbstractOutletComponent {

    @Input() isEventOverlay: boolean;
    @Input() sportName: string;
    isBrandLadbrokes: boolean;

    constructor(protected deviceService: DeviceService, protected locale: LocaleService,) {
        super();
        this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    }
}