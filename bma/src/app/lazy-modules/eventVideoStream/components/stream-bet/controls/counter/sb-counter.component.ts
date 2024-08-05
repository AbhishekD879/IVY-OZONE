import {
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';


@Component({
  selector: 'sb-counter',
  templateUrl: './sb-counter.component.html',
  styleUrls: ['./sb-counter.component.scss']
})
export class SbCounterComponent {
  @Input() teamScores: number[];
  @Input() teamName: string;
  @Output() counterValueEmitter = new EventEmitter<number>();

  disableMinus: boolean = true;
  disablePlus: boolean = false;
  selectedValue: number;

  constructor() { }

  ngOnInit(): void {
    this.selectedValue = this.teamScores[0];
    if (this.selectedValue === this.teamScores[this.teamScores.length - 1])
      this.disablePlus = true;

    if (this.selectedValue === this.teamScores[0])
      this.disableMinus = true;

    this.counterValueEmitter.emit(this.selectedValue);
  }

  scoreChange(currState: number) {
    this.selectedValue += currState;
    this.counterValueEmitter.emit(this.selectedValue);
    if (this.selectedValue === this.teamScores[this.teamScores.length - 1]) {
      this.disablePlus = true;
      if (this.selectedValue !== this.teamScores[0])
        this.disableMinus = false;

      return;
    }

    if (this.selectedValue === this.teamScores[0]) {
      this.disableMinus = true;
      if (this.selectedValue !== this.teamScores[this.teamScores.length - 1])
        this.disablePlus = false;

      return;
    }

    this.disablePlus = false;
    this.disableMinus = false;

  }

}
