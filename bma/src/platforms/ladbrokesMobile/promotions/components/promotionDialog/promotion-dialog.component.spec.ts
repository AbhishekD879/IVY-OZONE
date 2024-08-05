import { PromotionDialogComponent } from './promotion-dialog.component';
import { PromotionDialogComponent as AppPromotionDialogComponent } from '@promotions/components/promotionDialog/promotion-dialog.component';

describe('PromotionDialogComponent', () => {
  let component;

  beforeEach(() => {
    component = new PromotionDialogComponent({} as any, {} as any ,{}as any);
  });

  it(`should be  instance of 'AbstractDialog'`, () => {
    expect(AppPromotionDialogComponent).isPrototypeOf(component);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
});
