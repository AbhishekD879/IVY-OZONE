import { RendererService } from './renderer.service';


describe('RendererService', () => {
  let service, rendererFactory;

  beforeEach(() => {
    rendererFactory = {
      createRenderer: jasmine.createSpy()
    };
    service = new RendererService(rendererFactory);
  });

  describe('constructor', () => {
    it('should create instance and create renderer property', () => {
      expect(service).toBeTruthy();
      expect(rendererFactory.createRenderer).toHaveBeenCalled();
    });
  });
});
