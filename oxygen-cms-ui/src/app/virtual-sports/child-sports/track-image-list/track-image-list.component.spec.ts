import { TrackImageListComponent } from './track-image-list.component';
import { environment } from '@root/environments/environment';

describe('TrackImageListComponent', () => {
  let component: TrackImageListComponent;
  let brandService;

  beforeEach(() => {
    brandService = { brand: 'bma' };
    component = new TrackImageListComponent(brandService);
    component.onImageRemoving.emit = jasmine.createSpy('emit');
  });

  it('absoluteUrl', () => {
    expect(
      component.absoluteUrl({ path: 'path', filename: 'file' } as any)
    ).toBe(`${environment.cmsRoot.bma}path/file`);
  });

  it('removeImageClicked', () => {
    component.removeImageClicked(null);
    expect(component.onImageRemoving.emit).toHaveBeenCalled();
  });
});
