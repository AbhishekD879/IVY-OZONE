(function() {
    // Create a global interceptor object
    window.interceptor = {
        interceptedRequests: {
            XHR: [],
            Fetch: [],
            WebSocket: [],
            SocketIO: [],
            Axios: [],
            RxJSAjax: []
        },
        originalXHR: window.XMLHttpRequest,
        originalFetch: window.fetch,
        originalWebSocket: window.WebSocket,
        originalIO: window.io,
        originalAxios: window.axios,
        intercepting: false,
        eventListeners: [],

        // Function to log request details
        logRequest(type, details) {
            console.log(`${type} Request: `, details);
            this.interceptedRequests[type].push({
                details,
                timestamp: new Date().toISOString()
            });
        },

        logError(type, error, url) {
            console.error(`${type} Error: `, error);
            this.interceptedRequests[type].push({
                error: error.message,
                url,
                timestamp: new Date().toISOString()
            });
        },

        // Method to start interception
        start() {
            if (this.intercepting) return;
            this.intercepting = true;

            const self = this;

            // Intercepting XMLHttpRequest
            window.XMLHttpRequest = function() {
                const realXHR = new self.originalXHR();

                realXHR.open = function(method, url, async, user, password) {
                    this._url = url;
                    this._method = method;
                    self.originalXHR.prototype.open.apply(this, arguments);
                };

                realXHR.setRequestHeader = function(header, value) {
                    if (!this._headers) {
                        this._headers = {};
                    }
                    this._headers[header] = value;
                    self.originalXHR.prototype.setRequestHeader.apply(this, arguments);
                };

                realXHR.send = function(body) {
                    const details = {
                        method: this._method,
                        url: this._url,
                        headers: this._headers || {},
                        body: body ? JSON.parse(JSON.stringify(body)) : null // Deep copy
                    };
                    self.logRequest('XHR', details);
                    const errorListener = function() {
                        self.logError('XHR', new Error('An error occurred during the XHR request.'), this._url);
                    };
                    this.addEventListener('error', errorListener);
                    self.eventListeners.push({
                        target: this,
                        type: 'error',
                        listener: errorListener
                    });
                    self.originalXHR.prototype.send.apply(this, arguments);
                };

                return realXHR;
            };

            // Intercepting Fetch API
            window.fetch = function() {
                const fetchArgs = arguments;
                const url = fetchArgs[0];
                const options = fetchArgs[1] || {};
                const headers = options.headers || {};

                const details = {
                    method: options.method || 'GET',
                    url: url,
                    headers: headers,
                    body: options.body ? JSON.parse(JSON.stringify(options.body)) : null // Deep copy
                };

                self.logRequest('Fetch', details);

                return self.originalFetch.apply(this, arguments).then(response => response).catch(error => {
                    self.logError('Fetch', error, url);
                    throw error;
                });
            };

            // Intercepting WebSocket
            window.WebSocket = function(url, protocols) {
                const socket = new self.originalWebSocket(url, protocols);

                const details = {
                    url: url,
                    protocols: protocols || null
                };
                self.logRequest('WebSocket', details);

                // Intercept WebSocket messages
                const originalSend = socket.send;
                socket.send = function(data) {
                    const dataCopy = JSON.parse(JSON.stringify(data)); // Deep copy
                    const jsonString = dataCopy.slice(2).trim();
                    let jsonData;
                    let parseError = false;
                    try {
                        jsonData = JSON.parse(jsonString);
                    } catch (err) {
                        parseError = true;
                        jsonData = jsonString;
                    }
                    self.logRequest('WebSocket', {
                        data: jsonData,
                        url,
                        parseError
                    });
                    originalSend.call(socket, data);
                };

                const messageListener = function(event) {
                    const dataCopy = JSON.parse(JSON.stringify(event.data)); // Deep copy
                    const jsonString = dataCopy.slice(2).trim();
                    let jsonData;
                    let parseError = false;
                    try {
                        jsonData = JSON.parse(jsonString);
                    } catch (err) {
                        parseError = true;
                        jsonData = jsonString;
                    }
                    self.logRequest('WebSocket', {
                        data: jsonData,
                        url,
                        parseError
                    });
                };
                socket.addEventListener('message', messageListener);
                self.eventListeners.push({
                    target: socket,
                    type: 'message',
                    listener: messageListener
                });

                const errorListener = function(error) {
                    self.logError('WebSocket', error, url);
                };
                socket.addEventListener('error', errorListener);
                self.eventListeners.push({
                    target: socket,
                    type: 'error',
                    listener: errorListener
                });

                return socket;
            };

            // Intercepting Socket.io
            if (window.io) {
                window.io = function(url, options) {
                    const socket = self.originalIO(url, options);

                    // Intercept Socket.io messages
                    const originalEmit = socket.emit;
                    socket.emit = function(eventName, ...args) {
                        const argsCopy = JSON.parse(JSON.stringify(args)); // Deep copy
                        self.logRequest('SocketIO', {
                            eventName,
                            args: argsCopy,
                            url
                        });
                        originalEmit.call(socket, eventName, ...args);
                    };

                    const errorListener = function(error) {
                        self.logError('SocketIO', error, url);
                    };
                    socket.on('error', errorListener);
                    self.eventListeners.push({
                        target: socket,
                        type: 'error',
                        listener: errorListener
                    });

                    const connectListener = function() {
                        self.logRequest('SocketIO', {
                            url
                        });
                    };
                    socket.on('connect', connectListener);
                    self.eventListeners.push({
                        target: socket,
                        type: 'connect',
                        listener: connectListener
                    });

                    const disconnectListener = function(reason) {
                        self.logRequest('SocketIO', {
                            reason,
                            url
                        });
                    };
                    socket.on('disconnect', disconnectListener);
                    self.eventListeners.push({
                        target: socket,
                        type: 'disconnect',
                        listener: disconnectListener
                    });

                    const anyListener = function(eventName, ...args) {
                        const argsCopy = JSON.parse(JSON.stringify(args)); // Deep copy
                        self.logRequest('SocketIO', {
                            eventName,
                            args: argsCopy,
                            url
                        });
                    };
                    socket.onAny(anyListener);
                    self.eventListeners.push({
                        target: socket,
                        type: 'any',
                        listener: anyListener
                    });

                    return socket;
                };
            }

            // Intercepting Axios
            if (window.axios) {
                window.axios.interceptors.request.use(function(config) {
                    const details = {
                        method: config.method.toUpperCase(),
                        url: config.url,
                        headers: config.headers,
                        data: config.data ? JSON.parse(JSON.stringify(config.data)) : null // Deep copy
                    };
                    self.logRequest('Axios', details);
                    return config;
                }, function(error) {
                    self.logError('Axios', error, error.config.url);
                    return Promise.reject(error);
                });

                window.axios.interceptors.response.use(function(response) {
                    return response;
                }, function(error) {
                    self.logError('Axios', error, error.config.url);
                    return Promise.reject(error);
                });
            } else {
                // If Axios is not available when the script runs, keep checking until it is
                const checkAxios = setInterval(() => {
                    if (window.axios) {
                        clearInterval(checkAxios);
                        window.axios.interceptors.request.use(function(config) {
                            const details = {
                                method: config.method.toUpperCase(),
                                url: config.url,
                                headers: config.headers,
                                data: config.data ? JSON.parse(JSON.stringify(config.data)) : null // Deep copy
                            };
                            self.logRequest('Axios', details);
                            return config;
                        }, function(error) {
                            self.logError('Axios', error, error.config.url);
                            return Promise.reject(error);
                        });

                        window.axios.interceptors.response.use(function(response) {
                            return response;
                        }, function(error) {
                            self.logError('Axios', error, error.config.url);
                            return Promise.reject(error);
                        });
                    }
                }, 1000); // Check every second
            }

            // Intercepting RxJS Ajax
            if (window.Rx && window.Rx.ajax) {
                const originalAjax = window.Rx.ajax.ajax;
                window.Rx.ajax.ajax = function(request) {
                    const url = request.url;
                    const details = {
                        method: request.method || 'GET',
                        url: url,
                        headers: request.headers,
                        body: request.body ? JSON.parse(JSON.stringify(request.body)) : null // Deep copy
                    };

                    self.logRequest('RxJSAjax', details);

                    return originalAjax.apply(this, arguments).pipe(tap(response => {
                        if (!response.response.ok) {
                            self.logError('RxJSAjax', new Error(`Request failed with status ${response.response.status}`), url);
                        }
                    }, error => {
                        self.logError('RxJSAjax', error, url);
                    }));
                };
            }
        },

        // Method to stop interception
        stop() {
            if (!this.intercepting) return;
            this.intercepting = false;

            // Restore original XMLHttpRequest, fetch, WebSocket, and Socket.io
            window.XMLHttpRequest = this.originalXHR;
            window.fetch = this.originalFetch;
            window.WebSocket = this.originalWebSocket;
            if (window.io) {
                window.io = this.originalIO;
            }
            if (window.axios) {
                window.axios.interceptors.request.eject();
                window.axios.interceptors.response.eject();
            }
            if (window.Rx && window.Rx.ajax) {
                window.Rx.ajax.ajax = this.originalAjax;
            }

            // Remove event listeners
            console.log(this.eventListeners)
            this.eventListeners.forEach(({
                target,
                type,
                listener
            }) => {
                target.removeEventListener(type, listener);
            });

            // Clear intercepted requests
            this.interceptedRequests = {
                XHR: [],
                Fetch: [],
                WebSocket: [],
                SocketIO: [],
                Axios: [],
                RxJSAjax: []
            };
        }
    };

    // Expose interception methods to be invoked from Python code
    window.exposeInterceptionMethods = function() {
        return {
            startInterception: function() {
                window.interceptor.start();
            },
            stopInterception: function() {
                window.interceptor.stop();
            },
            getInterceptedRequests: function(type) {
                return window.interceptor.interceptedRequests[type];
            },
            clearInterceptedRequests: function(type) {
                window.interceptor.interceptedRequests[type] = [];
            }
        };
    };
})();