import { AddStreamAndBetNodeComponent } from './add-stream-and-bet-node.component';
import {MAT_DIALOG_DATA as data} from '@angular/material/dialog';

describe('AddStreamAndBetNodeComponent', () => {
  let component: AddStreamAndBetNodeComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {};
    component = new AddStreamAndBetNodeComponent(
      dialogRef, data
    );
    component.ngOnInit();
  });

  it('should set initial data', () => {
    expect(component.nameToIdMap).toBeDefined();
    expect(component.nameDropDown).toBeDefined();
  });
});
