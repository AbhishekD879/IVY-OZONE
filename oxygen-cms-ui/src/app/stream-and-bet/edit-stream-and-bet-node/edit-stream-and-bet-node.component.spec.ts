import { EditStreamAndBetNodeComponent } from './edit-stream-and-bet-node.component';
import {MAT_DIALOG_DATA as data} from '@angular/material/dialog';

describe('EditStreamAndBetNodeComponent', () => {
  let component: EditStreamAndBetNodeComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {};
    component = new EditStreamAndBetNodeComponent(
      dialogRef, data
    );
    component.ngOnInit();
  });

  it('should set initial data', () => {
    expect(component.node).toEqual(component.data.node);
  });
});
