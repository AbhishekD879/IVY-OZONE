import { Component, Input, EventEmitter,Output } from '@angular/core';

@Component({
  selector: 'stream-bet-template-drop-down',
  templateUrl: './sb-template-drop-down.component.html',
  styleUrls: ['./sb-template-drop-down.component.scss']
})
export class StreamBetTemplateDropDownComponent {
  @Input() outcomes: string[] = [];
  @Output() itemEmit?: EventEmitter<string> = new EventEmitter();

  constructor() { }

  onValueChange(outcomeName:string){
   this.itemEmit.emit(outcomeName);
  }
   /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
   trackByIndex(index: number): number {
    return index;
  }
}