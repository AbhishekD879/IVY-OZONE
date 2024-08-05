import { VsVideoStreamComponent } from './vs-video-stream.component';

describe('VsVideoStreamComponent', () => {
  let sanitizer;
  let component: VsVideoStreamComponent;

  beforeEach(() => {
    sanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
    };

    component = new VsVideoStreamComponent(
      sanitizer
    );
  });

  it('ngOnChanges with empty stream url', () => {

    component.ngOnChanges();
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith('https://player.igamemedia.com/vplayer?c=83127&s=none&q=moblo');
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledTimes(1);

    component.baseStreamURL = 'http://test.local';
    component.ngOnChanges();
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith('https://player.igamemedia.com/vplayer?c=83127&s=none&q=moblo');
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledTimes(2);
  });

  it('ngOnChanges ', () => {
    component.deviceViewType = 'mobile';
    component.baseStreamURL = 'http://test.local';
    component.ngOnChanges();
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith('http://test.local&q=moblo');
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledTimes(1);
  });
});
