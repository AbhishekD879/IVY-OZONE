export const EVENTS = {
  SOCKET_CONNECT_SUCCESS: 'ws.connectionSuccess',
  SOCKET_CONNECT_ERROR: 'ws.connectionError',

  SOCKET_RECONNECT_ATTEMPT: 'ws.reconnectAttempt',
  SOCKET_RECONNECT_SUCCESS: 'ws.reconnectSuccess',
  SOCKET_RECONNECT_ERROR: 'ws.reconnectError',

  SOCKET_DISCONNECT: 'ws.disconnect'
};
export const MatchCmtryConstants = {
  subMatchCmtry: 'subMatchCmtry',
  unsubMatchCmtry: 'unsubMatchCmtry',
  subLastMatchCode: 'subLastMatchCode'
}
export const SOCKETCODES = {
  SOCKET_PING: '2',
  SOCKET_MESSAGE_CONNECT: '40',
  SOCKET_MESSAGE_EVENT: '42',
  SOCKET_DISCONNECT: '1'
}
