import {
  Component
} from '@angular/core';

import { DigitKeyboardComponent } from '@shared/components/digitKeyboard/digit-keyboard.component';

interface ILabelledValue {
  label: string;
  value: string;
}

@Component({
  selector: 'sb-digit-keyboard',
  templateUrl: 'sb-digit-keyboard.component.html',
  styleUrls: ['sb-digit-keyboard.component.scss']
})
export class SbDigitKeyboardComponent extends DigitKeyboardComponent {
  
}
