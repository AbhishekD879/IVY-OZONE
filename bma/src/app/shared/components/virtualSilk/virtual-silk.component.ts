import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'virtual-silk',
  template: '<img *ngIf="src" [src]="src" [title]="outcome.name" (error)="src = null"/>',
  styleUrls: ['virtual-silk.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class VirtualSilkComponent implements OnInit {
  @Input() event: ISportEvent;
  @Input() outcome: IOutcome;

  public src: string;

  constructor(
    public virtualSharedService: VirtualSharedService) {
  }

  ngOnInit(): void {
    const silkName = this.outcome.silkName || this.outcome.racingFormOutcome && this.outcome.racingFormOutcome.silkName;
    this.src = silkName && this.virtualSharedService.getVirtualSilkSrc(this.event, silkName);
  }
}
