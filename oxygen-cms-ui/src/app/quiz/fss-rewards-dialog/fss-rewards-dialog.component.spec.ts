import { FssRewardsDialogComponent } from './fss-rewards-dialog.component';
import { FssRewards } from '@app/client/private/models/coins-rewards.model';

describe('FssRewardsDialogComponent', () => {
  let component: FssRewardsDialogComponent;
  let dialogRef = {
    disableClose: false,
    close: jasmine.createSpy('close')
  } as any;

  const mockDialogData: FssRewards = {
    value: 100,
    communicationType: 'Inbox',
    siteCoreId: '12345',
  };

  beforeEach(() => {
    component = new FssRewardsDialogComponent(dialogRef, {data: mockDialogData});
  });

  it('should initialize fssRewards with dialog data', () => {
    component.ngOnInit();
    expect(component.fssRewards).toEqual(mockDialogData);
  });

  it('should disable dialog close', () => {
    expect(component['dialogRef'].disableClose).toBe(true);
  });

  it('should close the dialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
