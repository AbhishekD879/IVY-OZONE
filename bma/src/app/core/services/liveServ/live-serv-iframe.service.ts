import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';

declare let window: any;
declare let document: any;
declare let push_instances: any;
declare let push_iframe_id: any;
declare let push_www_url: any;
declare let push_version: any;
// eslint-disable-next-line
declare let ps_connect_push: any;
declare let ps_connect_add_onready: any;
declare let push_location_handler: any;
declare let push_auth_token: any;
declare let push_common_subdomain: any;
// eslint-disable-next-line
declare let ps_connect_register: any;

/* eslint-disable */
@Injectable()
export class LiveServIframeService {
  _ps_connect_onready_fns;
  _ps_connect_is_required;
  _ps_connect_loaded;
  _ps_connect_ready;
  _ps_connect_started;

  initIframe(): void {
    this.initGlobalVariables();
    this.initGlobalFunctions();
    this.setDefaultValues();
  }

  /**
   * Subscribe for update
   * @param keyId {string} - name of subscriber
   * @param callback {function}
   * @param channels {array} - ['sEVENT', 'sPRICE', ...]
   * @param lastMsgId {string} - update from time period
   */
  psRegister(keyId, callback, channels, lastMsgId) {
    window.ps_connect_register(keyId, callback, channels, lastMsgId);
  }

  private initGlobalVariables() {
    // document.domain = 'coral.co.uk';
    document.domain = environment.LIVESERV.DOMAIN;

    // let push_www_url = 'http://push-tst2.coral.co.uk';
    window.push_www_url = environment.LIVESERV.PUSH_URL;
    window.push_instances = [];

    // push_instances[push_instances.length] = 'push-tst2.coral.co.uk';
    window.push_instances[push_instances.length] = environment.LIVESERV.PUSH_INSTANCE_URL;
    window.push_instances[push_instances.length] = environment.LIVESERV.PUSH_INSTANCE_PORT;
    window.push_instances[push_instances.length] = environment.LIVESERV.PUSH_INSTANCE_TYPE;
    // let push_common_subdomain = 'coral.co.uk';

    window.push_common_subdomain = environment.LIVESERV.PUSH_COMMON_SUBDOMAIN;
    window.push_location_handler = environment.LIVESERV.PUSH_LOCATION_HANDLER;
    window.push_iframe_id = environment.LIVESERV.PUSH_IFRAME_ID;
    window.push_version = environment.LIVESERV.PUSH_VERSION;

    // Low-level API object.
    window.ps_connect_push = null;
  }

  private initGlobalFunctions() {
    const self = this;

    window.ps_connect_add_onready = function (fn) {
      self.ps_connect_required();
      if (!self._ps_connect_started) {
        self._ps_connect_onready_fns.push(fn);
      } else {
        fn();
      }
    };

    window.ps_connect_register = function (key, handler, channels, last_msg_id, letargs) {
      const allargs = arguments;
      const fn = function () {
        window.ps_connect_push.ps_client_register && window.ps_connect_push.ps_client_register.apply(window.ps_connect_push, allargs);
      };
      ps_connect_add_onready(fn);
    };

    window.ps_connect_get_client_api = function () {
      if (self._ps_connect_loaded && self._ps_connect_ready) {
        return window.ps_connect_push;
      } else {
        throw new Error(('full API not yet ready'));
      }
    };

    window.ps_connect_make_channel_name = function (channel_type, channel_number) {
      channel_type = '' + channel_type;
      if (channel_type.length > 6) {
        throw new Error(('bad channel_type ' + channel_type));
      }
      while (channel_type.length < 6) {
        channel_type += 'X';
      }
      channel_number = '' + channel_number;
      if (channel_type.length > 10) {
        throw new Error(('bad channel_number ' + channel_number));
      }
      while (channel_number.length < 10) {
        channel_number = '0' + channel_number;
      }
      return channel_type + channel_number;
    };

    // Called by the push iframe once it's ready.
    window.push_ready = function () {
      // Record where the push iframe is.
      const d = document;
      const f = d.frames ? d.frames[push_iframe_id] : d.getElementById(push_iframe_id);
      window.ps_connect_push = f.contentWindow || f;

      /* Provided the page is also ready, start now. */
      self._ps_connect_ready = true;
      if (self._ps_connect_loaded && self._ps_connect_ready) {
        self.ps_connect_start();
      }
    };

    // Called by the push iframe at unload.
    window.push_shutdown = function () {
      // currently a no-op.
      console.log('Push shutdown called');
    };
  }

  private setDefaultValues() {
    // Array of onready functions.
    this._ps_connect_onready_fns = [];

    // Has anyone asked for push functionality yet?
    this._ps_connect_is_required = false;

    this._ps_connect_ready = false;
    this._ps_connect_started = false;

    this._ps_connect_loaded = true;

    // Drop to common subdomain. Called inline.
    if (push_common_subdomain !== '') {
      document.domain = push_common_subdomain;
    }
  }

  /**
   * Someone needs a push.
   */
  private ps_connect_required() {
    if (this._ps_connect_is_required) {
      return;
    } else {
      this.ps_connect_source_iframe();
      this._ps_connect_is_required = true;
    }
  }

  /**
   * We don't source the iframe until push is needed.
   */
  private ps_connect_source_iframe() {
    const d = document;
    const f = d.frames ? d.frames[push_iframe_id] : d.getElementById(push_iframe_id);

    if (!f) {
      window.setTimeout(() => {
        this.ps_connect_source_iframe();
      }, 1050);
    } else {
      const src = push_www_url + '/push_api.html' + '?v=' + push_version;
      if (f.location) {
        f.location.href = src;
      } else {
        f.src = src;
      }
    }
  }

  /**
   * Called once the page has loaded and the push API is ready.
   */
  private ps_connect_start() {
    if (this._ps_connect_started) {
      return;
    }

    // Set the push location handler if found.
    if (window.push_location_handler && push_location_handler.length) {
      window.ps_connect_push.ps_wrapper_set_cfg
      ('pushLocationHandler', push_location_handler);
    }

    // Set the authentication token if found.
    if (window.push_auth_token && push_auth_token.length) {
      window.ps_connect_push.ps_client_set_auth_token(push_auth_token);
    }

    // Add the servers defined by js_global.html
    for (let i = 0; i < push_instances.length; i += 3) {
      window.ps_connect_push.ps_client_add_server(
        push_instances[i],
        push_instances[i + 1],
        push_instances[i + 2]
      );
    }

    // Call the onready handlers.
    for (let ii = 0; ii < this._ps_connect_onready_fns.length; ii++) {
      this._ps_connect_onready_fns[ii]();
    }

    window.ps_connect_push.ps_client_start();
    this._ps_connect_started = true;

    return;
  }
}
