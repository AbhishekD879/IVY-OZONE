import { Component, Input } from '@angular/core';
interface IBurttons {
  label: string;
  onClick: Function;
}

@Component({
  selector: 'filter-buttons',
  templateUrl: 'filter-buttons.component.html',
  styleUrls: ['filter-buttons.component.scss']
})
export class FilterButtonsComponent {
  @Input() items: IBurttons[];
  @Input() position: number;

  trackByLabel(index: number, button: IBurttons): string {
    return `${index}_${button.label}`;
  }
}
