import { LiveServIframeService } from './live-serv-iframe.service';
import environment from '@environment/oxygenEnvConfig';

declare let window: any;
declare let document: any;

describe('LiveServIframeService', () => {
  let service: LiveServIframeService;

  beforeEach(() => {
    window.document.frames = {};
    window.ps_connect_register = jasmine.createSpy('ps_connect_register');
    window.ps_connect_get_client_api = jasmine.createSpy('ps_connect_get_client_api');
    window.ps_connect_add_onready = jasmine.createSpy('ps_connect_add_onready');
    window.ps_connect_make_channel_name = jasmine.createSpy('ps_connect_make_channel_name');

    service = new LiveServIframeService();
    service['ps_connect_source_iframe'] = jasmine.createSpy('ps_connect_source_iframe');
  });

  afterEach(() => {
    service = null;
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('initIframe', () => {
    service['initGlobalVariables'] = jasmine.createSpy();
    service['initGlobalFunctions'] = jasmine.createSpy();
    service['setDefaultValues'] = jasmine.createSpy();

    service.initIframe();

    expect(service['initGlobalVariables']).toHaveBeenCalled();
    expect(service['initGlobalFunctions']).toHaveBeenCalled();
    expect(service['setDefaultValues']).toHaveBeenCalled();
  });

  it('psRegister', () => {
    const keyId = 'kid',
      callback = () => {},
      channels = [],
      lastMsgId = 'lmi';

    service.psRegister(keyId, callback, channels, lastMsgId);

    expect(window.ps_connect_register).toHaveBeenCalledWith(keyId, callback, channels, lastMsgId);
  });

  xit('initGlobalVariables', () => {
    service['initGlobalVariables']();

    expect(document.domain).toBe(environment.LIVESERV.DOMAIN);
    expect(window.push_www_url).toBe(environment.LIVESERV.PUSH_URL);
    expect(window.push_instances).toEqual([
      environment.LIVESERV.PUSH_INSTANCE_URL,
      environment.LIVESERV.PUSH_INSTANCE_PORT,
      environment.LIVESERV.PUSH_INSTANCE_TYPE
    ]);
    expect(window.push_common_subdomain).toBe(environment.LIVESERV.PUSH_COMMON_SUBDOMAIN);
    expect(window.push_location_handler).toBe(environment.LIVESERV.PUSH_LOCATION_HANDLER);
    expect(window.push_iframe_id).toBe(environment.LIVESERV.PUSH_IFRAME_ID);
    expect(window.push_version).toBe(environment.LIVESERV.PUSH_VERSION);
    expect(window.ps_connect_push).toBeNull();
  });

  it('initGlobalFunctions', () => {
    service['initGlobalFunctions']();

    expect(window.ps_connect_add_onready).toEqual(jasmine.any(Function));
    expect(window.ps_connect_register).toEqual(jasmine.any(Function));
    expect(window.ps_connect_get_client_api).toEqual(jasmine.any(Function));
    expect(window.ps_connect_make_channel_name).toEqual(jasmine.any(Function));
    expect(window.push_ready).toEqual(jasmine.any(Function));
    expect(window.push_shutdown).toEqual(jasmine.any(Function));
  });

  it('initGlobalFunctions (ps_connect_add_onready)', () => {
    service['ps_connect_required'] = jasmine.createSpy();
    service._ps_connect_onready_fns = [];
    service['initGlobalFunctions']();
    const fnSpy = jasmine.createSpy();

    service._ps_connect_started = true;
    window.ps_connect_add_onready(fnSpy);
    expect(service['ps_connect_required']).toHaveBeenCalled();
    expect(fnSpy).toHaveBeenCalled();

    service._ps_connect_started = false;
    window.ps_connect_add_onready(fnSpy);
    expect(service['ps_connect_required']).toHaveBeenCalled();
    expect(service._ps_connect_onready_fns[0]).toBe(fnSpy);
  });

  it('initGlobalFunctions (ps_connect_register)', () => {
    service['initGlobalFunctions']();

    window.ps_connect_add_onready = jasmine.createSpy();
    window.ps_connect_register();

    expect(window.ps_connect_add_onready).toHaveBeenCalledWith(jasmine.any(Function));
  });

  it('initGlobalFunctions (ps_connect_get_client_api)', () => {
    service['initGlobalFunctions']();
    service._ps_connect_loaded = true;
    service._ps_connect_ready = true;

    window.ps_connect_push = [];

    expect(window.ps_connect_get_client_api()).toBe(window.ps_connect_push);

    service._ps_connect_loaded = false;
    expect(() => { window.ps_connect_get_client_api(); }).toThrowError('full API not yet ready');
  });

  it('initGlobalFunctions (ps_connect_make_channel_name)', () => {
    service['initGlobalFunctions']();

    expect(() => { window.ps_connect_make_channel_name('football-one', 1); }).toThrowError('bad channel_type football-one');
    expect(window.ps_connect_make_channel_name('sport', 2)).toBe('sportX0000000002');
  });

  xit('setDefaultValues', () => {
    window.push_common_subdomain = 'coral.co.uk';

    service['setDefaultValues']();

    expect(service._ps_connect_onready_fns).toEqual([]);
    expect(service._ps_connect_is_required).toBe(false);
    expect(service._ps_connect_ready).toBe(false);
    expect(service._ps_connect_started).toBe(false);
    expect(service._ps_connect_loaded).toBe(true);
    expect(window.domain).toBe(window.push_common_subdomain);
  });

  it('ps_connect_required', () => {
    service._ps_connect_is_required = false;
    service['ps_connect_source_iframe'] = jasmine.createSpy();
    service['ps_connect_required']();

    expect(service['ps_connect_source_iframe']).toHaveBeenCalled();
    expect(service._ps_connect_is_required).toBe(true);
  });

  xit('ps_connect_source_iframe', () => {
    window.push_iframe_id = 'live-serv-iframe-test';
    window.push_www_url = 'url-to-frame.com';
    window.push_version = '0.01';

    const frame: any = {};

    window.frames = {
      [window.push_iframe_id]: frame
    };

    service['ps_connect_source_iframe']();
    expect(frame.src).toBe(`${window.push_www_url}/push_api.html?v=${window.push_version}`);

    frame.location = {};
    service['ps_connect_source_iframe']();
    expect(frame.location.href).toBe(`${window.push_www_url}/push_api.html?v=${window.push_version}`);
  });

  it('ps_connect_start', () => {
    service._ps_connect_started = false;
    window.ps_connect_push = {
      ps_wrapper_set_cfg: jasmine.createSpy(),
      ps_client_set_auth_token: jasmine.createSpy(),
      ps_client_add_server: jasmine.createSpy(),
      ps_client_start: jasmine.createSpy()
    };
    window.push_location_handler = [{}];
    window.push_auth_token = [{}];
    window.push_instances = [{}, {}, {}];
    service._ps_connect_onready_fns = [jasmine.createSpy()];

    service['ps_connect_start']();

    expect(window.ps_connect_push.ps_wrapper_set_cfg).toHaveBeenCalledWith(
      'pushLocationHandler', window.push_location_handler
    );
    expect(window.ps_connect_push.ps_client_set_auth_token).toHaveBeenCalledWith(
      window.push_auth_token
    );
    expect(window.ps_connect_push.ps_client_add_server).toHaveBeenCalledWith(
      ...window.push_instances
    );
    expect(service._ps_connect_onready_fns[0]).toHaveBeenCalled();
    expect(window.ps_connect_push.ps_client_start).toHaveBeenCalled();
    expect(service._ps_connect_started).toBe(true);
  });
});
