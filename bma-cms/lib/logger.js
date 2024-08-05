// simple logger
const Logger = {
  log: console.log.bind(console, '[%s] [%s] %s'), // eslint-disable-line no-console
  dir: console.dir.bind(console, '[%s] [DIR] %s'), // eslint-disable-line no-console
  info: console.info.bind(console, '[%s] [INFO] %s'),
  warn: console.warn.bind(console, '[%s] [WARN] %s'),
  trace: console.trace.bind(console, '[%s] [TRACE] %s'), // eslint-disable-line no-console
  error: console.error.bind(console, '[%s] [ERROR] %s')
};

module.exports = Logger;
