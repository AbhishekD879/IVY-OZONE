import { Component, OnInit } from '@angular/core';
import {
  VirtualSportClassesComponent as CoralVirtualSportClassesComponent
} from '@app/vsbr/components/virtualSportClasses/virtual-sport-classes.component';

@Component({
  selector: 'virtual-sport-classes',
  templateUrl: './virtual-sport-classes.component.html',
  styleUrls: ['./virtual-sport-classes.component.scss']
})
export class VirtualSportClassesComponent extends CoralVirtualSportClassesComponent implements OnInit {

  ngOnInit(): void {
    super.ngOnInit();
  }
}
