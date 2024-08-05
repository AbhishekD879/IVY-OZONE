import { of } from 'rxjs';

import { PostPreviewComponent } from './post-preview.component';
import { environment } from '@root/environments/environment';

describe('PostPreviewComponent', () => {
  let component: PostPreviewComponent;
  let imageLoaderService;
  let brandService;

  beforeEach(() => {
    imageLoaderService = {
      getData: jasmine.createSpy('getData').and.returnValue(of(['image']))
    };
    brandService = {
      brand: 'bma'
    }

    component = new PostPreviewComponent(imageLoaderService, brandService);

    component.post = {
      brand: 'bma',
      template: { postIconSvgId: 'post',  headerIconSvgId: 'header',  showLeftSideRedLine: false, showLeftSideBlueLine: false}
    } as any;
  });

  describe('ngOnInit', () => {
    it('should get data', () => {
      component.ngOnInit();
      expect(imageLoaderService.getData).toHaveBeenCalledWith(component.post.template.postIconSvgId);
      expect(imageLoaderService.getData).toHaveBeenCalledWith(component.post.template.headerIconSvgId);
      expect(component.activePostIconImage).toBeDefined();
      expect(component.activeHeaderIconImage).toBeDefined();
    });

    it('shoud not get data', () => {
      component.post.template = {} as any;
      component.ngOnInit();
      expect(imageLoaderService.getData).not.toHaveBeenCalled();
      expect(component.activePostIconImage).toBeUndefined();
      expect(component.activeHeaderIconImage).toBeUndefined();
    });
  });

  it('absoluteUrl', () => {
    expect(
      component.absoluteUrl({ path: 'path', filename: 'file' } as any)
    ).toEqual(`${environment.cmsRoot.bma}path/file`);
  });

  describe('#getCssClass', () => {
    it('should call getCssClass method and return empty value for bma brand', () => {
      component.brand = 'bma';
      component.activePostIconImage = undefined;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('');
    });

    it('should call getCssClass method and return post--with-icon for bma brand', () => {
      component.brand = 'bma';
      component.activePostIconImage = { active: true } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual(' post--with-icon');
    });

    it('should call getCssClass method and return post--blue-line for bma brand', () => {
      component.brand = 'bma';
      component.activePostIconImage = undefined;
      component.post.template = { showLeftSideRedLine: false, showLeftSideBlueLine: true } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('post--blue-line');
    });

    it('should call getCssClass method and return post--blue-line post--with-icon for bma brand', () => {
      component.brand = 'bma';
      component.activePostIconImage = { active: true } as any;
      component.post.template = { showLeftSideRedLine: true, showLeftSideBlueLine: true } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('post--blue-line post--with-icon');
    });

    it('should call getCssClass method and return empty value for ladbrokes brand', () => {
      component.brand = 'ladbrokes';
      component.activePostIconImage = undefined;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('');
    });

    it('should call getCssClass method and return post--with-icon for ladbrokes brand', () => {
      component.brand = 'ladbrokes';
      component.activePostIconImage = { active: true } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual(' post--with-icon');
    });

    it('should call getCssClass method and return post--red-line for ladbrokes brand', () => {
      component.brand = 'ladbrokes';
      component.activePostIconImage = undefined;
      component.post.template = { showLeftSideRedLine: true, showLeftSideBlueLine: false } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('post--red-line');
    });

    it('should call getCssClass method and return post--red-line  post--with-icon for ladbrokes brand', () => {
      component.brand = 'ladbrokes';
      component.activePostIconImage = { active: true } as any;
      component.post.template = { showLeftSideRedLine: true, showLeftSideBlueLine: true } as any;
      const result = component.getCssClass(component.post.template);

      expect(result).toEqual('post--red-line post--with-icon');
    });
  });
});
